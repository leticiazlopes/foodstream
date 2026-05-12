#!/bin/bash

# Pega o diretório atual onde o script está sendo executado
DIR=$(pwd)

echo "🚀 Iniciando o Middleware Pub/Sub FoodStream..."
echo "Configuração: 2 Brokers, 4 Tópicos, 2 Publicadores, 2 Clientes."

osascript <<EOF
tell application "Terminal"
    # --- BROKERS (As fundações) ---
    do script "cd '$DIR' && echo '🌐 BROKER 8080 (Pedidos)' && python3 centralBroker.py 8080"
    delay 1
    do script "cd '$DIR' && echo '🌐 BROKER 8081 (Marketing/Logística)' && python3 centralBroker.py 8081"
    delay 2

    # --- CLIENTES / INSCRITOS (Quem ouve) ---
    # Cliente 1: Focado em Marketing
    do script "cd '$DIR' && echo '📢 CLIENTE MARKETING' && python3 cliente_marketing.py"
    delay 1
    # Cliente 2: Focado em Pedidos e Entrega
    do script "cd '$DIR' && echo '📱 CLIENTE APP (Pedidos/Entrega)' && python3 cliente_pedidos.py"
    delay 2

    # --- PUBLICADORES (Quem envia) ---
    # Publicador 1: Restaurante (Tópicos: pedido/123 e ofertas/diaria)
    do script "cd '$DIR' && echo '🍕 PUBLICADOR: RESTAURANTE' && python3 restaurante.py"
    delay 1
    # Publicador 2: Entregador (Tópicos: entrega/status e suporte/geral)
    do script "cd '$DIR' && echo '🚚 PUBLICADOR: ENTREGADOR' && python3 entregador.py"
end tell
EOF

echo "✅ Todos os terminais foram abertos!"