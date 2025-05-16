# 🪓 Hangman Game

An interactive project developed with **HTML**, **CSS** and **Python (FastAPI)** that simulates the classic **Hangman game**, with dynamic visual updates after each attempt.

---

## 📸 Features

- Simple and responsive web interface for two players.
- Real-time communication between players via WebSocket.
- Visual update of the hangman based on incorrect guesses.
- Secret word handling and letter validation.
- Dynamic SVG drawing of the hangman.
- Victory or defeat messages with the revealed word.

---

## 🧠 Technologies Used

- 💻 **HTML5** – Interface structure.
- 🎨 **CSS3** – Visual styling of the game.
- 🐍 **Python + FastAPI** –  Server logic and WebSocket handling.
- 🖼️ **SVG** – Real-time graphical drawing of the hangman.

---

## 🚀 How to Use

1. **Clone the repository:**
   git clone https://github.com/rafamesquita/hangman_game
   cd forca-fastapi/

2. **Install Python dependencies (FastAPI and Uvicorn):**
   pip install fastapi uvicorn

3. **Run the server locally:**
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

4. **Find your machine’s IP address:**
   - Windows: ipconfig
   - Linux/macOS: ifconfig

5. **Access the game from two different browsers or devices using your machine’s IP:**
   - http://<seu-ip>:8000/jogador1
   - http://<seu-ip>:8000/jogador2

---

# 🪓 Jogo da Forca

Um projeto interativo desenvolvido com **HTML**, **CSS** e **Python (FastAPI)** que simula o clássico **jogo da forca**, com atualizações visuais dinâmicas a cada tentativa.

---

## 📸 Funcionalidades

- Interface web simples e responsiva para dois jogadores.
- Comunicação em tempo real entre os jogadores via WebSocket.
- Atualização visual da forca com base nas tentativas erradas.
- Palavras secretas e validação de letras.
- Desenho da forca em SVG dinâmico.
- Mensagens de vitória ou derrota com a palavra revelada.

---

## 🧠 Tecnologias Utilizadas

- 💻 **HTML5** – Estrutura da interface.
- 🎨 **CSS3** – Estilização visual do jogo.
- 🐍 **Python + FastAPI** – Lógica do servidor e WebSocket.
- 🖼️ **SVG** – Desenho gráfico da forca em tempo real.

---

## 🚀 Como Usar

1. **Clone o repositório:**
   git clone https://github.com/rafamesquita/hangman_game
   cd forca-fastapi/

2. **Instale as dependências do Python (FastAPI e Uvicorn):**
   pip install fastapi uvicorn

3. **Execute o servidor localmente:**
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

4. **Descubra o IP da sua máquina:**
   - Windows: ipconfig
   - Linux/macOS: ifconfig

5. **Acesse o jogo em dois navegadores diferentes ou dispositivos, utilizando o IP da sua máquina:**
   - http://<seu-ip>:8000/jogador1
   - http://<seu-ip>:8000/jogador2