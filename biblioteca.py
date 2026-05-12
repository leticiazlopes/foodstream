import socket
import threading
import queue
import json
from mensagem import Mensagem
import logging

logging.basicConfig(level=logging.INFO)

class Biblioteca:
    def __init__(self):
        self.conexoes = {} 
        self.fila_mensagens = queue.Queue()
        self.conectado = True
        
    def _definir_broker(self, topico):
        """Regra de Balanceamento: Divide os tópicos entre as portas 8080 e 8081"""
        if topico.startswith("pedido"):
            return 8080
        else:
            return 8081

    def _conectar_ao_broker(self, porta):
        """Gerencia a conexão com os diferentes brokers de forma transparente"""
        if porta not in self.conexoes:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', porta))
                self.conexoes[porta] = sock
                
                threading.Thread(target=self._escutar_servidor, args=(sock,), daemon=True).start()
            except Exception as e:
                logging.error(f"❌ Erro ao conectar no Broker da porta {porta}: {e}")
                return None
        return self.conexoes.get(porta)

    def inscrever(self, topico):
        porta = self._definir_broker(topico)
        sock = self._conectar_ao_broker(porta)
        
        if sock:
            msg = Mensagem("inscricao", topico)
            
            sock.send(msg.prepara_json() + b'\n')
        else:
            logging.warning(f"⚠️ Falha na inscrição: Broker {porta} offline.")

    def publicar(self, topico, conteudo):
        porta = self._definir_broker(topico)
        sock = self._conectar_ao_broker(porta)
        
        if sock:
            msg = Mensagem("publicacao", topico, conteudo)
            sock.send(msg.prepara_json() + b'\n')
        
    def _escutar_servidor(self, socket_especifico):
        """Roda em segundo plano para cada broker conectado"""
        while self.conectado:
            try:
                dados_brutos = socket_especifico.recv(1024)
                if not dados_brutos:
                    break
                
                
                pacotes = dados_brutos.decode('utf-8').strip().split('\n')
                for pacote in pacotes:
                    if pacote:
                        msg_recebida = Mensagem.recebe_json(pacote.encode('utf-8'))
                        self.fila_mensagens.put(msg_recebida)
            except:
                break
        
    def receber_notificacao(self):
        """Verifica se tem algo na Caixa de Entrada comum"""
        try:
            return self.fila_mensagens.get_nowait()
        except queue.Empty:
            return None
        
    def cancelar_inscricao(self, topico):
        porta = self._definir_broker(topico)
        sock = self._conectar_ao_broker(porta)
        
        if sock:
            msg = Mensagem("remocao", topico)
            sock.send(msg.prepara_json() + b'\n')
            logging.info(f"🚪 Inscrição removida do tópico: {topico}")
        else:
            logging.warning(f"⚠️ Falha na remoção: Broker {porta} offline.")