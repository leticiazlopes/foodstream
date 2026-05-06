#cérebro da aplicação
import socket
import threading
from mensagem import Mensagem


class CentralBroker:
    def __init__(self):
        self.topicos = {} 
        self.lock = threading.Lock()
        
    def iniciar(self, porta=5000):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', porta))
        server.listen()
        print("Central Broker ouvindo ")
        
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
                    print(f"Cliente inscrito no tópico {msg.topico}")
                
                elif msg.operacao == "publicacao":
                    if msg.topico in self.topicos:
                        lista_inscritos = self.topicos[msg.topico]
                        
                        if len(lista_inscritos) > 0:
                            for inscrito in lista_inscritos:
                                inscrito.send(dados_brutos)
                        else:
                            conexao.send("Ninguém inscrito nesse tópico".encode('utf-8'))
                    else:
                        conexao.send("Tópico não encontrado".encode('utf-8'))
                
                elif msg.operacao == "remocao":
                    with self.lock:
                        if msg.topico in self.topicos:
                            self.topicos[msg.topico].remove(conexao)
                            if not self.topicos[msg.topico]: #n tem ng, apaga tópico
                                del self.topicos[msg.topico]
            conexao.close()