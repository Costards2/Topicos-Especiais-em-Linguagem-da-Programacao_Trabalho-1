import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("graficos", exist_ok=True)

PROJETOS = ['flask', 'renpy', 'love']
CORES = {'flask': '#4C72B0', 'renpy': '#DD8452', 'love': '#55A868'}
NOMES = ['Flask (Base)', 'RenPy', 'Love2D']

# ==========================================
# GRÁFICO 1: Bus Factor
# ==========================================
try:
    bf_valores = []
    for p in PROJETOS:
        df = pd.read_csv(f"{p}_contrib.csv")
        total = df['contributions'].sum()
        top3 = df.nlargest(3, 'contributions')['contributions'].sum()
        bf_valores.append((top3 / total) * 100)

    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(NOMES, bf_valores, color=[CORES[p] for p in PROJETOS], edgecolor='black')
    ax.set_title("Métrica de Risco: Bus Factor (Top 3 Contribuidores)\nMenor % indica maior distribuição de conhecimento", fontsize=14, pad=15)
    
    # Rótulos Eixos X e Y claros
    ax.set_ylabel("Percentual de Contribuição (%)", fontsize=12)
    ax.set_xlabel("Repositórios Avaliados", fontsize=12)
    
    ax.bar_label(barras, fmt='%.1f%%', padding=3, fontweight='bold', fontsize=11)
    ax.margins(y=0.15)
    plt.tight_layout()
    plt.savefig("graficos/grafico_01_bus_factor.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G1: {e}")

