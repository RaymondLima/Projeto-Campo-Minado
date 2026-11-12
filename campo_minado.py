
import tkinter as tk
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

janela = tk.Tk()
janela.title("Campo Minado")
janela.configure(bg="#2c3e50")

jogo_acabou = False
casas_abertas = 0
minas_sorteadas = False
bandeiras_colocadas = 0
rotulo_minas = None
segundos = 0
id_cronometro = None
rotulo_tempo = None


# Criar as tabelas 

# Cria as três tabelas vazias para armazenar as informações do jogo.
def criar_tabuleiro():

    global tabela_minas, tabela_numeros, tabela_estado
    global jogo_acabou, casas_abertas, minas_sorteadas
    global bandeiras_colocadas, segundos

    tabela_minas = [[False] * COLUNAS for _ in range(LINHAS)]

    tabela_numeros = [[0] * COLUNAS for _ in range(LINHAS)]

    tabela_estado = [["fechada"] * COLUNAS for _ in range(LINHAS)]

    jogo_acabou = False
    casas_abertas = 0
    minas_sorteadas = False
    bandeiras_colocadas = 0

    parar_cronometro()
    segundos = 0


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

    global botoes, rotulo_minas, rotulo_tempo

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

             # Clique direito coloca ou tira a bandeira.
            botao.bind(
                "<Button-3>",
                lambda evento, l=linha, c=coluna: alternar_bandeira(l, c)
            )

            linha_de_botoes.append(botao)

        botoes.append(linha_de_botoes)

    # Barra embaixo do tabuleiro com o contador de minas.
    barra = tk.Frame(janela, bg="#2c3e50")
    barra.grid(row=LINHAS, column=0, columnspan=COLUNAS, sticky="we")

    rotulo_minas = tk.Label(
        barra,
        text="",
        font=("Press Start 2P", 9),
        bg="#2c3e50",
        fg="#ecf0f1"
    )
    rotulo_minas.pack(side="left", padx=10, pady=8)
    rotulo_tempo = tk.Label(
        barra,
        text="",
        font=("Press Start 2P", 9),
        bg="#2c3e50",
        fg="#ecf0f1"
    )
    rotulo_tempo.pack(side="right", padx=10, pady=8)

    atualizar_contador()
    mostrar_tempo()


# Abrir uma casa 

# Abre a casa clicada e mostra se há uma mina ou um número.
def abrir_casa(linha, coluna):

    global jogo_acabou, casas_abertas

    if jogo_acabou:
        return

    # Não abre casa já aberta nem casa com bandeira.
    if tabela_estado[linha][coluna] in ("aberta", "bandeira"):
        return

    # Sorteia as minas somente no primeiro clique.
    if not minas_sorteadas:
        sortear_minas(linha, coluna)
        iniciar_cronometro()

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

    # Se a casa é vazia, abre as vizinhas sozinha.
    if quantidade == 0:
        abrir_vizinhas(linha, coluna)

    verificar_fim_de_jogo(linha, coluna)


# Abre sozinha as vizinhas de uma casa vazia (zero minas ao redor).
def abrir_vizinhas(linha, coluna):

    global casas_abertas

    for deslocamento_linha in [-1, 0, 1]:
        for deslocamento_coluna in [-1, 0, 1]:

            nova_linha = linha + deslocamento_linha
            nova_coluna = coluna + deslocamento_coluna

            # Para na borda do tabuleiro.
            if not (0 <= nova_linha < LINHAS and
                    0 <= nova_coluna < COLUNAS):
                continue

            # Para em casa já aberta ou com bandeira.
            if tabela_estado[nova_linha][nova_coluna] in ("aberta", "bandeira"):
                continue

            # Abre a vizinha.
            tabela_estado[nova_linha][nova_coluna] = "aberta"
            casas_abertas += 1

            quantidade = tabela_numeros[nova_linha][nova_coluna]

            texto = str(quantidade) if quantidade > 0 else ""

            botoes[nova_linha][nova_coluna].config(
                text=texto,
                relief=tk.SUNKEN,
                state="disabled",
                bg="lightgray"
            )

            # Só continua a onda se a vizinha também for vazia.
            if quantidade == 0:
                abrir_vizinhas(nova_linha, nova_coluna)

# Atualiza o texto que mostra quantas minas ainda faltam marcar.
def atualizar_contador():

    restantes = MINAS - bandeiras_colocadas

    rotulo_minas.config(text="Minas: " + str(restantes))


# Mostra o tempo na tela no formato 00:00.
def mostrar_tempo():

    minutos = segundos // 60
    seg = segundos % 60

    rotulo_tempo.config(text="Tempo: %02d:%02d" % (minutos, seg))


# Soma um segundo, atualiza a tela e agenda o próximo segundo.
def contar_segundo():

    global segundos, id_cronometro

    segundos += 1
    mostrar_tempo()

    id_cronometro = janela.after(1000, contar_segundo)


# Começa a contar o tempo (chamada no primeiro clique).
def iniciar_cronometro():

    global id_cronometro

    id_cronometro = janela.after(1000, contar_segundo)


# Para o cronômetro cancelando o próximo segundo agendado.
def parar_cronometro():

    global id_cronometro

    if id_cronometro is not None:
        janela.after_cancel(id_cronometro)
        id_cronometro = None


