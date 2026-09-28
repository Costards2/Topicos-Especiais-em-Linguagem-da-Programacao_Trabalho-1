import requests # Importa a biblioteca 'requests' para efetuar chamadas HTTP e comunicar com a API da internet (GitHub).
import pandas as pd # Importa o Pandas (com o apelido 'pd') para transformar os dados brutos em tabelas estruturadas (DataFrames) e guardá-los.
import subprocess # Importa o módulo 'subprocess' para permitir que o Python execute comandos nativos do terminal (linha de comandos).
import os # Importa funcionalidades do sistema operativo, utilizado aqui para verificar se uma pasta existe no disco rígido.

# ==========================================
# CONFIGURAÇÕES DA API
# ==========================================
# Insira o seu NOVO token gerado aqui. Ocultei o antigo por segurança.
GITHUB_TOKEN = "SEU_NOVO_TOKEN_AQUI" 

HEADERS = {
    "Accept": "application/vnd.github+json", # Informa o GitHub que o nosso script espera receber a resposta em formato JSON.
    "Authorization": f"Bearer {GITHUB_TOKEN}", # Envia o seu Token como um "crachá" de identificação, permitindo descarregar dados sem esbarrar no limite para utilizadores anónimos.
    "X-GitHub-Api-Version": "2022-11-28", # Fixa a versão da API do GitHub para garantir que alterações futuras nos servidores deles não quebrem o seu script.
}

# Cria uma lista de dicionários. Cada dicionário guarda o dono do projeto, o nome do repositório na web e a localização da pasta clonada no seu computador.
REPOSITORIOS = [
    {"owner": "pallets", "repo": "flask", "pasta": "./flask"},
    {"owner": "renpy", "repo": "renpy", "pasta": "./renpy"},
    {"owner": "love2d", "repo": "love", "pasta": "./love"}
]

