from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRect, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap

from parametros import (
                        dic_mesero, ANCHO_MAPA, LARGO_MAPA,
                        dic_chef, ruta_silla,
                        MIN_TIEMPO_PREPARACION, MAX_TIEMPO_PREPARACION,
                        MULTI_PREP, PLATOS_INTERMEDIO, PLATOS_EXPERTO,
                        EXPERIENCIA_INTERMEDIA, EXPERIENCIA_EXPERTO,
                        NUMERADOR_PROB_FALLAR, SUMA_NIVEL_PROB_FALLAR,
                        )

from random import choice, random


class Objetos(QLabel):
    lista_objetos = []
    lista_clientes = []

    def __init__(self, x, y, ancho, alto, *args):
        super().__init__(*args)
        self.pos_x = x
        self.pos_y = y
        self.ancho = ancho
        self.alto = alto
        self.area = QRect(self.pos_x, self.pos_y, self.ancho, self.alto)
        self.setGeometry(self.area)


class Mesero(Objetos):
    def __init__(self, x, y, ancho, alto, *args):
        super().__init__(x, y, ancho, alto, *args)
        Objetos.lista_objetos.append(self)
        self.setPixmap(QPixmap(dic_mesero["down_02.png"]))

        self.timer_derecha = QTimer()
        self.timer_derecha.timeout.connect(self.caminar_derecha)
        self.contador_animacion_der = 1
        self.timer_izquierda = QTimer()
        self.timer_izquierda.timeout.connect(self.caminar_izquierda)
        self.contador_animacion_iz = 1
        self.timer_arriba = QTimer()
        self.timer_arriba.timeout.connect(self.caminar_arriba)
        self.contador_animacion_ar = 1
        self.timer_abajo = QTimer()
        self.timer_abajo.timeout.connect(self.caminar_abajo)
        self.contador_animacion_ab = 1

        self.llevando_comida = False
        self.chef_seleccionado = None

    def caminar_derecha(self):
        for elem in Objetos.lista_objetos[1:]:
            if elem.area.intersects(QRect(self.pos_x + 2, self.pos_y,
                                          self.ancho, self.alto)):
                return
        self.timer_derecha.start(10)
        if self.pos_x < ANCHO_MAPA - self.ancho:
            self.pos_x += 2
        self.animacion_caminar_derecha()
        self.move(self.pos_x, self.pos_y)
        self.area.moveTo(self.pos_x + 2, self.pos_y)

    def caminar_izquierda(self):
        for elem in Objetos.lista_objetos[1:]:
            if elem.area.intersects(QRect(self.pos_x - 2, self.pos_y,
                                          self.ancho, self.alto)):
                return
        self.timer_izquierda.start(10)
        if self.pos_x > 0:
            self.pos_x -= 2
        self.animacion_caminar_izquierda()
        self.move(self.pos_x, self.pos_y)
        self.area.moveTo(self.pos_x - 2, self.pos_y)

    def caminar_arriba(self):
        for elem in Objetos.lista_objetos[1:]:
            if elem.area.intersects(QRect(self.pos_x, self.pos_y - 2,
                                          self.ancho, self.alto)):
                return
        self.timer_arriba.start(10)
        if self.pos_y > 0:
            self.pos_y -= 2
        self.animacion_caminar_arriba()
        self.move(self.pos_x, self.pos_y)
        self.area.moveTo(self.pos_x, self.pos_y - 2)

    def caminar_abajo(self):
        for elem in Objetos.lista_objetos[1:]:
            if elem.area.intersects(QRect(self.pos_x, self.pos_y + 2,
                                          self.ancho, self.alto)):
                return
        self.timer_abajo.start(10)
        if self.pos_y < LARGO_MAPA - self.alto:
            self.pos_y += 2
        self.animacion_caminar_abajo()
        self.move(self.pos_x, self.pos_y)
        self.area.moveTo(self.pos_x, self.pos_y + 2)

    def parar_derecha(self):
        self.timer_derecha.stop()

    def parar_izquierda(self):
        self.timer_izquierda.stop()

    def parar_arriba(self):
        self.timer_arriba.stop()

    def parar_abajo(self):
        self.timer_abajo.stop()

    def animacion_caminar_derecha(self):
        if not self.llevando_comida:
            if self.contador_animacion_der >= 4:
                self.contador_animacion_der = 1
            anim = self.contador_animacion_der
            self.setPixmap(QPixmap(dic_mesero[f"right_0{anim}.png"]))
            self.contador_animacion_der += 1
        elif self.llevando_comida is True:
            if self.contador_animacion_der >= 4:
                self.contador_animacion_der = 1
            anim = self.contador_animacion_der
            self.setPixmap(QPixmap(dic_mesero[f"right_snack_0{anim}.png"]))
            self.contador_animacion_der += 1

    def animacion_caminar_izquierda(self):
        if self.llevando_comida is False:
            if self.contador_animacion_iz >= 4:
                self.contador_animacion_iz = 1
            anim = self.contador_animacion_iz
            self.setPixmap(QPixmap(dic_mesero[f"left_0{anim}.png"]))
            self.contador_animacion_iz += 1
        elif self.llevando_comida is True:
            if self.contador_animacion_iz >= 4:
                self.contador_animacion_iz = 1
            anim = self.contador_animacion_iz
            self.setPixmap(QPixmap(dic_mesero[f"left_snack_0{anim}.png"]))
            self.contador_animacion_iz += 1

    def animacion_caminar_arriba(self):
        if self.llevando_comida is False:
            if self.contador_animacion_ar >= 4:
                self.contador_animacion_ar = 1
            anim = self.contador_animacion_ar
            self.setPixmap(QPixmap(dic_mesero[f"up_0{anim}.png"]))
            self.contador_animacion_ar += 1
        elif self.llevando_comida is True:
            if self.contador_animacion_ar >= 4:
                self.contador_animacion_ar = 1
            anim = self.contador_animacion_ar
            self.setPixmap(QPixmap(dic_mesero[f"up_snack_0{anim}.png"]))
            self.contador_animacion_ar += 1

    def animacion_caminar_abajo(self):
        if self.llevando_comida is False:
            if self.contador_animacion_ab >= 4:
                self.contador_animacion_ab = 1
            anim = self.contador_animacion_ab
            self.setPixmap(QPixmap(dic_mesero[f"down_0{anim}.png"]))
            self.contador_animacion_ab += 1
        elif self.llevando_comida is True:
            if self.contador_animacion_ab >= 4:
                self.contador_animacion_ab = 1
            anim = self.contador_animacion_ab
            self.setPixmap(QPixmap(dic_mesero[f"down_snack_0{anim}.png"]))
            self.contador_animacion_ab += 1


