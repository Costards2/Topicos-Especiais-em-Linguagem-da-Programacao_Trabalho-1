# Análise de Saúde e Manutenibilidade de Repositórios de Software

Este projeto implementa um pipeline de engenharia de dados focado na avaliação da estabilidade técnica, engajamento comunitário e maturidade de engenharia de software em repositórios open-source.

A análise realiza um diagnóstico comparativo dos motores de jogo 2D **Ren'Py** e **Love2D**, utilizando a infraestrutura do micro-framework **Flask** como linha de base (*baseline*).

---

## 📂 Estrutura do Repositório

```text
.
├── .env                        # Variáveis de ambiente (Token do GitHub)
├── .gitignore                  # Ficheiros ignorados pelo Git
├── extracao.py                 # Script de extração de dados (API + Git)
├── metricas.py                 # Script de geração dos painéis analíticos
├── dados/                      # Data Lake local (CSV) organizado por projeto
│   ├── flask/                  # Dados extraídos do Flask
│   ├── love/                   # Dados extraídos do Love2D
│   └── renpy/                  # Dados extraídos do Ren'Py
├── explica/                    # Documentação explicativa do projeto
│   ├── extracao_exp.py         # Script de extração comentado detalhadamente
│   ├── formulas.md             # Explicação das fórmulas e metodologia
│   └── metricas_exp.py         # Script de visualização comentado detalhadamente
├── flask/                      # Repositório clonado (Base)
├── graficos/                   # Visualizações PNG geradas (300 DPI)
├── love/                       # Repositório clonado (Motor 2D)
├── renpy/                      # Repositório clonado (Motor 2D)
└── venv/                       # Ambiente virtual Python
