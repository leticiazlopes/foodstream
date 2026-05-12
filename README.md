
# 🍕 FoodStream - Middleware Pub/Sub Distribuído

O **FoodStream** é um middleware de mensagens baseado no padrão **Publish/Subscribe**, desenvolvido para facilitar a comunicação entre diferentes partes de um ecossistema de delivery (Restaurantes, Entregadores e Clientes). 

O projeto utiliza **Sockets TCP** e threads para garantir que a troca de mensagens seja assíncrona, escalável e transparente.

## 🚀 Funcionalidades

* **Arquitetura Pub/Sub:** Comunicação desacoplada entre publicadores e inscritos.
* **Balanceamento de Carga (Sharding):** Distribuição automática de tópicos entre múltiplas instâncias de Brokers.
* **Transparência de Localização:** A aplicação não precisa saber em qual porta o Broker está rodando; a biblioteca gerencia as conexões.
* **Garantia de Entrega/Descarte:** O Broker informa o publicador caso uma mensagem seja descartada por falta de inscritos.
* **Buffer de Mensagens:** Processamento independente para recebimento e encaminhamento.

---

## 🏗️ Estrutura do Projeto

* `centralBroker.py`: O servidor intermediário que gerencia tópicos e distribui mensagens.
* `biblioteca.py`: A camada de abstração (API) usada pelas aplicações.
* `restaurante.py`: Publicador de pedidos e promoções.
* `entregador.py`: Publicador de status de GPS e avisos de suporte.
* `cliente.py`: Aplicativo do usuário que acompanha o pedido e a entrega.
* `cliente_marketing.py`: Painel que exibe ofertas relâmpago.

---

## ⚖️ Estratégia de Balanceamento

Para atender ao requisito de balanceamento de carga, a biblioteca implementa uma regra de **Sharding por Tópico**. Isso permite que o sistema cresça horizontalmente:

| Prefixo do Tópico | Broker Destino | Tipo de Tráfego |
| :--- | :--- | :--- |
| `pedido/` | **Porta 8080** | Crítico (Transacional) |
| `outros` | **Porta 8081** | Informativo (Marketing/Logística) |



---

## 🛠️ Como Executar (Cenário de Teste)

Para demonstrar a capacidade total do middleware (2 Brokers, 2 Publicadores, 2 Inscritos e 4 Tópicos), siga a ordem abaixo em terminais separados:

### 1. Inicie os Brokers
```bash
python3 centralBroker.py 8080
python3 centralBroker.py 8081
```

### 2. Inicie os Inscritos (Clientes)
```bash
python3 cliente.py             # Ouve 'pedido/123' e 'entrega/status'
python3 cliente_marketing.py   # Ouve 'ofertas/diaria'
```

### 3. Inicie os Publicadores
```bash
python3 restaurante.py         # Envia para 8080 e 8081
python3 entregador.py          # Envia para 8081
```

---

## 📋 Protocolo de Comunicação

As mensagens trafegam via Sockets TCP encapsuladas em formato **JSON**, seguindo a estrutura:

```json
{
  "operacao": "publicar | inscrever | remocao | erro",
  "topico": "nome/do/topico",
  "mensagem": "conteúdo da mensagem ou dados do erro"
}
```