class Chef(Objetos):
    def __init__(self, x, y, ancho, alto, platos_preparados, cafe, *args):
        super().__init__(x, y, ancho, alto, *args)
        Objetos.lista_objetos.append(self)
        self.setPixmap(QPixmap(dic_chef["meson_01.png"]))
        self.platos_preparados = platos_preparados
        self.cafe = cafe
        self.nivel = 1
        self.preparando = False

        self.timer_esperar_orden = QTimer()
        self.timer_esperar_orden.timeout.connect(self.esperar_orden)
        self.timer_esperar_orden.start(10)
        self.contador_animacion_coc = 13
        self.timer_animacion = QTimer()
        self.timer_animacion.timeout.connect(self.animacion_preparar)
        self.timer_cocinando = QTimer()
        self.timer_cocinando.timeout.connect(self.preparar)

        self.estado = "empezando"
        self.listo = False
        self.setScaledContents(True)

    def esperar_orden(self):
        if (self.area.intersects(Objetos.lista_objetos[0].area) and
                self.preparando is False and self.listo is False and
                Objetos.lista_objetos[0].llevando_comida is False):
            self.preparando = True
            self.estado = "empezando"
            self.preparar()
        elif (self.area.intersects(Objetos.lista_objetos[0].area) and
              self.listo is True and Objetos.lista_objetos[0].llevando_comida is False):
            Objetos.lista_objetos[0].llevando_comida = True
            Objetos.lista_objetos[0].chef_seleccionado = self
            self.listo = False
            self.setPixmap(QPixmap(dic_chef["meson_01.png"]))

    def preparar(self):
        if self.estado == "empezando":
            self.animacion_preparar()
            self.timer_cocinando.start(self.tiempo_preparacion())
        elif self.estado == "terminado":
            if self.prob_fallar():
                self.timer_cocinando.stop()
                self.timer_animacion.stop()
                self.setPixmap(QPixmap(dic_chef["meson_16.png"]))
                self.preparando = False
                self.listo = True
                self.platos_preparados += 1
                self.calc_nivel()
            else:
                self.timer_cocinando.stop()
                self.timer_animacion.stop()
                self.preparando = False
                self.listo = False
                self.setPixmap(QPixmap(dic_chef["meson_01.png"]))

    def prob_fallar(self):
        prob_fallar = NUMERADOR_PROB_FALLAR / (self.nivel + SUMA_NIVEL_PROB_FALLAR)
        if random() < prob_fallar:
            return False
        else:
            return True

    def tiempo_preparacion(self):
        return max(MIN_TIEMPO_PREPARACION,
                   MAX_TIEMPO_PREPARACION - self.cafe.reputacion - self.nivel *
                   MULTI_PREP) * 1000

    def animacion_preparar(self):
        self.timer_animacion.start(1000)
        if self.contador_animacion_coc >= 16:
            self.contador_animacion_coc = 13
        anim = self.contador_animacion_coc
        self.setPixmap(QPixmap(dic_chef[f"meson_{anim}.png"]))
        self.contador_animacion_coc += 1
        self.estado = "terminado"

    def calc_nivel(self):
        if (self.platos_preparados >= PLATOS_INTERMEDIO and
           self.platos_preparados < PLATOS_EXPERTO):
            self.nivel = EXPERIENCIA_INTERMEDIA
        elif self.platos_preparados >= PLATOS_EXPERTO:
            self.nivel = EXPERIENCIA_EXPERTO


