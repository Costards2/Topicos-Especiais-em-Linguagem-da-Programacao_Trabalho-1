import os # Importa ferramentas do sistema operacional. Permite ao Python criar pastas e ler configurações do seu computador.
import subprocess # Permite que o Python "digite" comandos no terminal automaticamente, como se fosse um usuário humano.
import pandas as pd # Importa o Pandas (apelidado de 'pd'), que funciona como um "Excel invisível" para organizar dados em tabelas e salvá-los.
import requests # Importa o "carteiro" da internet: uma ferramenta que viaja até os servidores do GitHub para buscar as informações.
from dotenv import load_dotenv # Importa a chave do cofre: lê o arquivo escondido '.env' para não deixarmos senhas expostas no código.

# ==========================================
# CONFIGURAÇÕES INICIAIS E SEGURANÇA
# ==========================================

# Abre o arquivo '.env' e carrega a sua senha secreta para a memória do programa.
load_dotenv()

# Pega o token de acesso (a sua "identidade" no GitHub) que foi carregado no passo anterior.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Se você esqueceu de criar o arquivo .env ou de colocar o token lá, o programa avisa na tela.
if not GITHUB_TOKEN:
    print("Aviso: GITHUB_TOKEN não encontrado no ficheiro .env!")

# Cria o "crachá" que enviaremos ao GitHub em cada pedido para provarmos quem somos.
HEADERS = {
    "Accept": "application/vnd.github+json", # Pede ao GitHub que entregue os dados no formato padrão da web (JSON, que parece um dicionário).
    "Authorization": f"Bearer {GITHUB_TOKEN}", # Apresenta o seu token. Isso diz ao GitHub: "Sou eu, aumente meu limite de downloads".
    "X-GitHub-Api-Version": "2022-11-28", # Fixa a versão do sistema do GitHub. Assim, se o GitHub atualizar amanhã, nosso robô não quebra.
}

# Uma lista contendo as rotas de cada projeto. Tem o nome do criador original (owner), o nome do projeto (repo) e onde ele está no seu disco (pasta).
REPOSITORIOS = [
    {"owner": "pallets", "repo": "flask", "pasta": "./flask"},
    {"owner": "renpy", "repo": "renpy", "pasta": "./renpy"},
    {"owner": "love2d", "repo": "love", "pasta": "./love"},
]

# ==========================================
# FUNÇÃO 1: BUSCAR QUEM AJUDA NO PROJETO
# ==========================================
def extrair_contribuidores(owner, repo, pasta_destino):
    # Monta o link exato da internet para pedir a lista de voluntários/funcionários do projeto.
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    
    # O "carteiro" (requests) bate na porta do GitHub e pede até 100 pessoas por página.
    resp = requests.get(url, headers=HEADERS, params={"per_page": 100})
    
    # Se o servidor responder com "200" (o código universal da internet para "Tudo Certo!"):
    if resp.status_code == 200:
        # Pega a resposta, converte numa tabela de Excel (DataFrame) e salva como um arquivo .csv dentro da pasta correta.
        pd.DataFrame(resp.json()).to_csv(f"{pasta_destino}/{repo}_contrib.csv", index=False)

# ==========================================
# FUNÇÃO 2: BUSCAR DEFEITOS E MELHORIAS (ISSUES E PRS)
# ==========================================
def extrair_issues_e_prs(owner, repo, pasta_destino, limite=100):
    # Monta o link para buscar o mural de tarefas e discussões do projeto.
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    # Pede os últimos 100 registros do mural, mesmo os que já foram fechados ou resolvidos ("state": "all").
    resp = requests.get(url, headers=HEADERS, params={"state": "all", "per_page": limite})
    
    # Se a internet cair ou o GitHub negar o acesso, ele avisa o erro e para o trabalho dessa função.
    if resp.status_code != 200:
        print(f"Erro ao baixar PRs/Issues de {repo}: {resp.status_code}")
        return

    dados_prs = [] # Cria uma gaveta vazia para guardar as sugestões de código (Pull Requests).
    dados_issues = [] # Cria uma gaveta vazia para guardar as reclamações de defeitos ou pedidos de inovação (Issues).
    
    # Para cada anotação (item) que o GitHub nos enviou:
    for item in resp.json():
        # Tenta ver quantos comentários a anotação tem. Se não tiver nada, anota 0.
        comentarios = item.get("comments", 0)
        # Pega o título da anotação e transforma tudo em letra minúscula para facilitar a nossa leitura automática.
        titulo = item.get("title", "").lower()
        # Pega as etiquetas (tags) coloridas que os chefes do projeto colaram na anotação.
        labels = [l["name"].lower() for l in item.get("labels", [])]

        # Se a anotação tiver uma marca d'água chamada 'pull_request', sabemos que alguém enviou código novo.
        if "pull_request" in item:
            # Guarda na gaveta de Pull Requests apenas as datas, os comentários e se o código foi aceito (merged_at).
            dados_prs.append({
                "repo": repo,
                "criado_em": item["created_at"],
                "fechado_em": item["closed_at"],
                "comentarios": comentarios,
                "merge_feito": item.get("pull_request", {}).get("merged_at") is not None, # Vira 'True' se foi aceito, 'False' se foi rejeitado.
            })
        
        # Se não for envio de código, é apenas uma discussão (Issue).
        else:
            categoria = "outros" # Por padrão, dizemos que não sabemos do que se trata.
            
            # Se o título tiver a palavra 'bug', 'erro' ou se tiver a etiqueta oficial de bug:
            if any(p in titulo for p in ["bug", "fix", "error", "crash"]) or "bug" in labels:
                categoria = "bug" # Classifica como conserto de defeito.
            
            # Se o título tiver a palavra 'adicionar', 'nova' ou etiqueta de melhoria:
            elif any(p in titulo for p in ["add", "feature", "support"]) or "enhancement" in labels:
                categoria = "feature" # Classifica como criação de uma inovação.

            # Guarda a discussão na gaveta de Issues com a sua categoria (Bug ou Inovação) e as datas.
            dados_issues.append({
                "repo": repo,
                "categoria": categoria,
                "criado_em": item["created_at"],
                "fechado_em": item["closed_at"],
            })

    # Se a gaveta de Pull Requests não estiver vazia, transforma num arquivo CSV e salva no disco.
    if dados_prs:
        pd.DataFrame(dados_prs).to_csv(f"{pasta_destino}/{repo}_prs.csv", index=False)
    
    # Se a gaveta de Issues não estiver vazia, faz a mesma coisa.
    if dados_issues:
        pd.DataFrame(dados_issues).to_csv(f"{pasta_destino}/{repo}_issues.csv", index=False)

