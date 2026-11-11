import tkinter as tk
from tkinter import messagebox
import random

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

tabela_minas = []
tabela_numeros = []
tabela_estado = []

botoes = []

janela = None

jogo_acabou = False
casas_abertas = 0


# Cria o tabuleiro e distribui as minas aleatoriamente.
def criar_tabuleiro():

    global tabela_minas, tabela_numeros, tabela_estado
    global jogo_acabou, casas_abertas

    tabela_minas = [[False] * COLUNAS for _ in range(LINHAS)]

    tabela_numeros = [[0] * COLUNAS for _ in range(LINHAS)]

    tabela_estado = [["fechada"] * COLUNAS for _ in range(LINHAS)]

    jogo_acabou = False
    casas_abertas = 0

    todas_as_casas = []

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            todas_as_casas.append((linha, coluna))

    casas_com_mina = random.sample(todas_as_casas, MINAS)

    for linha, coluna in casas_com_mina:
        tabela_minas[linha][coluna] = True


# Conta quantas minas existem ao redor de uma casa.
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
    """Preenche a tabela com a quantidade de minas vizinhas."""

    global tabela_numeros

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):

            tabela_numeros[linha][coluna] = contar_minas_vizinhas(
                linha, coluna
            )


# ---------- Passo 2: Criar tela do jogo ----------

# Cria a janela do jogo e os botões que representam cada casa.
def criar_tela_jogo():
    """Abre a janela e coloca um botão para cada casa."""

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
                command=lambda l=linha, c=coluna: abrir_casa(l, c)
            )

            botao.grid(row=linha, column=coluna)

            linha_de_botoes.append(botao)

        botoes.append(linha_de_botoes)


# ---------- Passo 4: Abrir uma casa ----------

# Abre a casa clicada e mostra se há uma mina ou um número.
def abrir_casa(linha, coluna):

    global jogo_acabou, casas_abertas

    if jogo_acabou:
        return

    if tabela_estado[linha][coluna] == "aberta":
        return

    tabela_estado[linha][coluna] = "aberta"

    # Verifica se a casa possui uma mina
    if tabela_minas[linha][coluna]:

        botoes[linha][coluna].config(
            text="💣",
            bg="red",
            state="disabled"
        )

        verificar_fim_de_jogo(linha, coluna)

        return

    # Mostra o número de minas vizinhas
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


# ---------- Passo 5: Verificar fim de jogo ----------

# Verifica se o jogador perdeu ao encontrar uma mina ou ganhou ao abrir todas as casas sem minas.
def verificar_fim_de_jogo(linha, coluna):

    global jogo_acabou

    # Verifica se o jogador encontrou uma mina
    if tabela_minas[linha][coluna]:

        jogo_acabou = True

        # Mostra todas as minas do tabuleiro
        for l in range(LINHAS):
            for c in range(COLUNAS):

                if tabela_minas[l][c]:
                    botoes[l][c].config(
                        text="💣",
                        bg="red"
                    )

        messagebox.showinfo("Fim de jogo", "Você perdeu!")

    # Verifica se o jogador ganhou
    elif casas_abertas == LINHAS * COLUNAS - MINAS:

        jogo_acabou = True

        messagebox.showinfo("Fim de jogo", "Você ganhou!")


# ---------- Executar o jogo ----------

criar_tabuleiro()
calcular_numeros()
criar_tela_jogo()

janela.mainloop()