# Coloca ou tira a bandeira de uma casa fechada.
def alternar_bandeira(linha, coluna):

    global bandeiras_colocadas

    if jogo_acabou:
        return

    estado = tabela_estado[linha][coluna]

    # Casa aberta não recebe bandeira.
    if estado == "aberta":
        return

    if estado == "fechada":
        tabela_estado[linha][coluna] = "bandeira"
        botoes[linha][coluna].config(text="🚩")
        bandeiras_colocadas += 1

    elif estado == "bandeira":
        tabela_estado[linha][coluna] = "fechada"
        botoes[linha][coluna].config(text="")
        bandeiras_colocadas -= 1

    atualizar_contador()


# Verificar fim do jogo 

# Verifica se o jogador perdeu ou ganhou.
def verificar_fim_de_jogo(linha, coluna):

    global jogo_acabou

    # Verifica se o jogador encontrou uma mina.
    if tabela_minas[linha][coluna]:

        jogo_acabou = True
        parar_cronometro()

        # Mostra todas as minas do tabuleiro.
        for l in range(LINHAS):
            for c in range(COLUNAS):

                if tabela_minas[l][c]:
                    botoes[l][c].config(
                        text="💣",
                        bg="red",
                        state="disabled"
                    )

        # Espera um pouco para o jogador ver as minas e abre a tela de fim.
        janela.after(1200, lambda: mostrar_tela_fim(False))

    # Verifica se o jogador ganhou.
    elif casas_abertas == LINHAS * COLUNAS - MINAS:

        jogo_acabou = True
        parar_cronometro()

        janela.after(1200, lambda: mostrar_tela_fim(True))

# Converte segundos para o formato 00:00.
def formatar_tempo(total):
    return "%02d:%02d" % (total // 60, total % 60)


# Mostra a tela de fim de jogo com o resultado, o tempo e os botões.
def mostrar_tela_fim(venceu):

    limpar_janela()
    janela.geometry("500x400")

    frame = tk.Frame(janela, bg="#2c3e50")
    frame.pack(expand=True)

    if venceu:
        titulo = "VOCÊ GANHOU!"
        cor = "#2ecc71"
    else:
        titulo = "VOCÊ PERDEU!"
        cor = "#e74c3c"

    tk.Label(
        frame, text=titulo,
        font=("Press Start 2P", 18, "bold"),
        bg="#2c3e50", fg=cor
    ).pack(pady=(0, 20))

    tk.Label(
        frame, text="Tempo: " + formatar_tempo(segundos),
        font=("Press Start 2P", 10),
        bg="#2c3e50", fg="#ecf0f1"
    ).pack(pady=(0, 10))

    # Só guarda o tempo se o jogador ganhou.
    if venceu:
        novo_recorde = salvar_recorde(DIFICULDADE_ATUAL, segundos)

        if novo_recorde:
            tk.Label(
                frame, text="NOVO RECORDE!",
                font=("Press Start 2P", 10),
                bg="#2c3e50", fg="#f1c40f"
            ).pack(pady=(0, 10))

    criar_botao(frame, "JOGAR DE NOVO", iniciar_partida)
    criar_botao(frame, "VOLTAR AO MENU", mostrar_menu)


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
            atualizar_contador()
            mostrar_tempo()


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

# Apaga tudo o que está na janela (usada ao trocar de tela).
def limpar_janela():
    parar_cronometro()

    for widget in janela.winfo_children():
        widget.destroy()


# Cria um botão arcade estilizado dentro do frame recebido.
def criar_botao(frame, texto, comando):
    btn = tk.Button(
        frame,
        text=texto,
        command=comando,
        font=("Press Start 2P", 9),
        width=18,
        height=2,
        bg="#34495e",
        fg="#ffffff",
        activebackground="#e74c3c",
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        cursor="hand2",
    )

    # Efeito hover ao passar o mouse.
    btn.bind("<Enter>", lambda e: btn.config(bg="#3b5998"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#34495e"))

    btn.pack(pady=10)
    return btn


# Mostra a tela de menu com os botões de dificuldade.
def mostrar_menu():
    limpar_janela()
    janela.geometry("500x400")

    main_frame = tk.Frame(janela, bg="#2c3e50")
    main_frame.pack(expand=True)

    tk.Label(
        main_frame, text="CAMPO",
        font=("Press Start 2P", 24, "bold"),
        bg="#2c3e50", fg="#ecf0f1"
    ).pack(pady=(0, 5))

    tk.Label(
        main_frame, text="MINADO",
        font=("Press Start 2P", 24, "bold"),
        bg="#2c3e50", fg="#e74c3c"
    ).pack(pady=(0, 30))

    criar_botao(main_frame, "FÁCIL", lambda: escolher_nivel("facil"))
    criar_botao(main_frame, "MÉDIO", lambda: escolher_nivel("medio"))
    criar_botao(main_frame, "DIFÍCIL", lambda: escolher_nivel("dificil"))


# Guarda o tamanho do tabuleiro e as minas da dificuldade escolhida.
def escolher_nivel(nome):
    global LINHAS, COLUNAS, MINAS, DIFICULDADE_ATUAL

    DIFICULDADE_ATUAL = nome
    LINHAS = DIFICULDADES[nome]["linhas"]
    COLUNAS = DIFICULDADES[nome]["colunas"]
    MINAS = DIFICULDADES[nome]["minas"]

    iniciar_partida()


# Limpa a janela e começa uma partida nova.
def iniciar_partida():
    limpar_janela()
    janela.geometry("")  # deixa a janela se ajustar ao tamanho do tabuleiro
    criar_tabuleiro()
    criar_tela_jogo()

mostrar_menu()

janela.mainloop()
