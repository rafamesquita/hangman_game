from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

palavra_secreta = ""
letras_certas = []
letras_erradas = []
tentativas = 6

jogador1_ws = None
jogador2_ws = None
jogador3_ws = None

jogador1_nome = None
jogador2_nome = None
jogador3_nome = None

@app.get("/jogador1", response_class=HTMLResponse)
async def jogador1(request: Request):
    return templates.TemplateResponse("jogador1.html", {"request": request})

@app.get("/jogador2", response_class=HTMLResponse)
async def jogador2(request: Request):
    return templates.TemplateResponse("jogador2.html", {"request": request})

@app.get("/jogador3", response_class=HTMLResponse)
async def jogador3(request: Request):
    return templates.TemplateResponse("jogador3.html", {"request": request})

@app.websocket("/ws/jogador1")
async def websocket_jogador1(ws: WebSocket):
    global palavra_secreta, letras_certas, letras_erradas, tentativas, jogador1_ws, jogador1_nome
    await ws.accept()
    jogador1_ws = ws 
    try:
        while True:
            data = await ws.receive_json()
            
            if data["type"] == "nome":
                nome = data["nome"]
                if nome_ja_em_uso(nome):
                    await ws.send_json({"type": "error", "msg": "Nome já está em uso, escolha outro."})
                    await ws.close()
                    break
                else:
                    global jogador1_nome
                    jogador1_nome = nome
                    await enviar_lista_jogadores()
                    if palavra_secreta:
                        await ws.send_json({"type": "inicio"})
                        await ws.send_json({
                            "type": "jogo",
                            "letras_certas": "".join(letras_certas),
                            "letras_erradas": "".join(letras_erradas),
                            "tentativas": tentativas,
                            "status": "continua",
                            "palavra": palavra_secreta
                        })
                    continue
            
            if data["type"] == "palavra":
                resetar_jogo()
                palavra_secreta = data["palavra"].lower() 
                letras_certas = ["_" for _ in palavra_secreta] 
                letras_erradas = []
                tentativas = 6
                for jogador_ws in [jogador2_ws, jogador3_ws]:
                    if jogador_ws:
                        await jogador_ws.send_json({"type": "inicio"})

    except:
        jogador1_ws = None
        nome = jogador1_nome or "Jogador1"
        jogador1_nome = None
        await enviar_lista_jogadores()

@app.websocket("/ws/jogador2")
async def websocket_jogador2(ws: WebSocket):
    global jogador2_ws, jogador2_nome
    await ws.accept()
    jogador2_ws = ws
    try:
        while True:
            data = await ws.receive_json() 
            
            if data["type"] == "nome":
                nome = data["nome"]
                if nome_ja_em_uso(nome):
                    await ws.send_json({"type": "error", "msg": "Nome já está em uso, escolha outro."})
                    await ws.close()
                    break
                else:
                    global jogador2_nome
                    jogador2_nome = nome
                    await enviar_lista_jogadores()
                    if palavra_secreta:
                        await ws.send_json({"type": "inicio"})
                        await ws.send_json({
                            "type": "jogo",
                            "letras_certas": "".join(letras_certas),
                            "letras_erradas": "".join(letras_erradas),
                            "tentativas": tentativas,
                            "status": "continua",
                            "palavra": palavra_secreta
                        })
                    continue
            
            if data["type"] == "letra":
                await processar_letra(data["letra"].lower(), jogador="jogador2") # Processa a letra recebida
    except:
        jogador2_ws = None
        nome = jogador2_nome or "Jogador2"
        jogador2_nome = None
        await enviar_lista_jogadores()

@app.websocket("/ws/jogador3")
async def websocket_jogador3(ws: WebSocket):
    global jogador3_ws, jogador3_nome
    await ws.accept()
    jogador3_ws = ws
    try:
        while True:
            data = await ws.receive_json()
            
            if data["type"] == "nome":
                nome = data["nome"]
                if nome_ja_em_uso(nome):
                    await ws.send_json({"type": "error", "msg": "Nome já está em uso, escolha outro."})
                    await ws.close()
                    break
                else:
                    global jogador3_nome
                    jogador3_nome = nome
                    await enviar_lista_jogadores()
                    if palavra_secreta:
                        await ws.send_json({"type": "inicio"})
                        await ws.send_json({
                            "type": "jogo",
                            "letras_certas": "".join(letras_certas),
                            "letras_erradas": "".join(letras_erradas),
                            "tentativas": tentativas,
                            "status": "continua",
                            "palavra": palavra_secreta
                        })
                    continue
            
            if data["type"] == "letra":
                await processar_letra(data["letra"].lower(), jogador="jogador3")
    except:
        jogador3_ws = None
        nome = jogador3_nome or "Jogador3"
        jogador3_nome = None
        await enviar_lista_jogadores()
        
async def processar_letra(letra: str, jogador: str):
    global tentativas, letras_certas, letras_erradas
    
    if "_" not in letras_certas or tentativas <= 0:
        return

    ganhou = False
    perdeu = False

    if letra in palavra_secreta:
        for i, l in enumerate(palavra_secreta):
            if l == letra:
                letras_certas[i] = letra
    else:
        if letra not in letras_erradas:
            letras_erradas.append(letra)
            tentativas -= 1

    if "_" not in letras_certas:
        ganhou = True
    elif tentativas <= 0:
        perdeu = True
        
    if ganhou or perdeu:
        status = f"{jogador}_ganhou" if ganhou else "empate"
    else:
        status = "continua"
        
    if ganhou or perdeu:
        status = f"{jogador}_ganhou" if ganhou else "empate"
        msg = {
            "type": "jogo",
            "letras_certas": "".join(letras_certas),
            "letras_erradas": "".join(letras_erradas),
            "tentativas": tentativas,
            "status": status,
            "palavra": palavra_secreta
        }       
          
        for jogador_ws in [jogador1_ws, jogador2_ws, jogador3_ws]:
            if jogador_ws:
                await jogador_ws.send_json(msg)
        return

    msg = {
        "type": "jogo",
        "letras_certas": "".join(letras_certas),
        "letras_erradas": "".join(letras_erradas),
        "tentativas": tentativas,
        "status": status,
        "palavra": palavra_secreta
    }

    for jogador_ws in [jogador1_ws, jogador2_ws, jogador3_ws]:
        if jogador_ws:
            await jogador_ws.send_json(msg)
            
def nome_ja_em_uso(nome: str) -> bool:
    nomes_atuais = [jogador1_nome, jogador2_nome, jogador3_nome]
    return nome in nomes_atuais
   
async def enviar_lista_jogadores():
    nomes = [n for n in [jogador1_nome, jogador2_nome, jogador3_nome] if n]
    msg = {
        "type": "jogadores",
        "lista": nomes
    }
    for ws in [jogador1_ws, jogador2_ws, jogador3_ws]:
        if ws:
            try:
                await ws.send_json(msg)
            except:
                pass

def resetar_jogo():
    global palavra_secreta, letras_certas, letras_erradas, tentativas
    palavra_secreta = ""
    letras_certas = []
    letras_erradas = []
    tentativas = 6