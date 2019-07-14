# -*- coding: utf-8 -*-

import json
import re


class Biblia:

    def __init__(self):
        self.version_nombre = None
        self.dict = {}
        self.libro = u'Génesis'
        self.capitulo = 1
        self.desde = 1
        self.hasta = 1

    def version(self, nombre):
        if self.version_nombre != nombre:
            archivo = open('biblias/' + nombre + '.json', 'r')
            self.dict = json.loads(archivo.read())
            archivo.close()
            self.version_nombre = nombre
            print('LIBROS', len(self.dict))
        else:
            pass

    def get_libro(self, abr):
        abr = abr.lower()
        for l in self.libros:
            if l[2] == abr:
                return l[0]
            elif l[3].search(abr):
                return l[0]
            else:
                print(abr, l[1])

        return False


    def get(self, cita):
        n = cita.find(' ')
        if n:
            libro = self.get_libro(cita[:n])
            if libro:
                numeros = cita[n + 1:]
                m = numeros.find(':')
                if m < 0:
                    m = numeros.find('.')
                    if m < 0:
                        m = numeros.find(' ')
                        if m < 0:
                            return ''
                capitulo = numeros[:m]
                versiculos = numeros[m + 1:]
                p = versiculos.find('-')
                if p > 0:
                    desde = int(versiculos[:p])
                    hasta = int(versiculos[p + 1:])
                else:
                    desde = int(versiculos)
                    hasta = int(versiculos)
                self.libro = libro
                self.capitulo = int(capitulo)
                self.desde = desde
                self.hasta = hasta
                return self.versiculo()
            return ''
        else:
            return ''

    def versiculo(self, data):
        print('busq vers', data)
        try:
            libro = self.dict[data['l']]
            capitulo = libro['capitulos'][data['c']]
            texto = capitulo[data['v']]
        except:
            print('No se encontro el versiculo')
            return {'h': libro['nombre'], 'b': '-', 'f': self.version_nombre}

        return {'h': libro['nombre'], 'b': '%s:%s %s' % (data['c'] + 1, data['v'] + 1, texto), 'f': self.version_nombre}


def descargar_biblia():
    import urllib3
    version = 'RVR60'
    http = urllib3.HTTPConnectionPool('api.biblia.com')
    f = open(version + '.json', 'r')
    biblia = json.loads(f.read())
    f.close()
    i = 0
    for l in libros:
        i += 1
        if l[0] in biblia:
            print
            i, l[0], 'YA ESTA'
            continue
        print
        i, l[0], 'BUSCAR'
        l[3] = l[2].lower().replace(' ', '')
        cap = 1
        vers = 1
        respuesta = True
        fin_capitulo = False
        while respuesta:
            versiculo = (l[2] + '%d:%d' % (cap, vers))
            url = '/v1/bible/content/' + version + '.txt.js?passage=' + versiculo.replace(' ',
                                                                                          '%20') + '&key=90aa8a24bcb98b1987b1865f61dd8cb6'
            respuesta = http.urlopen('GET', url)
            try:
                respuesta = json.loads(respuesta.data)
            except:
                if fin_capitulo:
                    respuesta = False
                else:
                    cap += 1
                    vers = 1
                    respuesta = True
                    fin_capitulo = True
            else:
                fin_capitulo = False
                data = respuesta['text']
                if l[0] in biblia:
                    if cap in biblia[l[0]]:
                        biblia[l[0]][cap].append(data)
                        print
                        l[0], cap, vers
                    else:
                        biblia[l[0]][cap] = [data]
                        print
                        l[0], cap, vers
                else:
                    biblia[l[0]] = {cap: [data]}
                    print
                    l[0], cap, vers
                vers += 1
        f = open(version + '.json', 'wb')
        f.write(json.dumps(biblia))
        f.close()