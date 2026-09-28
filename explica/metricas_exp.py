import pandas as pd # Importa o Pandas (apelidado de pd) para ler, filtrar e fazer cálculos em tabelas de dados.
import matplotlib.pyplot as plt # Importa o módulo de desenho de gráficos para criar a tela, eixos e linhas.
import numpy as np # Importa o NumPy, usado aqui para gerar sequências numéricas (como âncoras no eixo X do Gráfico 7).
import os # Importa funções do sistema operacional para lidar com pastas e arquivos do seu computador.

# Cria uma pasta chamada "graficos". O 'exist_ok=True' impede que o programa trave e dê erro se a pasta já existir.
os.makedirs("graficos", exist_ok=True)

# Variáveis de configuração: guardam as siglas dos arquivos CSV
PROJETOS = ['flask', 'renpy', 'love']
# Dicionário guardando as cores exatas (em código hexadecimal) para padronizar as barras de cada projeto
CORES = {'flask': '#4C72B0', 'renpy': '#DD8452', 'love': '#55A868'}
# Lista com os nomes amigáveis que aparecerão nos títulos para evitar repetição de texto
NOMES = ['Flask (Base)', 'RenPy', 'Love2D']

# ==========================================
# GRÁFICO 1: Bus Factor
# ==========================================
try: # Inicia um bloco de segurança. Tenta executar o código abaixo; se der erro, pula para o 'except'.
    bf_valores = [] # Cria uma lista vazia para guardar os resultados do cálculo de cada projeto.
    for p in PROJETOS: # Inicia um laço de repetição (loop) que vai iterar por flask, renpy e love.
        df = pd.read_csv(f"{p}_contrib.csv") # Lê o arquivo .csv do disco e o transforma numa tabela virtual (DataFrame).
        total = df['contributions'].sum() # Soma toda a coluna 'contributions' para saber o total histórico de commits.
        top3 = df.nlargest(3, 'contributions')['contributions'].sum() # Pega os 3 maiores contribuidores e soma os commits deles.
        bf_valores.append((top3 / total) * 100) # Calcula a porcentagem dos top 3 em relação ao total e adiciona na lista.

    fig, ax = plt.subplots(figsize=(10, 6)) # Cria a tela de desenho (fig) com 10x6 polegadas e o quadrado do gráfico (ax).
    barras = ax.bar(NOMES, bf_valores, color=[CORES[p] for p in PROJETOS], edgecolor='black') # Desenha barras verticais com as cores definidas e borda preta.
    ax.set_title("Métrica de Risco: Bus Factor (Top 3 Contribuidores)\nMenor % indica maior distribuição de conhecimento", fontsize=14, pad=15) # Define o título do gráfico.
    
    ax.set_ylabel("Percentual de Contribuição (%)", fontsize=12) # Escreve a legenda do eixo Y (vertical).
    ax.set_xlabel("Repositórios Avaliados", fontsize=12) # Escreve a legenda do eixo X (horizontal).
    
    ax.bar_label(barras, fmt='%.1f%%', padding=3, fontweight='bold', fontsize=11) # Lê a altura de cada barra e posiciona o número (ex: 45.2%) no topo.
    ax.margins(y=0.15) # Adiciona 15% de espaço em branco no teto do gráfico para o número não ser cortado pela borda superior.
    plt.tight_layout() # Ajusta as margens internas automaticamente para que nenhum texto fique espremido para fora da imagem.
    plt.savefig("graficos/grafico_01_bus_factor.png", dpi=300) # Salva a imagem em alta resolução (300 dpi) dentro da pasta "graficos".
    plt.close() # Apaga a memória da tela para que o próximo gráfico comece com um quadro em branco.
except Exception as e: print(f"Erro G1: {e}") # Se algo falhar (ex: arquivo não encontrado), imprime o erro no terminal sem fechar o programa.

