# BIBLIOTECAS

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


print("Status:", resposta.status_code)


sopa = BeautifulSoup(resposta.text, "html.parser")


linhas = sopa.find_all("tr")


print("Linhas na tabela:", len(linhas))


for linha in linhas[:4]:

    celulas = [c.get_text(" ", strip=True) for c in linha.find_all(["td", "th"])]

    print(celulas)