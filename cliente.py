import json
import socket
from threading import Thread


class Cliente(Thread):

    def __init__(self, app):
        super(Cliente, self).__init__()
        self.connect()
        self.app = app
        self.cambiado = True
        self.data = {'t': None}
        self.ON = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 22222))
        self.socket.settimeout(1)

    def setON(self):
        self.ON = True

    def readSocket(self):
        try:
            recibido = self.socket.recv(1024)
        except socket.timeout:
            return
        try:
            self.data = json.loads(recibido)
        except:
            return
        self.cambiado = True

    def run(self):
        while self.ON:
            self.readSocket()

    def getData(self):
        self.cambiado = False
        return self.data