import pandas as pd # O Pandas (apelidado de 'pd') é como um "Excel invisível". Ele abre nossos arquivos CSV e nos deixa fazer contas e filtros com eles.
import matplotlib.pyplot as plt # O Matplotlib (apelidado de 'plt') é o nosso "desenhista". Ele pega os números do Pandas e desenha os gráficos coloridos.
import numpy as np # O NumPy (apelidado de 'np') é o nosso "matemático". Vamos usá-lo para criar uma régua invisível no Gráfico 7.
import os # O 'os' nos permite falar com o sistema operacional para criar pastas ou procurar arquivos.

# Pede ao computador para criar uma pasta chamada "graficos". O 'exist_ok=True' avisa: "Se a pasta já existir, não precisa criar de novo nem dar erro".
os.makedirs("graficos", exist_ok=True)

# ==========================================
# CONFIGURAÇÕES INICIAIS
# ==========================================
PROJETOS = ['flask', 'renpy', 'love'] # A lista com as siglas das pastas onde guardamos os dados de cada projeto.
CORES = {'flask': '#4C72B0', 'renpy': '#DD8452', 'love': '#55A868'} # Um dicionário com os códigos hexadecimais das cores exatas para padronizar cada projeto.
NOMES = ['Flask (Base)', 'RenPy', 'Love2D'] # Nomes amigáveis e bem formatados que vão aparecer nos títulos dos gráficos.

# ==========================================
# GRÁFICO 1: BUS FACTOR (DEPENDÊNCIA DE PESSOAS)
# ==========================================
try: # "Tente rodar este código. Se der algum erro (como faltar um arquivo), não feche o programa, apenas pule para a próxima etapa."
    bf_valores = [] # Cria uma gaveta vazia para guardar os 3 resultados finais.
    
    for p in PROJETOS: # O robô vai repetir isso 3 vezes (uma para o Flask, uma para o Renpy, uma para o Love).
        df = pd.read_csv(f"dados/{p}/{p}_contrib.csv") # O Pandas lê o arquivo CSV e o transforma numa tabela virtual na memória.
        total = df['contributions'].sum() # Pega a coluna inteira de contribuições e soma tudo para sabermos o total de trabalho feito no projeto.
        top3 = df.nlargest(3, 'contributions')['contributions'].sum() # Pega apenas os 3 programadores que mais trabalharam e soma o trabalho deles.
        bf_valores.append((top3 / total) * 100) # Divide o trabalho dos 3 pelo trabalho total para descobrir a porcentagem, e guarda na gaveta.

    # Agora vamos desenhar!
    fig, ax = plt.subplots(figsize=(10, 6)) # Cria uma tela em branco (fig) do tamanho 10x6 polegadas e uma área de desenho (ax).
    barras = ax.bar(NOMES, bf_valores, color=[CORES[p] for p in PROJETOS], edgecolor='black') # Desenha as barras verticais usando as cores e nomes que configuramos lá em cima.
    
    # Escreve o título principal e os nomes dos eixos X (horizontal) e Y (vertical).
    ax.set_title("Métrica de Risco: Bus Factor (Top 3 Contribuidores)\nMenor % indica maior distribuição de conhecimento", fontsize=14, pad=15) 
    ax.set_ylabel("Percentual de Contribuição (%)", fontsize=12)
    ax.set_xlabel("Repositórios Avaliados", fontsize=12)
    
    # Pede ao "desenhista" para olhar a altura de cada barra e escrever o número exato no topo dela (ex: 45.2%).
    ax.bar_label(barras, fmt='%.1f%%', padding=3, fontweight='bold', fontsize=11)
    
    ax.margins(y=0.15) # Empurra o teto do gráfico 15% para cima, para que o número que acabamos de escrever não fique cortado na borda.
    plt.tight_layout() # Arruma todos os espaçamentos internos de forma inteligente para a imagem ficar bonita.
    plt.savefig("graficos/grafico_01_bus_factor.png", dpi=300) # Salva o desenho como uma imagem PNG de alta qualidade.
    plt.close() # Apaga o quadro branco para o próximo gráfico começar do zero.
except Exception as e: print(f"Erro G1: {e}")

