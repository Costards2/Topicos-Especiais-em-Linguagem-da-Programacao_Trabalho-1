import os
import subprocess
import pandas as pd
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("Aviso: GITHUB_TOKEN não encontrado no ficheiro .env!")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

REPOSITORIOS = [
    {"owner": "pallets", "repo": "flask", "pasta": "./flask"},
    {"owner": "renpy", "repo": "renpy", "pasta": "./renpy"},
    {"owner": "love2d", "repo": "love", "pasta": "./love"},
]


def extrair_contribuidores(owner, repo, pasta_destino):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    resp = requests.get(url, headers=HEADERS, params={"per_page": 100})
    if resp.status_code == 200:
        pd.DataFrame(resp.json()).to_csv(
            f"{pasta_destino}/{repo}_contrib.csv", index=False
        )


def extrair_issues_e_prs(owner, repo, pasta_destino, limite=100):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    resp = requests.get(
        url, headers=HEADERS, params={"state": "all", "per_page": limite}
    )
    if resp.status_code != 200:
        print(f"Erro ao baixar PRs/Issues de {repo}: {resp.status_code}")
        return

    dados_prs, dados_issues = [], []
    for item in resp.json():
        comentarios = item.get("comments", 0)
        titulo = item.get("title", "").lower()
        labels = [l["name"].lower() for l in item.get("labels", [])]

        if "pull_request" in item:
            dados_prs.append(
                {
                    "repo": repo,
                    "criado_em": item["created_at"],
                    "fechado_em": item["closed_at"],
                    "comentarios": comentarios,
                    "merge_feito": item.get("pull_request", {}).get("merged_at")
                    is not None,
                }
            )
        else:
            categoria = "outros"
            if (
                any(p in titulo for p in ["bug", "fix", "error", "crash"])
                or "bug" in labels
            ):
                categoria = "bug"
            elif (
                any(p in titulo for p in ["add", "feature", "support"])
                or "enhancement" in labels
            ):
                categoria = "feature"

            dados_issues.append(
                {
                    "repo": repo,
                    "categoria": categoria,
                    "criado_em": item["created_at"],
                    "fechado_em": item["closed_at"],
                }
            )

    if dados_prs:
        pd.DataFrame(dados_prs).to_csv(
            f"{pasta_destino}/{repo}_prs.csv", index=False
        )
    if dados_issues:
        pd.DataFrame(dados_issues).to_csv(
            f"{pasta_destino}/{repo}_issues.csv", index=False
        )


def extrair_git_local(pasta_repo, repo_nome, pasta_destino):
    if not os.path.exists(pasta_repo):
        print(f"Aviso: Pasta '{pasta_repo}' não encontrada.")
        return

    comando = [
        "git",
        "-C",
        pasta_repo,
        "log",
        "--name-only",
        "--format=COMMIT|%ad",
        "--date=iso",
    ]
    resultado = subprocess.run(
        comando, stdout=subprocess.PIPE, text=True, errors="ignore"
    )

    datas, arquivos = [], []
    data_atual = None

    for linha in resultado.stdout.split("\n"):
        linha = linha.strip()
        if not linha:
            continue
        if linha.startswith("COMMIT|"):
            data_atual = linha.split("|")[1]
            datas.append({"repo": repo_nome, "data_str": data_atual})
        elif data_atual:
            arquivos.append({"repo": repo_nome, "arquivo": linha})

    pd.DataFrame(datas).to_csv(
        f"{pasta_destino}/{repo_nome}_datas_git.csv", index=False
    )
    pd.DataFrame(arquivos).to_csv(
        f"{pasta_destino}/{repo_nome}_hotspots_git.csv", index=False
    )


for p in REPOSITORIOS:
    print(f"[{p['repo']}] A extrair dados...")
    pasta_destino = f"dados/{p['repo']}"
    os.makedirs(pasta_destino, exist_ok=True)

    extrair_contribuidores(p["owner"], p["repo"], pasta_destino)
    extrair_issues_e_prs(p["owner"], p["repo"], pasta_destino)
    extrair_git_local(p["pasta"], p["repo"], pasta_destino)

print(
    "\nExtração concluída com sucesso! Ficheiros salvos na pasta 'dados/'."
)