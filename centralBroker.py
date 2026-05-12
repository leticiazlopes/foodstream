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
        self.buffer = Queue()
        threading.Thread(target=self._processar_buffer, daemon=True).start()
        
    def _processar_buffer(self):
        """Thread que consome o buffer e faz as entregas"""
        while True:
            dados_brutos, msg, conexao_origem = self.buffer.get()
            with self.lock:
                lista_inscritos = self.topicos.get(msg.topico, [])
            if lista_inscritos:
                contagem_envios = 0
                for inscrito in list(lista_inscritos):
                    if inscrito == conexao_origem: 
                        continue 
                    try:
                        inscrito.send(dados_brutos)
                        contagem_envios += 1
                    except:
                        
                        with self.lock:
                            if msg.topico in self.topicos and inscrito in self.topicos[msg.topico]:
                                self.topicos[msg.topico].remove(inscrito)
                
                logging.info(f"   ┗━ [BUFFER] ✅ Repassado para {contagem_envios} interessado(s).")
            else:
                logging.warning(f"   ┗━ [BUFFER] ⚠️ Nenhum inscrito no tópico {msg.topico}")
                erro_msg = Mensagem("erro", msg.topico, f"Mensagem descartada: sem inscritos.")
                try:
                    conexao_origem.send(erro_msg.prepara_json() + b'\n')
                except: 
                    pass
            self.buffer.task_done()
        
    def iniciar(self, porta=8080):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', porta))
        server.listen()
        logging.info(f"🚀 Central Broker online na porta {porta}")
        
        while True:
            try:
                conexao, addr = server.accept()
                threading.Thread(target=self.gerenciar_operacao, args=(conexao,), daemon=True).start()
            except Exception as e:
                logging.error(f"Erro no accept: {e}")
            
    def gerenciar_operacao(self, conexao):
        """Thread de Recebimento: Rápida e focada em não bloquear"""
        while True:
            try:
                dados_brutos = conexao.recv(4096) 
                if not dados_brutos:
                    break
                
                msg = Mensagem.recebe_json(dados_brutos)

                if msg.operacao == "inscricao":
                    with self.lock:
                        if msg.topico not in self.topicos:
                            self.topicos[msg.topico] = []
                        self.topicos[msg.topico].append(conexao)
                    logging.info(f"👤 Cliente inscrito no tópico: {msg.topico}")

                elif msg.operacao == "publicacao":
                    logging.info(f"📩 RECEBIDO: {msg.topico}. Enviando para o buffer...")
                    self.buffer.put((dados_brutos, msg, conexao))

                elif msg.operacao == "remocao":
                    with self.lock:
                        if msg.topico in self.topicos:
                            if conexao in self.topicos[msg.topico]:
                                self.topicos[msg.topico].remove(conexao)
                            if not self.topicos[msg.topico]:
                                del self.topicos[msg.topico]
                    logging.info(f"🚪 Cliente removido do tópico: {msg.topico}")

            except Exception as e:
                break

        conexao.close()
            
if __name__ == "__main__":
    porta_escolhida = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    broker = CentralBroker()
    broker.iniciar(porta=porta_escolhida)