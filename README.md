# Análise de Saúde e Manutenibilidade de Repositórios de Software

Este projeto implementa uma esteira automatizada de extração e análise de dados focada em avaliar a estabilidade técnica, o engajamento comunitário e a qualidade processual de repositórios open-source. 

O escopo da análise foi desenhado para avaliar comparativamente os motores de jogos 2D **Ren'Py** e **Love2D**, estabelecendo a robustez operacional do micro-framework **Flask** como infraestrutura de base (baseline).

## Metodologia e Funcionalidades

O pipeline é composto por duas frentes de processamento que geram as métricas exigidas para análises de adoção tecnológica corporativa:
1. **Mineração em Nuvem (API GitHub):** Avalia Pull Requests, Issues e Contribuidores para derivar métricas de processo e comunicação.
2. **Mineração Local (Git History):** Processa o versionamento profundo via subprocessos locais para mapeamento de hotspots estruturais e padrões comportamentais de *commits*.

### Métricas Analisadas
* **Índice de Concentração (Bus Factor):** Identificação de gargalos de pessoal.
* **Cadência de Resolução de PRs:** Velocidade do pipeline de integração e testes.
* **Densidade de Discussão:** Mapeamento de atrito burocrático e clareza de requisitos.
* **Cultura de Trabalho (Distribuição Temporal):** Detecção de trabalho corporativo vs. voluntariado madrugador.
* **Hotspots Arquiteturais:** Identificação da dívida técnica nos repositórios locais.
* **Merge Rate:** Taxa percentual de receptividade da comunidade.
* **Foco da Equipe (Bugs vs. Features):** Avaliação preditiva do esforço de engenharia.

## 📂 Estrutura do Projeto

Após a execução, o ambiente do projeto será organizado da seguinte forma:

```text
/
├── extracao.py                 # Script para mineração via API e Git local
├── metricas.py                 # Script para processamento offline (Pandas/Matplotlib)
├── README.md                   # Documentação
├── flask/                      # Repositório clonado (Base)
├── renpy/                      # Repositório clonado (Avaliação A)
├── love/                       # Repositório clonado (Avaliação B)
├── dados/                      # Data Lake local gerado dinamicamente
│   ├── flask/                  # CSVs isolados do Flask
│   ├── renpy/                  # CSVs isolados do Ren'Py
│   └── love/                   # CSVs isolados do Love2D
└── graficos/                   # Painéis analíticos (Imagens em .PNG)
