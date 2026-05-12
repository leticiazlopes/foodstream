import json
import time
from biblioteca import Biblioteca

app = Biblioteca()


print("[ENTREGADOR] Iniciando rota de entrega...")
app.publicar("entrega/status", json.dumps({
    "id_pedido": "123",
    "geolocalizacao": "-23.5505,-46.6333",
    "estimativa": "15 min"
}))

time.sleep(2)


print("[SUPORTE] Enviando aviso do sistema...")
app.publicar("suporte/geral", json.dumps({
    "aviso": "Manutenção programada às 02:00",
    "prioridade": "alta"
}))

print("[INFO] Mensagens enviadas com sucesso!")