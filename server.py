# -*- coding: utf-8 -*-

# from gevent import monkey
# monkey.patch_all()
from threading import Thread
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor
import json


class ClientFactory(Factory):
    def __init__(self):
        print('Servidor Iniciado')
        self.conexiones = 0
        self.clientes = []

    def buildProtocol(self, addr):
        self.conexiones += 1
        cliente = Cliente(self)
        self.clientes.append(cliente)
        return cliente

    def broadcast(self, data):
        for c in self.clientes:
            c.send(data)

class Cliente(LineReceiver):

    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, recibido):
        try:
            data = json.loads(recibido)
        except:
            print('Error Data Received')
        self.factory.broadcast(recibido)

    def send(self, text):
        self.sendLine(text)


if __name__ == '__main__':
    reactor.listenTCP(22222, ClientFactory())
    reactor.suggestThreadPoolSize(64000)
    reactor.run()
