#Os app usarão
import socket
import threading
import queue
from mensagem import Mensagem

class Biblioteca:
    def __init__(self):
        self.socket_cliente = None
        self.fila_mensagens = queue.Queue()
        self.conectado = False
        
    def conectar(self, host='localhost', porta=5000):
        """Botão: Ligar o rádio"""
        
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect((host, porta))
        self.conectado = True
        threading.Thread(target=self._escutar_servidor, daemon=True).start()
        print ("Conectado ao Central Broker")
        
        
    def inscrever(self, topico):
        """Botão: Sintonizar na rádio do pedido"""
        
        msg = Mensagem("inscricao", topico, "")
        self.socket_cliente.send(msg.prepara_json())
        print(f"Inscrito no tópico {topico}")
        
        
    def publicar(self, topico, dados):
        """Botão: Falar no microfone da rádio (Restaurante avisando)"""
        
        msg = Mensagem("publicacao", topico, dados)
        self.socket_cliente.send(msg.prepara_json())
        
        
    def _escutar_servidor(self): #roda em 2 plano
        while self.conectado:
            try:
                dados_brutos = self.socket_cliente.recv(1024)
                if dados_brutos:
                    msg_recebida = Mensagem.recebe_json(dados_brutos)
                    self.fila_mensagens.put(msg_recebida)
            except:
                break
        
    def receber_notificacao(self):
        """Botão: Verificar se tem algo na Caixa de Entrada"""
        
        try:
            return self.fila_mensagens.get_nowait() #pegar msg na fila 
        except queue.Empty:
            return None # caso n tenha