# ==========================================
# GRÁFICO 2: Tempo de Resolução de PRs
# ==========================================
try: # Bloco de segurança para o Gráfico 2.
    tempo_prs = [] # Lista para guardar as médias de tempo de cada projeto.
    for p in PROJETOS: # Passa por cada projeto novamente.
        df = pd.read_csv(f"{p}_prs.csv") # Carrega o arquivo de Pull Requests.
        df = df.dropna(subset=['fechado_em']) # Remove da tabela qualquer PR que ainda esteja aberto (sem data de fechamento).
        df['criado_em'] = pd.to_datetime(df['criado_em']) # Converte o texto da data de criação para um objeto de tempo compreensível pelo Python.
        df['fechado_em'] = pd.to_datetime(df['fechado_em']) # Converte o texto da data de fechamento para um objeto de tempo.
        df['tempo_dias'] = (df['fechado_em'] - df['criado_em']).dt.total_seconds() / 86400 # Subtrai as datas, extrai o total de segundos e divide por 86400 (segundos contidos em um dia).
        tempo_prs.append(df['tempo_dias'].mean()) # Calcula a média matemática de todos os PRs desse projeto e adiciona na lista.

    fig, ax = plt.subplots(figsize=(10, 6)) # Cria a tela de desenho de 10x6 polegadas.
    barras = ax.barh(NOMES, tempo_prs, color=[CORES[p] for p in PROJETOS], edgecolor='black') # Desenha barras horizontais ('barh' em vez de 'bar').
    ax.set_title("Cadência de Engenharia: Tempo Médio de Resolução de PRs", fontsize=14, pad=15) # Título do gráfico.
    
    ax.set_xlabel("Tempo Médio de Resolução (em Dias)", fontsize=12) # Legenda do eixo X.
    ax.set_ylabel("Repositórios Avaliados", fontsize=12) # Legenda do eixo Y.
    ax.grid(axis='x', linestyle='--', alpha=0.5) # Adiciona linhas de grade tracejadas no fundo, apenas no eixo X, com 50% de transparência.

    ax.bar_label(barras, fmt='%.1f dias', padding=5, fontweight='bold', fontsize=11) # Posiciona os rótulos automáticos à direita de cada barra horizontal.
    ax.margins(x=0.2) # Adiciona 20% de espaço em branco à direita para o texto não colidir com o limite da imagem.
    plt.tight_layout() # Ajusta as margens perfeitamente.
    plt.savefig("graficos/grafico_02_cadencia_prs.png", dpi=300) # Salva a imagem.
    plt.close() # Limpa a tela de desenho da memória.
except Exception as e: print(f"Erro G2: {e}")

# ==========================================
# GRÁFICO 3: Densidade de Discussão
# ==========================================
try:
    densidade_prs = [] # Lista para guardar a média de comentários.
    for p in PROJETOS:
        df = pd.read_csv(f"{p}_prs.csv") # Carrega a tabela de PRs.
        densidade_prs.append(df['comentarios'].mean()) # Calcula a média matemática isolada da coluna de comentários e armazena o valor.

    fig, ax = plt.subplots(figsize=(10, 6)) # Cria a área de desenho.
    barras = ax.bar(NOMES, densidade_prs, color=[CORES[p] for p in PROJETOS], edgecolor='black') # Desenha o gráfico de barras verticais padrão.
    ax.set_title("Atrito de Processo: Comentários Médios por Pull Request", fontsize=14, pad=15) # Título.
    
    ax.set_ylabel("Quantidade Média de Comentários", fontsize=12) # Legenda Y.
    ax.set_xlabel("Repositórios Avaliados", fontsize=12) # Legenda X.
    ax.grid(axis='y', linestyle='--', alpha=0.5) # Grade tracejada de fundo no eixo Y.

    ax.bar_label(barras, fmt='%.1f', padding=3, fontweight='bold', fontsize=11) # Rótulo fixado no topo das barras flutuantes, exibindo uma casa decimal.
    ax.margins(y=0.15) # Adiciona margem de respiro no topo de 15%.
    plt.tight_layout() # Empacota toda a moldura para exportação.
    plt.savefig("graficos/grafico_03_atrito_comentarios.png", dpi=300) # Salva o arquivo PNG.
    plt.close() # Libera a memória alocada.
except Exception as e: print(f"Erro G3: {e}")