# ==========================================
# GRÁFICO 2: CADÊNCIA (VELOCIDADE DE RESPOSTA)
# ==========================================
try:
    tempo_prs = [] # Gaveta para as médias de tempo.
    
    for p in PROJETOS:
        df = pd.read_csv(f"dados/{p}/{p}_prs.csv") # Abre a tabela de envios de código (Pull Requests).
        df = df.dropna(subset=['fechado_em']) # Descarta qualquer linha da tabela que não tenha data de fechamento (tarefas ainda inacabadas).
        
        # O Python não sabe subtrair textos. Estas linhas convertem os textos de data num "Objeto Calendário" que o computador entende.
        df['criado_em'] = pd.to_datetime(df['criado_em'])
        df['fechado_em'] = pd.to_datetime(df['fechado_em'])
        
        # Subtrai o fim pelo começo, descobre o total de segundos de diferença e divide por 86400 (os segundos de um dia) para termos a resposta em dias.
        df['tempo_dias'] = (df['fechado_em'] - df['criado_em']).dt.total_seconds() / 86400
        tempo_prs.append(df['tempo_dias'].mean()) # Calcula a média de todos os dias e guarda na gaveta.

    fig, ax = plt.subplots(figsize=(10, 6)) # Cria a tela.
    barras = ax.barh(NOMES, tempo_prs, color=[CORES[p] for p in PROJETOS], edgecolor='black') # O 'barh' desenha barras DEITADAS (horizontais).
    
    ax.set_title("Cadência de Engenharia: Tempo Médio de Resolução de PRs", fontsize=14, pad=15)
    ax.set_xlabel("Tempo Médio de Resolução (em Dias)", fontsize=12)
    ax.set_ylabel("Repositórios Avaliados", fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.5) # Cria linhas pontilhadas de fundo no eixo X para facilitar a leitura visual.

    ax.bar_label(barras, fmt='%.1f dias', padding=5, fontweight='bold', fontsize=11) # Escreve os dias no final de cada barra.
    ax.margins(x=0.2) # Dá um espaço extra de 20% à direita para o texto não bater na parede da imagem.
    
    plt.tight_layout()
    plt.savefig("graficos/grafico_02_cadencia_prs.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G2: {e}")

