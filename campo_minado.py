
import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Configurações 

DIFICULDADES = {
    "facil": {
        "linhas": 9,
        "colunas": 9,
        "minas": 10
    },

    "medio": {
        "linhas": 16,
        "colunas": 16,
        "minas": 40
    },

    "dificil": {
        "linhas": 16,
        "colunas": 30,
        "minas": 99
    }
}

LINHAS = DIFICULDADES["facil"]["linhas"]
COLUNAS = DIFICULDADES["facil"]["colunas"]
MINAS = DIFICULDADES["facil"]["minas"]

DIFICULDADE_ATUAL = "facil"

ARQUIVO_RECORDES = "recordes.json"

tabela_minas = []
tabela_numeros = []
tabela_estado = []

botoes = []

janela = None

jogo_acabou = False
casas_abertas = 0
minas_sorteadas = False


# Criar as tabelas 

# Cria as três tabelas vazias para armazenar as informações do jogo.
def criar_tabuleiro():

    global tabela_minas, tabela_numeros, tabela_estado
    global jogo_acabou, casas_abertas, minas_sorteadas

    tabela_minas = [[False] * COLUNAS for _ in range(LINHAS)]

    tabela_numeros = [[0] * COLUNAS for _ in range(LINHAS)]

    tabela_estado = [["fechada"] * COLUNAS for _ in range(LINHAS)]

    jogo_acabou = False
    casas_abertas = 0
    minas_sorteadas = False


# Sortear as minas 

# Sorteia as minas sem colocar nenhuma na primeira casa clicada.
def sortear_minas(linha_segura, coluna_segura):

    global minas_sorteadas

    todas_as_casas = []

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):

            if (linha, coluna) != (linha_segura, coluna_segura):
                todas_as_casas.append((linha, coluna))

    casas_com_mina = random.sample(todas_as_casas, MINAS)

    for linha, coluna in casas_com_mina:
        tabela_minas[linha][coluna] = True

    minas_sorteadas = True

    calcular_numeros()


# Contar minas vizinhas 

# Conta quantas minas existem nas oito casas ao redor.
def contar_minas_vizinhas(linha, coluna):

    quantidade = 0

    for deslocamento_linha in [-1, 0, 1]:
        for deslocamento_coluna in [-1, 0, 1]:

            if deslocamento_linha == 0 and deslocamento_coluna == 0:
                continue

            nova_linha = linha + deslocamento_linha
            nova_coluna = coluna + deslocamento_coluna

            if (0 <= nova_linha < LINHAS and
                0 <= nova_coluna < COLUNAS):

                if tabela_minas[nova_linha][nova_coluna]:
                    quantidade += 1

    return quantidade


# Calcula e preenche os números de minas vizinhas em cada casa.
def calcular_numeros():

    global tabela_numeros

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):

            if not tabela_minas[linha][coluna]:

                tabela_numeros[linha][coluna] = contar_minas_vizinhas(
                    linha, coluna
                )

# Criar tela do campo minado

# Cria a janela do jogo e os botões que representa as casa
def criar_tela_jogo():

    global janela, botoes

    janela = tk.Tk()
    janela.title("Campo Minado")

    botoes = []

    for linha in range(LINHAS):

        linha_de_botoes = []

        for coluna in range(COLUNAS):

            botao = tk.Button(
                janela,
                width=3,
                height=1,
                text="",
                bg="#d9d9d9",
                command=lambda l=linha, c=coluna: abrir_casa(l, c)
            )

            botao.grid(row=linha, column=coluna)

            linha_de_botoes.append(botao)

        botoes.append(linha_de_botoes)


# Abrir uma casa 

# Abre a casa clicada e mostra se há uma mina ou um número.
def abrir_casa(linha, coluna):

    global jogo_acabou, casas_abertas

    if jogo_acabou:
        return

    if tabela_estado[linha][coluna] == "aberta":
        return

    # Sorteia as minas somente no primeiro clique.
    if not minas_sorteadas:
        sortear_minas(linha, coluna)

    tabela_estado[linha][coluna] = "aberta"

    # Verifica se a casa possui uma mina.
    if tabela_minas[linha][coluna]:

        botoes[linha][coluna].config(
            text="💣",
            bg="red",
            state="disabled"
        )

        verificar_fim_de_jogo(linha, coluna)

        return

    # Mostra o número de minas vizinhas.
    quantidade = tabela_numeros[linha][coluna]

    texto = str(quantidade) if quantidade > 0 else ""

    botoes[linha][coluna].config(
        text=texto,
        relief=tk.SUNKEN,
        state="disabled",
        bg="lightgray"
    )

    casas_abertas += 1

    verificar_fim_de_jogo(linha, coluna)


# Verificar fim do jogo 

# Verifica se o jogador perdeu ou ganhou.
def verificar_fim_de_jogo(linha, coluna):

    global jogo_acabou

    # Verifica se o jogador encontrou uma mina.
    if tabela_minas[linha][coluna]:

        jogo_acabou = True

        # Mostra todas as minas do tabuleiro.
        for l in range(LINHAS):
            for c in range(COLUNAS):

                if tabela_minas[l][c]:
                    botoes[l][c].config(
                        text="💣",
                        bg="red",
                        state="disabled"
                    )

        messagebox.showinfo("Fim de jogo", "Você perdeu!")

    # Verifica se o jogador ganhou.
    elif casas_abertas == LINHAS * COLUNAS - MINAS:

        jogo_acabou = True

        messagebox.showinfo("Fim de jogo", "Você ganhou!")


# Reiniciar o jogo 

# Limpa as tabelas e prepara uma nova partida.
def reiniciar_jogo():

    global botoes

    criar_tabuleiro()

    # Volta todos os botões ao estado inicial.
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):

            botoes[linha][coluna].config(
                text="",
                state="normal",
                relief=tk.RAISED,
                bg="#d9d9d9"
            )


# Salvar os recordes 

# Salva o melhor tempo de cada dificuldade em um arquivo.
def salvar_recorde(dificuldade, tempo):

    if dificuldade not in DIFICULDADES:
        return False

    if tempo < 0:
        return False

    recordes = {
        "facil": None,
        "medio": None,
        "dificil": None
    }

    # Verifica se o arquivo já existe.
    if os.path.exists(ARQUIVO_RECORDES):

        try:
            with open(ARQUIVO_RECORDES, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if isinstance(dados, dict):
                for nivel in recordes:
                    recordes[nivel] = dados.get(nivel)

        except (json.JSONDecodeError, OSError):
            pass

    # Salva somente se for um novo recorde.
    recorde_atual = recordes[dificuldade]

    if recorde_atual is None or tempo < recorde_atual:

        recordes[dificuldade] = tempo

        try:
            with open(ARQUIVO_RECORDES, "w", encoding="utf-8") as arquivo:
                json.dump(
                    recordes,
                    arquivo,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except OSError:
            return False

    return False


# Executar o jogo 

criar_tabuleiro()
criar_tela_jogo()

janela.mainloop()