# ==========================================
# GRÁFICO 4: Distribuição de Horários (CORRIGIDO)
# ==========================================
try:
    # Cria uma janela (fig) gigante (18x6) contendo 1 linha e 3 colunas de painéis menores (axes).
    # sharey=True faz com que todos os 3 painéis dividam a mesma escala vertical absoluta, para a comparação visual ser justa.
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    
    axes[0].set_ylabel("Volume Total de Commits", fontsize=12) # Coloca a legenda do eixo Y apenas no primeiro gráfico à esquerda.
    
    for i, p in enumerate(PROJETOS): # O 'enumerate' rastreia o índice numérico (0=flask, 1=renpy, 2=love) para desenhar no eixo correspondente.
        if os.path.exists(f"{p}_datas_git.csv"): # Verifica se o arquivo extraído do histórico local do Git existe antes de manipulá-lo.
            df = pd.read_csv(f"{p}_datas_git.csv") # Abre a tabela local de submissões.
            df['data'] = pd.to_datetime(df['data_str'], utc=True) # Converte as datas brutas textuais em referências exatas de fuso horário universal (UTC).
            df['hora'] = df['data'].dt.hour # Extrai cirurgicamente apenas o bloco numérico da hora (0 a 23) da referência temporal gerada.
            
            # Conta a incidência de commits para cada hora, ordena essa matriz de 0h a 23h, e desenha o gráfico interno direcionando-o para a posição correta (ax=axes[i]).
            ax_plot = df['hora'].value_counts().sort_index().plot(kind='bar', ax=axes[i], color=CORES[p], edgecolor='black')
            axes[i].set_title(NOMES[i], fontsize=14) # Define o título do subgráfico utilizando o nome comercial mapeado.
            axes[i].set_xlabel("Hora do Dia (0h - 23h, Fuso UTC)", fontsize=11) # Legenda do eixo X independente para cada um dos 3 painéis.
            
            axes[i].tick_params(axis='x', rotation=0) # Garante que as numerações horárias (0, 1, 2...) fiquem renderizadas de forma legível na horizontal base.
            
            for container in ax_plot.containers: # Intercepta o modelo de dados nativo de plotagem automatizada executada pelo objeto Pandas.
                # Insere individualmente os totais de ocorrência rotacionando em 90 graus (verticalmente) prevenindo que a densidade provoque a fusão visual dos números adjacentes.
                axes[i].bar_label(container, padding=4, fontsize=9, rotation=90, fontweight='bold')
            
            axes[i].margins(y=0.30) # Aumenta maciçamente a margem de teto para acomodar o volume longitudinal do rótulo rotacionado.

    plt.suptitle("Cultura de Trabalho: Distribuição de Horários de Commit", fontsize=16, fontweight='bold') # Fixa um rótulo mestre dominando o contorno de todos os painéis internos.
    plt.tight_layout() # Alinha tudo geometricamente.
    plt.savefig("graficos/grafico_04_horarios.png", dpi=300) # Persiste o arranjo triplo.
    plt.close() # Libera os objetos.
except Exception as e: print(f"Erro G4: {e}")

# ==========================================
# GRÁFICO 5: Hotspots de Dívida Técnica
# ==========================================
for p, nome_legivel in zip(PROJETOS, NOMES): # Laço híbrido que une a sigla ('flask') com seu nome amigável ('Flask (Base)') para gerar 3 painéis totalmente distintos no disco rígido.
    try:
        if os.path.exists(f"{p}_hotspots_git.csv"): # Valida a existência do mapeamento estrutural local.
            df_hotspots = pd.read_csv(f"{p}_hotspots_git.csv") # Carrega a estrutura listando milhares de acessos aos documentos primários.
            top_files = df_hotspots['arquivo'].value_counts().head(5) # Realiza uma tabulação de contagem bruta e suprime o resultado, fatiando apenas os 5 maiores volumes de incidência.

            fig, ax = plt.subplots(figsize=(10, 5)) # Constrói o contexto em branco 10x5.
            top_files.plot(kind='barh', ax=ax, color=CORES[p], edgecolor='black') # Chama a renderização matricial automática do Pandas configurando para o modo de linhas horizontais.
            ax.set_title(f"Gargalos de Arquitetura: Os 5 Arquivos Mais Alterados ({nome_legivel})", fontsize=13, pad=15) # Customiza um título concatenando a nomenclatura do laço atual de iteração.
            
            ax.set_xlabel("Frequência de Modificações (Quantidade de Commits)", fontsize=12) # Identifica a dimensão horizontal de volume.
            ax.set_ylabel("Nome do Arquivo (Caminho)", fontsize=12) # Identifica a dimensão vertical de texto.
            ax.invert_yaxis() # Inverte esteticamente a matriz visual nativa forçando o item de maior métrica escalar para a prateleira superior.
            
            for container in ax.containers: # Rastreia as demarcações dimensionais instanciadas.
                ax.bar_label(container, padding=5, fontweight='bold', fontsize=10) # Aloca a notação do dígito integral pontuando o final linear do vetor visual.
                
            ax.margins(x=0.15) # Acrescenta respiro direito contendo quebras indesejadas na imagem gerada.
            plt.tight_layout() # Empacota o vetor de visualização.
            plt.savefig(f"graficos/grafico_05_hotspots_{p}.png", dpi=300) # Exporta o resultado sob o nome restrito à variável da sigla injetada dinamicamente, gerando imagens independentes.
            plt.close() # Finaliza instância para não transbordar lixo para a próxima rodada do laço FOR.
    except Exception as e: print(f"Erro G5 ({p}): {e}")

