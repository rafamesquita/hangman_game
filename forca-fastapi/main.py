# Importações
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Inicialização da aplicação
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Variáveis globais do jogo
jogador1_ws = None
palavra_secreta = ""

jogador2_ws = None
letras_certas_jogador2 = []
letras_erradas_jogador2 = []
tentativas_jogador2 = 6

jogador3_ws = None
letras_certas_jogador3 = []
letras_erradas_jogador3 = []
tentativas_jogador3 = 6

jogador_turno = "jogador2"

# Rota para jogador 1
@app.get("/jogador1", response_class=HTMLResponse)
async def jogador1(request: Request):
    return templates.TemplateResponse("jogador1.html", {"request": request})

# Rota para jogador 2
@app.get("/jogador2", response_class=HTMLResponse)
async def jogador2(request: Request):
    return templates.TemplateResponse("jogador2.html", {"request": request})

# Rota para jogador 3
@app.get("/jogador3", response_class=HTMLResponse)
async def jogador3(request: Request):
    return templates.TemplateResponse("jogador3.html", {"request": request})

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
                jogador_turno = "jogador2"

                letras_certas_jogador2 = ["_" for _ in palavra_secreta] # Inicializa o jogo (reseta as variáveis)
                letras_erradas_jogador2 = []
                tentativas_jogador2 = 6

                letras_certas_jogador3 = ["_" for _ in palavra_secreta]
                letras_erradas_jogador3 = []
                tentativas_jogador3 = 6

                inicio_msg = {
                "type": "inicio",
                "letras_certas_jogador2": "".join(letras_certas_jogador2),
                "letras_erradas_jogador2": "".join(letras_erradas_jogador2),
                "letras_certas_jogador3": "".join(letras_certas_jogador3),
                "letras_erradas_jogador3": "".join(letras_erradas_jogador3),
                "tentativas_jogador2": tentativas_jogador2,
                "tentativas_jogador3": tentativas_jogador3,
                "turno": jogador_turno,
                "status": "continua",
                "palavra": palavra_secreta
            }

            if jogador2_ws:
                await jogador2_ws.send_json(inicio_msg)
            if jogador3_ws:
                await jogador3_ws.send_json(inicio_msg)
    except:
        jogador1_ws = None

@app.websocket("/ws/jogador2")
async def websocket_jogador2(ws: WebSocket):
    global jogador2_ws
    await ws.accept()
    jogador2_ws = ws
    try:
        while True:
            data = await ws.receive_json() # Recebe uma letra do jogador 2
            if data["type"] == "letra" and jogador_turno == "jogador2":
                letra = data["letra"].lower()
                resultado = "continua"
                if letra in palavra_secreta: # Se a letra estiver na palavra: Atualiza letras_certas com a letra nas posições corretas.
                    for i, l in enumerate(palavra_secreta):
                        if l == letra:
                            letras_certas_jogador2[i] = letra
                else: # Se não estiver: Adiciona a letra em letras_erradas (se ainda não estiver lá). Decrementa tentativas
                    if letra not in letras_erradas_jogador2:
                        letras_erradas_jogador2.append(letra)
                        global tentativas_jogador2
                        tentativas_jogador2 -= 1

                vencedor = None

                if "_" not in letras_certas_jogador2:
                    resultado = "ganhou"
                    vencedor = jogador_turno  # quem adivinhou corretamente
                    jogador_turno = "jogador2"  # reinicia para próxima partida
                elif tentativas_jogador2 <= 0:
                    resultado = "perdeu"
                    vencedor = "nenhum"  # ou None, indicando derrota
                    jogador_turno = "jogador2"
                else:
                    jogador_turno = "jogador3" if jogador_turno == "jogador2" else "jogador2"


                msg = {
                    "type": "jogo",
                    "letras_certas_jogador2": "".join(letras_certas_jogador2),
                    "letras_erradas_jogador2": "".join(letras_erradas_jogador2),
                    "letras_certas_jogador3": "".join(letras_certas_jogador3),
                    "letras_erradas_jogador3": "".join(letras_erradas_jogador3),
                    "tentativas_jogador2": tentativas_jogador2,
                    "tentativas_jogador3": tentativas_jogador3,
                    "status": resultado,
                    "palavra": palavra_secreta,
                    "turno": jogador_turno,
                    "vencedor": vencedor
                }
                # Envia para todos os jogadores
                if jogador1_ws:
                    await jogador1_ws.send_json(msg)
                if jogador2_ws:
                    await jogador2_ws.send_json(msg)
                if jogador3_ws:
                    await jogador3_ws.send_json(msg)
    except:
        jogador2_ws = None

@app.websocket("/ws/jogador3")
async def websocket_jogador3(ws: WebSocket):
    global jogador3_ws
    await ws.accept()
    jogador3_ws = ws
    try:
        while True:
            data = await ws.receive_json()
            if data["type"] == "letra" and jogador_turno == "jogador3":
                letra = data["letra"].lower()
                resultado = "continua"
                if letra in palavra_secreta: # Se a letra estiver na palavra: Atualiza letras_certas com a letra nas posições corretas.
                    for i, l in enumerate(palavra_secreta):
                        if l == letra:
                            letras_certas_jogador3[i] = letra
                else: # Se não estiver: Adiciona a letra em letras_erradas (se ainda não estiver lá). Decrementa tentativas
                    if letra not in letras_erradas_jogador3:
                        letras_erradas_jogador3.append(letra)
                        global tentativas_jogador3
                        tentativas_jogador3 -= 1

                vencedor = None

                if "_" not in letras_certas_jogador3:
                    resultado = "ganhou"
                    vencedor = jogador_turno  # quem adivinhou corretamente
                    jogador_turno = "jogador2"  # reinicia para próxima partida
                elif tentativas_jogador3 <= 0:
                    resultado = "perdeu"
                    vencedor = "nenhum"  # ou None, indicando derrota
                    jogador_turno = "jogador2"
                else:
                    jogador_turno = "jogador3" if jogador_turno == "jogador2" else "jogador2"


                msg = {
                    "type": "jogo",
                    "letras_certas_jogador2": "".join(letras_certas_jogador2),
                    "letras_erradas_jogador2": "".join(letras_erradas_jogador2),
                    "letras_certas_jogador3": "".join(letras_certas_jogador3),
                    "letras_erradas_jogador3": "".join(letras_erradas_jogador3),
                    "tentativas_jogador2": tentativas_jogador2,
                    "tentativas_jogador3": tentativas_jogador3,
                    "status": resultado,
                    "palavra": palavra_secreta,
                    "turno": jogador_turno,
                    "vencedor": vencedor
                }
                # Envia para todos os jogadores
                if jogador1_ws:
                    await jogador1_ws.send_json(msg)
                if jogador2_ws:
                    await jogador2_ws.send_json(msg)
                if jogador3_ws:
                    await jogador3_ws.send_json(msg)
    except:
        jogador3_ws = None