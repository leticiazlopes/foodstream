
from queue import Queue
import socket
import threading
from mensagem import Mensagem
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CentralBroker:
    def __init__(self):
        self.topicos = {} 
        self.lock = threading.Lock()
        
    def iniciar(self, porta=8080):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', porta))
        server.listen()
        logging.info(f"Central Broker ouvindo na porta {porta}")
        
        while True:
            conexao, addr = server.accept()
            thread=threading.Thread(target=self.gerenciar_operacao, args=(conexao,)).start()
            
    def gerenciar_operacao(self, conexao):
            while True:
                dados_brutos = conexao.recv(1024)
                if not dados_brutos: break
                msg=Mensagem.recebe_json(dados_brutos)
                
                if msg.operacao == "inscricao":
                    with self.lock:
                        if msg.topico not in self.topicos:
                            self.topicos[msg.topico] = []
                        self.topicos[msg.topico].append(conexao)
                    logging.info(f"Cliente inscrito no tópico {msg.topico}")
                
                elif msg.operacao == "publicacao":
                    logging.info(f"📩 PUBLICAÇÃO RECEBIDA")
                    logging.info(f"   ┃ Tópico: {msg.topico}")
                    logging.info(f"   ┃ Conteúdo: {msg.mensagem}") 
                    
                    if msg.topico in self.topicos:
                        lista_inscritos = self.topicos[msg.topico]
                        contagem_envios = 0
                        
                        for inscrito in list(lista_inscritos):
                            if inscrito == conexao:
                                continue 
                                
                            try:
                                inscrito.send(dados_brutos)
                                contagem_envios += 1
                            except:
                                self.topicos[msg.topico].remove(inscrito)
                        
                        logging.info(f"   ┗━ ✅ Repassado para {contagem_envios} interessado(s).")
                    else:
                        logging.warning(f"   ┗━ ⚠️ Nenhum inscrito no tópico {msg.topico}")
                        erro_msg = Mensagem("erro", msg.topico, f"Tópico '{msg.topico}' não possui inscritos. Mensagem descartada.")
                        conexao.send(erro_msg.prepara_json() + b'\n')
                
                elif msg.operacao == "remocao":
                    with self.lock:
                        if msg.topico in self.topicos:
                            self.topicos[msg.topico].remove(conexao)
                            if not self.topicos[msg.topico]: 
                                del self.topicos[msg.topico]
            conexao.close()
            
if __name__ == "__main__":
    porta_escolhida = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    broker = CentralBroker()
    broker.iniciar(porta=porta_escolhida)