class Mesa(Objetos):
    def __init__(self, x, y, ancho, alto, *args):
        super().__init__(x, y, ancho, alto, *args)
        Objetos.lista_objetos.append(self)
        self.setPixmap(QPixmap(ruta_silla))
        self.setScaledContents(True)

        self.timer_recibir_comida = QTimer()
        self.timer_recibir_comida.timeout.connect(self.recibir_comida_cliente)
        self.timer_recibir_comida.start(10)
        self.usada = False

    def sentar_cliente(self, cafe):
        self.cafe = cafe
        self.cafe.clientes_proximos -= 1
        self.cliente = choice(Objetos.lista_clientes)
        Objetos.lista_clientes.remove(self.cliente)
        self.usada = True
        self.cliente.pos_x = self.pos_x + 25
        self.cliente.pos_y = self.pos_y + 50
        self.cliente.setGeometry(self.cliente.pos_x, self.cliente.pos_y,
                                 self.cliente.ancho, self.cliente.alto)
        self.cliente.esperar_comida(self, self.cafe)

    def recibir_comida_cliente(self):
        if (self.area.intersects(Objetos.lista_objetos[0].area) and
                Objetos.lista_objetos[0].llevando_comida and self.usada):
            Objetos.lista_objetos[0].llevando_comida = False
            Objetos.lista_objetos[0].setPixmap(QPixmap(dic_mesero["down_01.png"]))
            self.cliente.timer_animacion.stop()
            self.cliente.setGeometry(self.cliente.pos_x - 20,
                                     self.cliente.pos_y - 5, self.cliente.ancho,
                                     self.cliente.alto)
            self.cliente.recibir_comida()
            self.cliente.timer_irse.start(1000)
            self.usada = False
            self.cliente.pagar(Objetos.lista_objetos[0].chef_seleccionado)
            Objetos.lista_objetos[0].chef_seleccionado = None
            self.cafe.clientes_atendidos += 1
            self.cafe.pedidos_totales += 1
            self.cafe.pedidos_exitosos += 1
