# -*- coding: utf-8 -*-

import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
# os.environ['KIVY_TEXT'] = 'sdl2'
from kivy.logger import Logger
import logging
Logger.setLevel(logging.DEBUG)
import cliente

from biblias import Biblia


import kivy


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import *

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.uix.scrollview import ScrollView

Config.set('graphics', 'allow_screensaver', False)
from kivy.config import Config
Config.set('graphics', 'resizable', 0)
from kivy.core.window import Window
Window.size = (1280, 720)
from fonts.iconfonts import register, icon
register('fontawesome', 'fonts/fa-solid-900.ttf', 'fonts/fontawesome.fontd')

kv_path = './kv/'
for kv in os.listdir(kv_path):
    Builder.load_file(kv_path + kv)

class MainApp(App):

    def build(self):
        self.title = 'Churchberry'
        self.main = MainContainer()
        self.screen = self.main.ids['screen']
        self.screen.config()
        self.cargarBiblias()
        cliente.setON()
        Clock.schedule_interval(self.update_reloj, 1 / 60.)
        return self.main

    def on_start(self):
        cliente.start()

    def parseReceived(self, data):
        print(data)
        if data['t'] == 'Song':
            self.screen.setData(data)
        elif data['t'] == 'Font':
            self.screen.setFont(data)
        elif data['t'] == 'Bible':
            if not ('p' in data):
                data['p'] = 1
            try:
                data = self.biblia.versiculo(data)
            except:
                raise
            else:
                print('biblia', data)
                self.screen.setData(data)
        elif data['t'] == 'Scroll':
            if data['y'] == 0:
                self.screen.set_pos(0)
            else:
                self.screen.add_move(data['y'])
        else:
            print('data incompleta', data)

    def update_reloj(self, *args):
        if cliente.cambiado:
            data = cliente.getData()
            self.parseReceived(data)
        self.screen.render()

    def cargarBiblias(self):
        self.biblia = Biblia()
        self.biblia.version('RVR60')

class ScreenDisplay(Screen):

    def config(self):
        self.y = 1
        self.move = 0
        self.opacity = 0
        self.effect = None
        self.header = self.ids['header']
        self.body = self.ids['body']
        self.footer = self.ids['footer']
        self.scrollview = self.ids['scroll']

        self.header.text = u'1'
        self.body.text = u'2'
        self.footer.text = u'3'

    def setData(self, data):
        print(data)
        self.effect = 'hide'
        self.data = data

    def setFont(self, data):
        if 's' in data:
            if data['s'] == 0:
                self.body.font_size = 60
            else:
                self.body.font_size += data['s']

    def cambiar(self):
        print('cambiar')
        self.header.text = 'Header'
        self.body.text = 'Versículo'
        self.footer.text = u'Footer'

    def set_pos(self, pos):
        self.y = pos
        self.scrollview.scroll_y = self.y
        self.move = 0

    def add_move(self, move):
        self.move = move
        print('y', self.y)

    def render(self):
        if self.move > 0:
            if self.y >= 1:
                self.move = 0
            else:
                self.y += 0.01
                self.move -= 1
                self.scrollview.scroll_y = self.y
        elif self.move < 0:
            if self.y <= 0:
                self.move = 0
            else:
                self.y -= 0.01
                self.move += 1
                self.scrollview.scroll_y = self.y
        else:
            if self.effect == 'hide':
                if self.opacity > 0:
                    self.opacity -= 0.1
                else:
                    self.set_pos(1)
                    self.header.text = self.data['h']
                    self.body.text = self.data['b']
                    self.footer.text = self.data['f']
                    self.effect = 'show'
            elif self.effect == 'show':
                if self.opacity < 1:
                    self.opacity += 0.05


class MainContainer(GridLayout):
    pass



if __name__ == '__main__':
    app = MainApp()
    cliente = cliente.Cliente(app)
    app.run()

