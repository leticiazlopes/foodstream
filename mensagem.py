#posssui tópico da mensagem e string JSON
import json


class Mensagem:
    def __init__(self, operacao, topico, mensagem):
        self.operacao = operacao #quero pizza ou avisar que está pronta
        self.topico = topico
        self.mensagem = mensagem
        
    def prepara_json(self): #transformar em string JSON
        dados_pacote = {
            "operacao": self.operacao,
            "topico": self.topico,
            "mensagem": self.mensagem
        }
        return json.dumps(dados_pacote).encode('utf-8')
    
    @staticmethod
    def recebe_json(dados_brutos):
        texto = dados_brutos.decode('utf-8')
        dados_recebidos = json.loads(texto)
        return Mensagem(
            operacao=dados_recebidos.get("operacao"),
            topico=dados_recebidos.get("topico"),
            mensagem=dados_recebidos.get("mensagem")
        )
        

    