# ==========================================
# GRÁFICO 6: Taxa de Sucesso (Merge Rate)
# ==========================================
try:
    taxa_merge = [] # Bloco alocado para matriz simples de incidência percentual.
    for p in PROJETOS:
        df = pd.read_csv(f"{p}_prs.csv") # Extrai a estrutura tabular dos pull requests isolados de cada engine.
        total_prs = len(df) # Aplica a função de medição de tamanho bruto em linhas da estrutura.
        aceitos = df['merge_feito'].sum() # Valida os campos da propriedade indicadora 'True' em binário onde sum() avalia 'True' como (1). O montante representa todos os PRs de sucesso real.
        taxa_merge.append((aceitos / total_prs) * 100 if total_prs > 0 else 0) # Efetua o raciocínio matemático clássico para formulação de probabilidade %. Inseriu-se um sistema 'IF' para imunização de travamento sobre divisões base em 0 (ZERO).

    fig, ax = plt.subplots(figsize=(10, 6)) # Prepara geometria da figura base em formato paisagem (10 polegadas).
    barras = ax.bar(NOMES, taxa_merge, color=[CORES[p] for p in PROJETOS], edgecolor='black') # Atrela lista indexada de strings com valores isolados na geometria.
    ax.set_title("Taxa de Sucesso de PRs (Merge Rate)", fontsize=14, pad=15) # Intitula quadro com distanciamento inferior pad(15).
    
    ax.set_ylabel("Taxa de Aceitação (%)", fontsize=12) # Demarca dimensão vetorial vertical (Y).
    ax.set_xlabel("Repositórios Avaliados", fontsize=12) # Demarca dimensão referencial analítica (X).
    
    ax.bar_label(barras, fmt='%.1f%%', padding=3, fontweight='bold', fontsize=11) # Configura a função auto-posicionadora fixando limitador em flutuação até (1) decima formatada estrita ao símbolo visual (%).
    ax.margins(y=0.15) # Reforça topo visando contenção numérico visual.
    plt.tight_layout() # Alinha preenchimento do canva principal limitando áreas desnecessárias.
    plt.savefig("graficos/grafico_06_merge_rate.png", dpi=300) # Salva a projeção binária da matriz em estrutura pixelada externa para a apresentação de slides.
    plt.close() # Mata thread remanescente garantindo descarregamento absoluto da memória.
except Exception as e: print(f"Erro G6: {e}")

