@echo off
echo 🚀 Iniciando o Middleware FoodStream no Windows...

:: Abre os Brokers em janelas separadas
start "Broker 8080" cmd /k "python centralBroker.py 8080"
start "Broker 8081" cmd /k "python centralBroker.py 8081"

:: Aguarda os servidores subirem (2 segundos)
timeout /t 2

:: Abre os Clientes
start "App Cliente Pedidos" cmd /k "python cliente_pedidos.py"
start "Painel Marketing" cmd /k "python cliente_marketing.py"

:: Aguarda mais um pouco antes do fluxo principal
timeout /t 1

:: Abre os Publicadores
start "App Entregador" cmd /k "python entregador.py"
start "Sistema Restaurante" cmd /k "python restaurante.py"

echo ✅ Todos os componentes foram iniciados!