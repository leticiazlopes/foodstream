from biblioteca import Biblioteca
import time
import json

app = Biblioteca()
topico = "ofertas/diaria"


app.inscrever(topico)

print("="*45)
print(f" 📢  FOODSTREAM - PAINEL DE PROMOÇÕES ")
print(f" 📍  Monitorando: {topico}")
print(f" 📡  Conectado ao Broker de Marketing")
print("="*45)
print("Aguardando ofertas imperdíveis...\n")

try:
    while True:
        notificacao = app.receber_notificacao()
        
        if notificacao:
            
            try:
                dados = json.loads(notificacao.mensagem)
                promo = dados.get("promo", notificacao.mensagem)
                validade = dados.get("valido_ate", "Hoje")
            except:
                promo = notificacao.mensagem
                validade = "Não informada"

            
            print("┌" + "─"*43 + "┐")
            print(f"│ 🔥 OFERTA RELÂMPAGO!                      │")
            print(f"│                                           │")
            print(f"│ 🍕 {promo[:35].ljust(35)} │")
            print(f"│ ⏰ Válido até: {validade.ljust(26)} │")
            print("└" + "─"*43 + "┘")
            print("  (Aproveite no nosso App!)\n")

        time.sleep(0.5) 
except KeyboardInterrupt:
    app.cancelar_inscricao("ofertas/diaria")
    print("\n[INFO] Painel de ofertas encerrado.")