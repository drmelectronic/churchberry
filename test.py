#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 22222))
data = [
    {
        'h': '',
        'b': 'Otras letras\n segundo verso\n otro versículo.\nmuchas\nlineas\nmás\nno alcanzan\n.',
        'f': '',
        't': 'Song'
    },
    {
        's': -1,
        'f': 0,
        't': 'Font'
    },
    {
        'h': 'Header',
        'b': 'Primera cancion\n párrafos\n versículo.',
        'f': 'Footer',
        't': 'Song'
    },
    {
        'l': 18,
        'c': 22,
        'v': 2,
        't': 'Bible'
    },
    {
        'l': 16,
        'c': 7,
        'v': 8,
        't': 'Bible'
    },
    {
        'y': -80,
        't': 'Scroll'
    },
    {
        'l': 16,
        'c': 7,
        'v': 9,
        't': 'Bible'
    },
    {
        'y': -50,
        't': 'Scroll'
    },
]

i = 0
while True:
    s.send(json.dumps(data[i]))
    print('send', data[i])
    i += 1
    time.sleep(2)
    if i == len(data):
        i = 0