# ==========================================
# FUNÇÃO 3: LER O DIÁRIO LOCAL DO COMPUTADOR
# ==========================================
def extrair_git_local(pasta_repo, repo_nome, pasta_destino):
    # Verifica se a pasta do projeto (ex: ./flask) realmente existe no seu computador.
    if not os.path.exists(pasta_repo):
        print(f"Aviso: Pasta '{pasta_repo}' não encontrada. Você precisa fazer o download do código primeiro.")
        return # Se a pasta não existir, cancela essa etapa.

    # Prepara uma instrução para o sistema operacional: "Abra a pasta do projeto e me dê a lista de todos os arquivos modificados e a hora exata".
    comando = ["git", "-C", pasta_repo, "log", "--name-only", "--format=COMMIT|%ad", "--date=iso"]
    
    # O Python "digita" a instrução de forma invisível e guarda toda a resposta do terminal na variável 'resultado'.
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, text=True, errors="ignore")

    datas = [] # Gaveta para as datas em que as pessoas trabalharam.
    arquivos = [] # Gaveta para os nomes dos arquivos que foram consertados.
    data_atual = None # Um marcador para o robô não se perder enquanto lê a lista.

    # O robô lê a resposta gigante do terminal, cortando-a linha por linha.
    for linha in resultado.stdout.split("\n"):
        linha = linha.strip() # Limpa espaços em branco inúteis no começo e no fim da linha.
        
        if not linha: # Se a linha estiver vazia, pula para a próxima.
            continue
            
        # Se a linha começar com a nossa marca "COMMIT|", o robô sabe que acabou de achar um registro de data e hora.
        if linha.startswith("COMMIT|"):
            data_atual = linha.split("|")[1] # Corta a palavra 'COMMIT' e pega só a data, guardando na memória.
            datas.append({"repo": repo_nome, "data_str": data_atual}) # Guarda a data na gaveta.
            
        # Se não tiver a marca "COMMIT|", o robô entende que aquilo é o nome de um arquivo que foi alterado naquela mesma data.
        elif data_atual:
            arquivos.append({"repo": repo_nome, "arquivo": linha}) # Guarda o nome do arquivo na gaveta.

    # Transforma a gaveta de datas em tabela CSV e salva.
    pd.DataFrame(datas).to_csv(f"{pasta_destino}/{repo_nome}_datas_git.csv", index=False)
    # Transforma a gaveta de arquivos em tabela CSV e salva. Isso revelará os "Hotspots" (arquivos mais defeituosos).
    pd.DataFrame(arquivos).to_csv(f"{pasta_destino}/{repo_nome}_hotspots_git.csv", index=False)

# ==========================================
# O MOTOR PRINCIPAL (ONDE TUDO COMEÇA)
# ==========================================
# Aqui o robô repete todo o processo acima para cada um dos 3 projetos (Flask, Renpy, Love).
for p in REPOSITORIOS:
    print(f"[{p['repo']}] A extrair dados...") # Avisa na tela qual projeto está sendo analisado agora.
    
    # Cria dinamicamente o caminho da pasta onde os dados vão ficar organizados (ex: 'dados/flask').
    pasta_destino = f"dados/{p['repo']}"
    
    # Pede ao computador para criar a pasta fisicamente. Se ela já existir, ele não faz nada e segue em frente.
    os.makedirs(pasta_destino, exist_ok=True)

    # Executa a Função 1 (Baixar Contribuidores)
    extrair_contribuidores(p["owner"], p["repo"], pasta_destino)
    
    # Executa a Função 2 (Baixar Bugs e Features)
    extrair_issues_e_prs(p["owner"], p["repo"], pasta_destino)
    
    # Executa a Função 3 (Ler arquivos locais do disco rígido)
    extrair_git_local(p["pasta"], p["repo"], pasta_destino)

# Quando terminar todos os 3 projetos, avisa que o trabalho pesado acabou.
print("\nExtração concluída com sucesso! Ficheiros salvos de forma organizada na pasta 'dados/'.")