# Importações
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Inicialização da aplicação
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Variáveis globais do jogo
palavra_secreta = ""
letras_certas = []
letras_erradas = []
tentativas = 6
jogador1_ws = None
jogador2_ws = None

# Rota para jogador 1
@app.get("/jogador1", response_class=HTMLResponse)
async def jogador1(request: Request):
    return templates.TemplateResponse("jogador1.html", {"request": request})

# Rota para jogador 2
@app.get("/jogador2", response_class=HTMLResponse)
async def jogador2(request: Request):
    return templates.TemplateResponse("jogador2.html", {"request": request})

# WebSocket do jogador 1
@app.websocket("/ws/jogador1")
async def websocket_jogador1(ws: WebSocket):
    global palavra_secreta, letras_certas, letras_erradas, tentativas, jogador1_ws
    await ws.accept() # Aceita a conexão WebSocket
    jogador1_ws = ws # Armazena a conexão
    try:
        while True:
            data = await ws.receive_json() # Espera por uma mensagem JSON
            if data["type"] == "palavra":
                palavra_secreta = data["palavra"].lower() # Salva a palavra secreta em minúsculas
                letras_certas = ["_" for _ in palavra_secreta] # Inicializa o jogo (reseta as variáveis)
                letras_erradas = []
                tentativas = 6
                if jogador2_ws:
                    await jogador2_ws.send_json({"type": "inicio"}) # Envia um sinal para o jogador 2 que o jogo começou
    except:
        jogador1_ws = None

# WebSocket do jogador 2
@app.websocket("/ws/jogador2")
async def websocket_jogador2(ws: WebSocket):
    global jogador2_ws
    await ws.accept()
    jogador2_ws = ws
    try:
        while True:
            data = await ws.receive_json() # Recebe uma letra do jogador 2
            if data["type"] == "letra":
                letra = data["letra"].lower()
                resultado = "continua"
                if letra in palavra_secreta: # Se a letra estiver na palavra: Atualiza letras_certas com a letra nas posições corretas.
                    for i, l in enumerate(palavra_secreta):
                        if l == letra:
                            letras_certas[i] = letra
                else: # Se não estiver: Adiciona a letra em letras_erradas (se ainda não estiver lá). Decrementa tentativas
                    if letra not in letras_erradas:
                        letras_erradas.append(letra)
                        global tentativas
                        tentativas -= 1

                if "_" not in letras_certas: # Verifica o status do jogo
                    resultado = "ganhou"
                elif tentativas <= 0:
                    resultado = "perdeu"

                # Envia a atualização para os dois jogadores
                msg = {
                    "type": "jogo",
                    "letras_certas": "".join(letras_certas),
                    "letras_erradas": "".join(letras_erradas),
                    "tentativas": tentativas,
                    "status": resultado,
                    "palavra": palavra_secreta
                }
                if jogador2_ws:
                    await jogador2_ws.send_json(msg)
                if jogador1_ws:
                    await jogador1_ws.send_json(msg)
    except:
        jogador2_ws = None
