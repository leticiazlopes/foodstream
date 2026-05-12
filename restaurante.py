import json
import time   
from biblioteca import Biblioteca

app = Biblioteca()

def enviar_log(msg):
    print(f"[RESTAURANTE] {msg}")


enviar_log("Enviando promoção do dia...")
app.publicar("ofertas/diaria", json.dumps({
    "promo": "Borda recheada grátis hoje!",
    "valido_ate": "23:59"
}))


topico_pedido = "pedido/123"
status_sequencia = ["RECEBIDO", "PREPARANDO", "PRONTO"]

for status in status_sequencia:
    enviar_log(f"Atualizando pedido para: {status}")
    app.publicar(topico_pedido, json.dumps({
        "status": status, 
        "item": "Calabresa",
        "horario": time.strftime("%H:%M:%S")
    }))
    
    
    
    time.sleep(1) 
    
    
    while True:
        notificacao = app.receber_notificacao()
        if not notificacao:
            break
            
        if notificacao.operacao == "erro":
            print(f"⚠️  AVISO DO BROKER: {notificacao.mensagem}")
        else:
            print(f"📩 Resposta recebida: {notificacao.mensagem}")

enviar_log("Fluxo finalizado.")