# ==========================================
# GRÁFICO 7: Resolução por Categoria (Bugs vs Features)
# ==========================================
try:
    tempos_bugs = [] # Acumulador vetorial isolando médias globais identificadas especificamente em falhas e gargalos no software.
    tempos_features = [] # Acumulador restritivo para médias inerentes à novas aquisições tecnológicas solicitadas e fechadas via repositório.

    for p in PROJETOS:
        df = pd.read_csv(f"{p}_issues.csv") # Inicializa a leitura primária de todo o sistema unificado Issue e rastreado no pipeline da ferramenta corretora da API.
        df = df.dropna(subset=['fechado_em']) # Impede distorções no log expurgando todas as discussões cujo ticket continue operacional ou travado por falta de alinhamento com a comunidade de manutenabilidade.
        df['criado_em'] = pd.to_datetime(df['criado_em']) # Traduz estrutura String crua isolada por padronização global.
        df['fechado_em'] = pd.to_datetime(df['fechado_em']) # Traduz registro limite temporal (fim da vida).
        df['tempo_dias'] = (df['fechado_em'] - df['criado_em']).dt.total_seconds() / 86400 # Diminuição padrão entre as variáveis para conversão sequencial para representação visual por (dia da terra/ 86400s).
        
        df_bugs = df[df['categoria'] == 'bug'] # Dissecação da estrutura tabular original limitando integralmente a matriz espelho isolada portando unicamente ocorrências nominais a 'bug' derivadas do parse na coleta.
        df_features = df[df['categoria'] == 'feature'] # Executa ação espelho análoga à decodificação referenciando somente incidências vetoriais 'feature'.
        
        # Conduz cálculo de média simples da subtabela. O sistema '.empty' instaura resguardo operacional que proíbe travamento originário da devolução tipográfica falha do numpy referenciado a matriz sem qualquer incidência vetorial de tipo em particular. Força retorno '0'.
        media_bug = df_bugs['tempo_dias'].mean() if not df_bugs.empty else 0
        media_feature = df_features['tempo_dias'].mean() if not df_features.empty else 0
        
        # Efetua enfileiramento das equações lineares resultantes na lista final de ancoragem visual. Notna() impossibilita o carregamento de estruturas vazias em decorrência do bug original.
        tempos_bugs.append(media_bug if pd.notna(media_bug) else 0)
        tempos_features.append(media_feature if pd.notna(media_feature) else 0)

    x = np.arange(len(PROJETOS)) # Implementa no motor matemático um array numérico subjacente invisível [0, 1, 2] cuja função é instanciar coordenadas bases unicamente referenciais fixas na extensão horizontal.
    largura = 0.35 # Fixa espessura da malha da barra estática visando compatibilizar fisicamente a co-alocação simétrica de dois blocos em cada slot fixo sem atrito mútuo.

    fig, ax = plt.subplots(figsize=(10, 6)) # Configura chassi principal da geometria subjacente.
    
    # Engenharia matriz paralela de colunas (Barra 1 e 2):
    # O motor deduz pela ancoragem 0 referida acima que a metade do recuo definido o posiciona no hemisfério da extrema esquerda (-). Configura-se sua identidade visual atrelada a "bugs" formatada no tom Hex Vermelho intenso de alerta corporativo.
    barras_bugs = ax.bar(x - largura/2, tempos_bugs, largura, label='Bugs', color='#e74c3c', edgecolor='black')
    
    # Realiza-se procedimento matemático espelhado no pólo diametralmente frontal da coordenada referencial em que operava seu par, avançando o bloco para o lado oposto (+) no tom Azul frio atrelado às matrizes vetoriais de Features.
    barras_feat = ax.bar(x + largura/2, tempos_features, largura, label='Features', color='#3498db', edgecolor='black')

    ax.set_title("Foco da Equipe: Tempo Médio de Resolução (Bugs vs Features)", fontsize=14, pad=15) # Implanta Título Descritivo com respiro formatado esteticamente baseando-se no preenchimento de (15) graus polimorfos para o teto do layout principal de fundo da moldura.
    
    ax.set_ylabel("Tempo Médio de Resolução (em Dias)", fontsize=12) # Posiciona eixo dependente temporal.
    ax.set_xlabel("Repositórios Avaliados", fontsize=12) # Posiciona matriz fixa principal de repositórios base (flask/renpy/love).
    
    ax.set_xticks(x) # Define que as demarcações do layout principal na horizontal serão baseadas fixamente unicamente nos números originados do array invisível instanciado (0, 1 e 2).
    ax.set_xticklabels(NOMES, fontsize=11) # Engloba o array e o encobre por intermédio das nomenclaturas strings da matriz de configuração principal (flask, renpy, etc) ao invés da tipografia crua [0,1,2].
    ax.legend(fontsize=11) # Solicita habilitação orgânica do sistema visual para agrupar identificadores label em bloco único com mapeamento cromático no quadrante primário exposto.
    ax.grid(axis='y', linestyle='--', alpha=0.5) # Efetua o tracionamento limitador horizontal no plano em Y da prancheta gráfica gerando linhas discretas.

    # Implanta nos painéis de barra as referências tabulares e assegura independência nas ancoragens evitando que as medições estáticas fiquem flutuando em dissonância vetorial gerando artefatos falhos pelo atrito nos dois blocos paralelos independentemente escaláveis por dimensões assimétricas matemáticas distintas de processamento.
    ax.bar_label(barras_bugs, fmt='%.1f', padding=3, fontweight='bold', fontsize=10)
    ax.bar_label(barras_feat, fmt='%.1f', padding=3, fontweight='bold', fontsize=10)
    
    ax.margins(y=0.15) # Eleva cota restritiva do teto de dimensionamento de fundo e encerra a colisão perimetral no topo das numerações do rótulo independente limitador referencial.
    plt.tight_layout() # Traciona blocos adjacentes e encerra vazios nas pranchetas de fundo e contornos indesejados nas bordas do limite fotográfico da prancheta gráfica para salvar em bitmap para apresentação executiva.
    plt.savefig("graficos/grafico_07_bugs_vs_features.png", dpi=300) # Salva a varredura das malhas com resolução elevada e finaliza a execução.
    plt.close() # Encerra motor visual.
except Exception as e: print(f"Erro G7: {e}")

print("Todos os gráficos foram otimizados e salvos!")