# ==========================================
# FUNÇÕES DE NUVEM (API GITHUB)
# ==========================================
def extrair_contribuidores(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors" # Monta o endereço web (URL) exato para aceder à lista de contribuidores do projeto.
    resp = requests.get(url, headers=HEADERS, params={"per_page": 100}) # Faz a requisição GET ao GitHub, pedindo para enviar 100 contribuidores por página.
    if resp.status_code == 200: # Verifica se a resposta do servidor foi "200 OK" (sucesso).
        # Converte a resposta JSON numa tabela do Pandas e guarda-a como um ficheiro CSV na sua pasta, sem incluir a coluna de índice (index=False).
        pd.DataFrame(resp.json()).to_csv(f"{repo}_contrib.csv", index=False)
        
def extrair_issues_e_prs(owner, repo, limite=100):
    """
    Descarrega Issues e PRs juntos usando a rota de issues.
    Isto garante que obtemos a contagem real de comentários e o título para classificar bugs/features.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues" # Monta o endereço da API para aceder às Issues (que no GitHub também incluem os Pull Requests).
    resp = requests.get(url, headers=HEADERS, params={"state": "all", "per_page": limite}) # Pede os últimos 100 itens, independentemente de estarem abertos ou fechados ("state": "all").
    
    if resp.status_code != 200: # Se o servidor não responder com sucesso (200), imprime um aviso e interrompe esta função.
        print(f"Erro ao baixar PRs/Issues de {repo}: {resp.status_code}")
        return
        
    dados_prs = [] # Cria uma lista vazia para armazenar temporariamente os dados dos Pull Requests.
    dados_issues = [] # Cria uma lista vazia para armazenar temporariamente os dados das Issues (tarefas normais).
    
    for item in resp.json(): # Inicia um laço de repetição que vai iterar sobre cada um dos 100 itens descarregados do GitHub.
        comentarios = item.get('comments', 0) # Tenta recolher a quantidade de comentários; se não existir, assume 0.
        titulo = item.get('title', '').lower() # Puxa o título da postagem e converte-o todo para minúsculas (.lower()) para facilitar a pesquisa de palavras.
        labels = [l['name'].lower() for l in item.get('labels', [])] # Puxa todas as etiquetas oficiais (labels) associadas ao item e também as converte para minúsculas.
        
        # Se a chave 'pull_request' existir dentro do item JSON, significa que é um código submetido (usado nas métricas 2, 3 e 6).
        if 'pull_request' in item:
            # Adiciona um dicionário à lista de PRs extraindo apenas as propriedades que nos interessam para a matemática.
            dados_prs.append({
                "repo": repo,
                "criado_em": item['created_at'], # Regista quando o PR foi aberto.
                "fechado_em": item['closed_at'], # Regista quando foi fechado.
                "comentarios": comentarios, # Regista o atrito/debate técnico.
                "merge_feito": item.get('pull_request', {}).get('merged_at') is not None # Avalia como Verdadeiro (True) se existir uma data de "merged" (aceitação), ou Falso se for nulo.
            })
        # Se não tiver a chave 'pull_request', é uma Issue normal de discussão de falhas/ideias (usada na métrica 7).
        else:
            categoria = 'outros' # Define a categoria padrão caso não consigamos identificar sobre o que é a Issue.
            
            # Procura por palavras-chave indicadoras de falhas ('bug', 'fix', etc.) no título OU verifica se os mantenedores lhe colaram a etiqueta 'bug'.
            if any(p in titulo for p in ['bug', 'fix', 'error', 'crash']) or 'bug' in labels:
                categoria = 'bug' # Classifica oficialmente como anomalia.
            # Procura por palavras-chave indicadoras de novidades ('add', 'feature', etc.) no título OU na etiqueta 'enhancement'.
            elif any(p in titulo for p in ['add', 'feature', 'support']) or 'enhancement' in labels:
                categoria = 'feature' # Classifica oficialmente como inovação/funcionalidade.
                
            # Adiciona o item classificado à lista de Issues com as suas datas de ciclo de vida.
            dados_issues.append({
                "repo": repo,
                "categoria": categoria,
                "criado_em": item['created_at'],
                "fechado_em": item['closed_at']
            })
            
    # Após processar os 100 itens, converte a lista de PRs numa tabela Pandas e guarda-a como CSV (apenas se a lista não estiver vazia).
    if dados_prs: pd.DataFrame(dados_prs).to_csv(f"{repo}_prs.csv", index=False)
    # Faz o mesmo para a lista de Issues classificada.
    if dados_issues: pd.DataFrame(dados_issues).to_csv(f"{repo}_issues.csv", index=False)

# ==========================================
# FUNÇÕES LOCAIS (HISTÓRICO GIT)
# ==========================================
def extrair_git_local(pasta_repo, repo_nome):
    """Lê o histórico do disco rígido para as métricas de Hotspots e Horários."""
    if not os.path.exists(pasta_repo): # Verifica se o caminho no disco rígido (ex: ./flask) realmente existe.
        print(f"Aviso: Pasta '{pasta_repo}' não encontrada. Faça o git clone primeiro para ter as métricas locais.")
        return # Se não existir, cancela a execução local.
        
    # Prepara o comando a ser injetado no terminal: pede ao Git o histórico de alterações (log) mostrando apenas os nomes dos ficheiros e a data/hora exata (ISO).
    comando = ['git', '-C', pasta_repo, 'log', '--name-only', '--format=COMMIT|%ad', '--date=iso']
    # O Python executa o comando silenciosamente nos bastidores e captura o texto que o Git "cuspiu" na variável 'resultado'.
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, text=True, errors='ignore')
    
    datas, arquivos = [], [] # Listas para acumular as datas extraídas e os nomes dos ficheiros alterados.
    data_atual = None # Variável de controlo para guardar a data do commit que está a ser lido no momento.
    
    # Separa o texto gigantesco do Git linha por linha e itera sobre ele.
    for linha in resultado.stdout.split('\n'):
        linha = linha.strip() # Remove espaços vazios no início e no fim da linha.
        if not linha: continue # Se a linha estiver em branco, salta para a próxima.
        
        if linha.startswith('COMMIT|'): # Se a linha começar com a tag criada, sabemos que é um bloco de data.
            data_atual = linha.split('|')[1] # Divide o texto pelo tubo '|' e guarda apenas a parte da data/hora.
            datas.append({"repo": repo_nome, "data_str": data_atual}) # Adiciona a data encontrada à lista de horários.
        elif data_atual: # Se não começou com 'COMMIT|', então é o nome de um ficheiro que foi alterado naquele momento.
            arquivos.append({"repo": repo_nome, "arquivo": linha}) # Adiciona o nome do ficheiro à lista de Hotspots.
            
    # Converte as listas de datas e de ficheiros alterados em tabelas Pandas independentes e guarda-as no disco.
    pd.DataFrame(datas).to_csv(f"{repo_nome}_datas_git.csv", index=False)
    pd.DataFrame(arquivos).to_csv(f"{repo_nome}_hotspots_git.csv", index=False)

# ==========================================
# EXECUÇÃO DA EXTRAÇÃO
# ==========================================
# Bloco final que põe o código inteiro a trabalhar de forma orquestrada.
for p in REPOSITORIOS: # Para cada um dos três projetos configurados lá em cima...
    print(f"[{p['repo']}] A iniciar extração completa...") # Avisa no terminal qual projeto está a ser minado.
    extrair_contribuidores(p["owner"], p["repo"]) # Aciona a função 1 (Contribuidores).
    extrair_issues_e_prs(p["owner"], p["repo"]) # Aciona a função 2 (Bugs, Features e PRs).
    extrair_git_local(p["pasta"], p["repo"]) # Aciona a função 3 (Horários e Arquivos Locais).

# Mensagem de encerramento avisando que toda a mineração e criação de bases de dados CSV foi concluída.
print("\nExtração consolidada concluída com sucesso! Tabelas prontas.")