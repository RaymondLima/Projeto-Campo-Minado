# ==============================================================
# BIBLIOTECAS
# ==============================================================

# Importa as bibliotecas usadas pelo jogo.
import requests
from bs4 import BeautifulSoup


# Define o endereço da página de ranking do Campo Minado.
URL = "https://minesweeper.now/ranking/beginner"


# Acessa a página e armazena a resposta do servidor.
resposta = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0 (trabalho da faculdade)"},
    timeout=10
)


# Exibe o código de status da requisição.
print("Status:", resposta.status_code)


# Analisa o HTML da página para permitir a extração dos dados.
sopa = BeautifulSoup(resposta.text, "html.parser")


# Localiza todas as linhas das tabelas presentes na página.
linhas = sopa.find_all("tr")


# Exibe a quantidade de linhas encontradas na tabela.
print("Linhas na tabela:", len(linhas))


# Percorre as quatro primeiras linhas da tabela.
for linha in linhas[:4]:

    # Extrai e organiza os textos das células de cada linha.
    celulas = [c.get_text(" ", strip=True) for c in linha.find_all(["td", "th"])]

    # Exibe os dados extraídos de cada linha.
    print(celulas)