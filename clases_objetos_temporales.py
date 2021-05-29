from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from random import random, randint

from clases_objetos import Objetos
from parametros import (PRECIO_BOCADILLO, MIN_PROB_PROP, SUM_PROB_PROP,
                        MULTI_PROB_PROP, DENOM_PROB_PROP, PROPINA,
                        dic_cliente_hamster, TIEMPO_ESPERA_RELAJADO,
                        dic_cliente_perro, TIEMPO_ESPERA_APURADO,
                        dic_bocadillos)


class Clientes(Objetos):
    def __init__(self, x, y, ancho, alto, *args):
        super().__init__(x, y, ancho, alto, *args)
        self.timer_animacion = QTimer()
        self.timer_animacion.timeout.connect(self.animacion_esperar)

        self.timer_irse = QTimer()
        self.timer_irse.timeout.connect(self.irse)

        self.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.bocadillo = None

    def esperar_comida(self, mesa, cafe):
        self.cafe = cafe
        self.mesa = mesa
        self.timer_animacion.start(1000)

    def pagar(self, chef):
        paga = PRECIO_BOCADILLO + self.propina(chef)
        self.cafe.dinero += paga

    def propina(self, chef):
        if random() < max(MIN_PROB_PROP,
                          (chef.nivel * (SUM_PROB_PROP - self.contador_espera *
                           MULTI_PROB_PROP) / DENOM_PROB_PROP)):
            return PROPINA
        else:
            return 0

    def irse(self):
        if self.bocadillo:
            self.bocadillo.comido()
        self.timer_animacion.stop()
        self.mesa.usada = False
        self.cafe.mesas.append(self.mesa)
        self.timer_irse.stop()
        self.cafe.clientes.remove(self)
        self.setGeometry(-70, -70, 70, 70)
        self.hide()
        del self


class ClienteRelajado(Clientes):
    def __init__(self, x, y, ancho, alto, *args):
        super().__init__(x, y, ancho, alto, *args)
        Objetos.lista_clientes.append(self)
        self.setPixmap(QPixmap(dic_cliente_hamster["hamster_01.png"]))
        self.tiempo_espera = TIEMPO_ESPERA_RELAJADO
        self.contador_espera = 0

    def animacion_esperar(self):
        if self.contador_espera < (self.tiempo_espera / 2):
            self.setPixmap(QPixmap(dic_cliente_hamster["hamster_01.png"]))
            self.show()
        elif (self.contador_espera >= (self.tiempo_espera / 2) and
              self.contador_espera < self.tiempo_espera):
            self.setGeometry(self.pos_x - 20, self.pos_y, self.ancho, self.alto)
            self.setPixmap(QPixmap(dic_cliente_hamster["hamster_19.png"]))
            self.show()
        elif self.contador_espera >= self.tiempo_espera:
            self.timer_animacion.stop()
            self.setGeometry(self.pos_x, self.pos_y, self.ancho, self.alto)
            self.setPixmap(QPixmap(dic_cliente_hamster["hamster_27.png"]))
            self.show()
            self.timer_irse.start(1000)
            self.mesa.usada = False
            self.cafe.clientes_perdidos += 1
            self.cafe.pedidos_totales += 1
        self.contador_espera += 1

    def recibir_comida(self):
        self.setPixmap(QPixmap(dic_cliente_hamster["hamster_37.png"]))
        self.bocadillo = Bocadillos(5, 20, 14, 12, self.mesa)
        self.show()


class ClienteApurado(Clientes):
    def __init__(self, x, y, ancho, alto, *args):
        super().__init__(x, y, ancho, alto, *args)
        Objetos.lista_clientes.append(self)
        self.setPixmap(QPixmap(dic_cliente_perro["perro_01.png"]))
        self.tiempo_espera = TIEMPO_ESPERA_APURADO
        self.contador_espera = 0

    def animacion_esperar(self):
        if self.contador_espera < (self.tiempo_espera / 2):
            self.setPixmap(QPixmap(dic_cliente_perro["perro_12.png"]))
            self.show()
        elif (self.contador_espera >= (self.tiempo_espera / 2) and
              self.contador_espera < self.tiempo_espera):
            self.setGeometry(self.pos_x - 20, self.pos_y, self.ancho, self.alto)
            self.setPixmap(QPixmap(dic_cliente_perro["perro_15.png"]))
            self.show()
        elif self.contador_espera >= self.tiempo_espera:
            self.timer_animacion.stop()
            self.setGeometry(self.pos_x, self.pos_y, self.ancho, self.alto)
            self.setPixmap(QPixmap(dic_cliente_perro["perro_17.png"]))
            self.show()
            self.timer_irse.start(1000)
            self.mesa.usada = False
            self.cafe.clientes_perdidos += 1
            self.cafe.pedidos_totales += 1
        self.contador_espera += 1

    def recibir_comida(self):
        self.setPixmap(QPixmap(dic_cliente_perro["perro_11.png"]))
        self.bocadillo = Bocadillos(5, 20, 14, 12, self.mesa)
        self.show()


class Bocadillos(Objetos):
    def __init__(self, x, y, alto, ancho, *args):
        super().__init__(x, y, alto, ancho, *args)
        num_boc = randint(10, 68)
        self.setPixmap(QPixmap(dic_bocadillos[f"bocadillo_{num_boc}.png"]))
        self.show()

    def comido(self):
        self.setGeometry(-70, -70, 70, 70)
        self.hide()
        del self
