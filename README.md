
# 💣 Campo Minado

Um jogo de **Campo Minado desenvolvido em Python**, com interface gráfica criada utilizando Tkinter. O projeto possui três níveis de dificuldade, cronômetro, sistema de bandeiras e armazenamento de recordes pessoais. Também utiliza Web Scraping para coletar os melhores tempos disponíveis em um ranking online e comparar o desempenho do jogador.

## 🎮 Funcionalidades

- **Três níveis de dificuldade:** Fácil, Médio e Difícil.
- **Tabuleiro interativo:** permite abrir as casas utilizando o botão esquerdo do mouse.
- **Sistema de bandeiras:** permite marcar e desmarcar possíveis minas utilizando o botão direito do mouse.
- **Primeira jogada segura:** as minas são sorteadas somente após o primeiro clique, garantindo que a primeira casa não contenha uma mina.
- **Abertura automática:** casas vazias abrem automaticamente suas vizinhas.
- **Cronômetro:** registra o tempo de cada partida.
- **Recordes pessoais:** armazena os melhores tempos do jogador em cada dificuldade.
- **Web Scraping:** coleta os melhores tempos dos rankings online do Minesweeper.now.
- **Comparação de recordes:** compara o tempo do jogador com o melhor tempo encontrado na internet.
- **Tela de resultados:** apresenta o resultado da partida, o tempo e as informações dos recordes.
- **Reinício de partida:** permite jogar novamente ou voltar ao menu principal.

## 🛠️ Tecnologias e bibliotecas utilizadas

- **Python:** linguagem de programação utilizada no desenvolvimento.
- **Tkinter:** criação da interface gráfica do jogo.
- **Random:** sorteio aleatório das posições das minas.
- **JSON:** armazenamento e leitura dos recordes.
- **OS:** verificação da existência de arquivos.
- **Threading:** execução da coleta de recordes em segundo plano.
- **Requests:** realização de requisições HTTP para acessar os rankings.
- **BeautifulSoup:** extração e organização de informações das páginas HTML por meio de Web Scraping.

## 📂 Estrutura do projeto

```text
Projeto-Campo-Minado/
│
├── .venv/
│
├── campo_minado.py
├── teste_site.py
├── README.md
├── requirements.txt
├── recordes_internet.json
├── recordes.json
└── .gitignore
```

### Descrição dos arquivos

- `campo_minado.py`: contém o código principal, a lógica do jogo, a interface gráfica e o sistema de recordes.
- `teste_site.py`: utilizado para testar a conexão com o site e a extração de informações por Web Scraping.
- `README.md`: documentação e apresentação do projeto.
- `requirements.txt`: lista as bibliotecas externas necessárias para executar o projeto.
- `recordes_internet.json`: armazena os melhores tempos coletados dos rankings online.
- `recordes.json`: armazena os melhores tempos pessoais do jogador. É criado quando um novo recorde pessoal é salvo.
- `.venv/`: ambiente virtual utilizado para isolar as dependências do projeto.
- `.gitignore`: define quais arquivos e pastas não devem ser enviados ao GitHub.

## ⚙️ Instalação e execução

**1. Clone o repositório:**

```bash
git clone URL_DO_REPOSITORIO
```

**2. Entre na pasta do projeto:**

```bash
cd Projeto-Campo-Minado
```

**3. Crie um ambiente virtual:**

```bash
python -m venv .venv
```

**4. Ative o ambiente virtual no Windows:**

```powershell
.venv\Scripts\Activate
```

**5. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**6. Execute o jogo:**

```bash
python campo_minado.py
```

## 📦 Dependências

As bibliotecas externas utilizadas estão listadas no arquivo `requirements.txt`:

```text
requests
beautifulsoup4
```

As demais bibliotecas utilizadas pertencem à biblioteca padrão do Python.

## 🌐 Web Scraping

O projeto utiliza Web Scraping para consultar os rankings disponíveis no site [Minesweeper.now](https://minesweeper.now/).

A coleta é realizada em três páginas, correspondentes aos níveis de dificuldade:

- **Beginner:** Fácil.
- **Intermediate:** Médio.
- **Expert:** Difícil.

Utilizando Requests, o programa acessa as páginas e, com BeautifulSoup, analisa o HTML para extrair os tempos registrados no ranking.

Após a coleta, os melhores tempos são armazenados no arquivo `recordes_internet.json` e utilizados para comparar o desempenho do jogador.

A coleta acontece em segundo plano, evitando que a interface do jogo fique bloqueada durante esse processo.

### Arquivos de recordes

O projeto utiliza dois arquivos JSON para armazenar os resultados:

- **recordes_internet.json:** guarda os melhores tempos coletados dos rankings online.
- **recordes.json:** guarda os melhores tempos pessoais do jogador em cada dificuldade.

## 🎯 Objetivo do projeto

Desenvolver um jogo funcional de Campo Minado, aplicando conceitos de lógica de programação, estruturas de dados, funções, interface gráfica, manipulação de arquivos, requisições HTTP, Web Scraping e execução de tarefas em paralelo.

O projeto também busca integrar conhecimentos de programação Python em uma aplicação interativa, com armazenamento e comparação de resultados.