# ==========================================
# GRÁFICO 3: DENSIDADE DE DISCUSSÃO (ATRITO)
# ==========================================
try:
    densidade_prs = [] # Gaveta para a média de comentários.
    for p in PROJETOS:
        df = pd.read_csv(f"dados/{p}/{p}_prs.csv")
        densidade_prs.append(df['comentarios'].mean()) # Vai direto na coluna 'comentarios', calcula a média matemática e guarda.

    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(NOMES, densidade_prs, color=[CORES[p] for p in PROJETOS], edgecolor='black')
    
    ax.set_title("Atrito de Processo: Comentários Médios por Pull Request", fontsize=14, pad=15)
    ax.set_ylabel("Quantidade Média de Comentários", fontsize=12)
    ax.set_xlabel("Repositórios Avaliados", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    ax.bar_label(barras, fmt='%.1f', padding=3, fontweight='bold', fontsize=11)
    ax.margins(y=0.15)
    
    plt.tight_layout()
    plt.savefig("graficos/grafico_03_atrito_comentarios.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G3: {e}")

# ==========================================
# GRÁFICO 4: DISTRIBUIÇÃO DE HORÁRIOS
# ==========================================
try:
    # Cria uma tela extra larga (18x6) e a divide em 3 quadros menores. O 'sharey=True' garante que todos os 3 usem a mesma escala de altura.
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    axes[0].set_ylabel("Volume Total de Commits", fontsize=12) # Escreve o texto vertical apenas no primeiro quadro da esquerda.
    
    for i, p in enumerate(PROJETOS): # O 'enumerate' numera os projetos (0, 1 e 2) para sabermos em qual dos 3 quadros vamos desenhar.
        arquivo_datas = f"dados/{p}/{p}_datas_git.csv"
        
        if os.path.exists(arquivo_datas): # Verifica se o arquivo existe antes de tentar abrir.
            df = pd.read_csv(arquivo_datas)
            df['data'] = pd.to_datetime(df['data_str'], utc=True) # Converte a data e ajusta para o relógio global padrão (UTC).
            df['hora'] = df['data'].dt.hour # Arranca fora o dia, mês e ano, guardando apenas o número da hora (0h a 23h).
            
            # Conta quantas vezes cada hora aparece, ordena do 0 ao 23, e manda o Pandas desenhar a barra no quadro correto (ax=axes[i]).
            ax_plot = df['hora'].value_counts().sort_index().plot(kind='bar', ax=axes[i], color=CORES[p], edgecolor='black')
            
            axes[i].set_title(NOMES[i], fontsize=14)
            axes[i].set_xlabel("Hora do Dia (0h - 23h, Fuso UTC)", fontsize=11)
            axes[i].tick_params(axis='x', rotation=0) # Mantém os números da base (0, 1, 2...) deitados e fáceis de ler.
            
            for container in ax_plot.containers:
                # Escreve a quantidade exata no topo de cada barrinha, mas gira o texto em 90 graus para eles não se atropelarem.
                axes[i].bar_label(container, padding=4, fontsize=9, rotation=90, fontweight='bold')
            
            axes[i].margins(y=0.30) # Aumenta bastante o teto, pois o texto em pé ocupa muito espaço.

    plt.suptitle("Cultura de Trabalho: Distribuição de Horários de Commit", fontsize=16, fontweight='bold') # Título mestre que abrange os 3 quadros.
    plt.tight_layout()
    plt.savefig("graficos/grafico_04_horarios.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G4: {e}")

# ==========================================
# GRÁFICO 5: ARQUIVOS MAIS QUEBRADOS (HOTSPOTS)
# ==========================================
# Esse gráfico é diferente: ele vai gerar 3 imagens separadas (uma para cada projeto).
for p, nome_legivel in zip(PROJETOS, NOMES): # Une a sigla (flask) ao nome bonito (Flask (Base)) para trabalharmos com os dois ao mesmo tempo.
    try:
        arquivo_hotspots = f"dados/{p}/{p}_hotspots_git.csv"
        if os.path.exists(arquivo_hotspots):
            df_hotspots = pd.read_csv(arquivo_hotspots)
            # Pede ao computador para contar qual nome de arquivo se repete mais vezes e pegar apenas os 5 primeiros (Top 5).
            top_files = df_hotspots['arquivo'].value_counts().head(5) 

            fig, ax = plt.subplots(figsize=(10, 5))
            top_files.plot(kind='barh', ax=ax, color=CORES[p], edgecolor='black') # Desenha as 5 barras na horizontal.
            
            ax.set_title(f"Gargalos de Arquitetura: Os 5 Arquivos Mais Alterados ({nome_legivel})", fontsize=13, pad=15)
            ax.set_xlabel("Frequência de Modificações (Quantidade de Commits)", fontsize=12)
            ax.set_ylabel("Nome do Arquivo (Caminho)", fontsize=12)
            
            ax.invert_yaxis() # Inverte o gráfico de cabeça para baixo para o maior arquivo ficar bonitão no topo, e não no chão.
            
            for container in ax.containers:
                ax.bar_label(container, padding=5, fontweight='bold', fontsize=10) # Coloca o número exato no fim de cada barra.
                
            ax.margins(x=0.15)
            plt.tight_layout()
            plt.savefig(f"graficos/grafico_05_hotspots_{p}.png", dpi=300) # Salva a imagem usando o nome do projeto atual.
            plt.close()
    except Exception as e: print(f"Erro G5 ({p}): {e}")

# ==========================================
# GRÁFICO 6: TAXA DE ACEITAÇÃO (MERGE RATE)
# ==========================================
try:
    taxa_merge = []
    for p in PROJETOS:
        df = pd.read_csv(f"dados/{p}/{p}_prs.csv")
        total_prs = len(df) # Conta quantas linhas a tabela tem no total (ex: 100).
        aceitos = df['merge_feito'].sum() # Como 'True' vale 1 e 'False' vale 0, somar a coluna nos dá o número exato de sugestões aceitas.
        
        # Matemática de porcentagem normal (aceitos divididos pelo total vezes 100). O "if" impede que o computador tente dividir por zero caso a tabela esteja vazia.
        taxa_merge.append((aceitos / total_prs) * 100 if total_prs > 0 else 0) 

    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(NOMES, taxa_merge, color=[CORES[p] for p in PROJETOS], edgecolor='black')
    
    ax.set_title("Taxa de Sucesso de PRs (Merge Rate)", fontsize=14, pad=15)
    ax.set_ylabel("Taxa de Aceitação (%)", fontsize=12)
    ax.set_xlabel("Repositórios Avaliados", fontsize=12)
    
    ax.bar_label(barras, fmt='%.1f%%', padding=3, fontweight='bold', fontsize=11)
    ax.margins(y=0.15)
    
    plt.tight_layout()
    plt.savefig("graficos/grafico_06_merge_rate.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G6: {e}")

# ==========================================
# GRÁFICO 7: BUGS VS NOVAS FUNCIONALIDADES
# ==========================================
try:
    tempos_bugs = [] # Gaveta para a média de tempo arrumando erros.
    tempos_features = [] # Gaveta para a média de tempo criando inovações.

    for p in PROJETOS:
        df = pd.read_csv(f"dados/{p}/{p}_issues.csv")
        df = df.dropna(subset=['fechado_em']) # Limpa as tarefas inacabadas.
        
        # Converte os textos para datas e acha a diferença em dias.
        df['criado_em'] = pd.to_datetime(df['criado_em'])
        df['fechado_em'] = pd.to_datetime(df['fechado_em'])
        df['tempo_dias'] = (df['fechado_em'] - df['criado_em']).dt.total_seconds() / 86400
        
        # Separa a tabela original em duas tabelas menores: uma só com bugs e outra só com features (inovações).
        df_bugs = df[df['categoria'] == 'bug']
        df_features = df[df['categoria'] == 'feature']
        
        # Calcula a média das duas separadamente. Se a tabela menor estiver vazia (empty), anota 0.
        media_bug = df_bugs['tempo_dias'].mean() if not df_bugs.empty else 0
        media_feature = df_features['tempo_dias'].mean() if not df_features.empty else 0
        
        # Guarda as duas médias nas gavetas definitivas.
        tempos_bugs.append(media_bug if pd.notna(media_bug) else 0)
        tempos_features.append(media_feature if pd.notna(media_feature) else 0)

    # Aqui é o segredo das barras duplas: a matemática (NumPy) cria as posições 0, 1 e 2 no gráfico.
    x = np.arange(len(PROJETOS)) 
    largura = 0.35 # Define que cada barra ocupará apenas 35% de espaço.

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Desenha as barras vermelhas de Bugs um pouco puxadas para a esquerda da posição central (x - largura/2).
    barras_bugs = ax.bar(x - largura/2, tempos_bugs, largura, label='Bugs', color='#e74c3c', edgecolor='black')
    
    # Desenha as barras azuis de Features um pouco puxadas para a direita da posição central (x + largura/2). Elas vão se encaixar perfeitamente lado a lado.
    barras_feat = ax.bar(x + largura/2, tempos_features, largura, label='Features', color='#3498db', edgecolor='black')

    ax.set_title("Foco da Equipe: Tempo Médio de Resolução (Bugs vs Features)", fontsize=14, pad=15)
    ax.set_ylabel("Tempo Médio de Resolução (em Dias)", fontsize=12)
    ax.set_xlabel("Repositórios Avaliados", fontsize=12)
    
    # Substitui as posições invisíveis (0, 1 e 2) pelos nomes bonitos das tecnologias.
    ax.set_xticks(x)
    ax.set_xticklabels(NOMES, fontsize=11)
    
    ax.legend(fontsize=11) # Liga a legenda colorida no canto para sabermos o que é o Vermelho e o que é o Azul.
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Manda escrever os valores no topo de ambas as barras.
    ax.bar_label(barras_bugs, fmt='%.1f', padding=3, fontweight='bold', fontsize=10)
    ax.bar_label(barras_feat, fmt='%.1f', padding=3, fontweight='bold', fontsize=10)
    
    ax.margins(y=0.15)
    plt.tight_layout()
    plt.savefig("graficos/grafico_07_bugs_vs_features.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G7: {e}")

print("✅ Todos os 9 gráficos foram desenhados e salvos com sucesso na pasta 'graficos'!")