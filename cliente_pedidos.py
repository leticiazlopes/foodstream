from biblioteca import Biblioteca
import time

app = Biblioteca()

# O cliente se inscreve em DOIS tópicos de BROKERS DIFERENTES
app.inscrever("pedido/123")    # Vai para o 8080
app.inscrever("entrega/status") # Vai para o 8081

print("📱 FOODSTREAM - Acompanhando seu pedido")
print("------------------------------------------")

try:
    while True:
        n = app.receber_notificacao()
        if n:
            # Aqui ele mostra tanto o status da cozinha quanto o GPS do entregador
            origem = "Cozinha" if "pedido" in n.topico else "Motoboy"
            print(f"\n[🔔 {origem}] {n.mensagem}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n[INFO] App do cliente fechado.")