# ==========================================
# GRÁFICO 2: Tempo de Resolução de PRs
# ==========================================
try:
    tempo_prs = []
    for p in PROJETOS:
        df = pd.read_csv(f"{p}_prs.csv")
        df = df.dropna(subset=['fechado_em'])
        df['criado_em'] = pd.to_datetime(df['criado_em'])
        df['fechado_em'] = pd.to_datetime(df['fechado_em'])
        df['tempo_dias'] = (df['fechado_em'] - df['criado_em']).dt.total_seconds() / 86400
        tempo_prs.append(df['tempo_dias'].mean())

    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.barh(NOMES, tempo_prs, color=[CORES[p] for p in PROJETOS], edgecolor='black')
    ax.set_title("Cadência de Engenharia: Tempo Médio de Resolução de PRs", fontsize=14, pad=15)
    
    ax.set_xlabel("Tempo Médio de Resolução (em Dias)", fontsize=12)
    ax.set_ylabel("Repositórios Avaliados", fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    ax.bar_label(barras, fmt='%.1f dias', padding=5, fontweight='bold', fontsize=11)
    ax.margins(x=0.2)
    plt.tight_layout()
    plt.savefig("graficos/grafico_02_cadencia_prs.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G2: {e}")

# ==========================================
# GRÁFICO 3: Densidade de Discussão
# ==========================================
try:
    densidade_prs = []
    for p in PROJETOS:
        df = pd.read_csv(f"{p}_prs.csv")
        densidade_prs.append(df['comentarios'].mean())

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
# GRÁFICO 4: Distribuição de Horários (CORRIGIDO)
# ==========================================
try:
    # Aumentei a largura da figura (de 15 para 18) para dar mais espaço
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    
    # Eixo Y geral definido apenas no primeiro gráfico à esquerda
    axes[0].set_ylabel("Volume Total de Commits", fontsize=12)
    
    for i, p in enumerate(PROJETOS):
        if os.path.exists(f"{p}_datas_git.csv"):
            df = pd.read_csv(f"{p}_datas_git.csv")
            df['data'] = pd.to_datetime(df['data_str'], utc=True)
            df['hora'] = df['data'].dt.hour 
            
            ax_plot = df['hora'].value_counts().sort_index().plot(kind='bar', ax=axes[i], color=CORES[p], edgecolor='black')
            axes[i].set_title(NOMES[i], fontsize=14)
            axes[i].set_xlabel("Hora do Dia (0h - 23h, Fuso UTC)", fontsize=11)
            
            # Rotaciona os números do eixo X para ficarem deitados (horizontais)
            axes[i].tick_params(axis='x', rotation=0)
            
            for container in ax_plot.containers:
                # Rotaciona os rótulos de dados em 90 graus (verticais) para não sobrepor
                axes[i].bar_label(container, padding=4, fontsize=9, rotation=90, fontweight='bold')
            
            # Aumenta muito a margem superior para acomodar o texto vertical
            axes[i].margins(y=0.30)

    plt.suptitle("Cultura de Trabalho: Distribuição de Horários de Commit", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig("graficos/grafico_04_horarios.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G4: {e}")

# ==========================================
# GRÁFICO 5: Hotspots de Dívida Técnica
# ==========================================
for p, nome_legivel in zip(PROJETOS, NOMES):
    try:
        if os.path.exists(f"{p}_hotspots_git.csv"):
            df_hotspots = pd.read_csv(f"{p}_hotspots_git.csv")
            top_files = df_hotspots['arquivo'].value_counts().head(5)

            fig, ax = plt.subplots(figsize=(10, 5))
            top_files.plot(kind='barh', ax=ax, color=CORES[p], edgecolor='black')
            ax.set_title(f"Gargalos de Arquitetura: Os 5 Arquivos Mais Alterados ({nome_legivel})", fontsize=13, pad=15)
            
            ax.set_xlabel("Frequência de Modificações (Quantidade de Commits)", fontsize=12)
            ax.set_ylabel("Nome do Arquivo (Caminho)", fontsize=12)
            ax.invert_yaxis()
            
            for container in ax.containers:
                ax.bar_label(container, padding=5, fontweight='bold', fontsize=10)
                
            ax.margins(x=0.15)
            plt.tight_layout()
            plt.savefig(f"graficos/grafico_05_hotspots_{p}.png", dpi=300)
            plt.close()
    except Exception as e: print(f"Erro G5 ({p}): {e}")

# ==========================================
# GRÁFICO 6: Taxa de Sucesso (Merge Rate)
# ==========================================
try:
    taxa_merge = []
    for p in PROJETOS:
        df = pd.read_csv(f"{p}_prs.csv")
        total_prs = len(df)
        aceitos = df['merge_feito'].sum()
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
# GRÁFICO 7: Resolução por Categoria (Bugs vs Features)
# ==========================================
try:
    tempos_bugs = []
    tempos_features = []

    for p in PROJETOS:
        df = pd.read_csv(f"{p}_issues.csv")
        df = df.dropna(subset=['fechado_em'])
        df['criado_em'] = pd.to_datetime(df['criado_em'])
        df['fechado_em'] = pd.to_datetime(df['fechado_em'])
        df['tempo_dias'] = (df['fechado_em'] - df['criado_em']).dt.total_seconds() / 86400
        
        df_bugs = df[df['categoria'] == 'bug']
        df_features = df[df['categoria'] == 'feature']
        
        media_bug = df_bugs['tempo_dias'].mean() if not df_bugs.empty else 0
        media_feature = df_features['tempo_dias'].mean() if not df_features.empty else 0
        
        tempos_bugs.append(media_bug if pd.notna(media_bug) else 0)
        tempos_features.append(media_feature if pd.notna(media_feature) else 0)

    x = np.arange(len(PROJETOS))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    barras_bugs = ax.bar(x - largura/2, tempos_bugs, largura, label='Bugs', color='#e74c3c', edgecolor='black')
    barras_feat = ax.bar(x + largura/2, tempos_features, largura, label='Features', color='#3498db', edgecolor='black')

    ax.set_title("Foco da Equipe: Tempo Médio de Resolução (Bugs vs Features)", fontsize=14, pad=15)
    
    ax.set_ylabel("Tempo Médio de Resolução (em Dias)", fontsize=12)
    ax.set_xlabel("Repositórios Avaliados", fontsize=12)
    
    ax.set_xticks(x)
    ax.set_xticklabels(NOMES, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    ax.bar_label(barras_bugs, fmt='%.1f', padding=3, fontweight='bold', fontsize=10)
    ax.bar_label(barras_feat, fmt='%.1f', padding=3, fontweight='bold', fontsize=10)
    
    ax.margins(y=0.15)
    plt.tight_layout()
    plt.savefig("graficos/grafico_07_bugs_vs_features.png", dpi=300)
    plt.close()
except Exception as e: print(f"Erro G7: {e}")

print("Todos os gráficos foram otimizados e salvos!")




