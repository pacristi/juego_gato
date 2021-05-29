from random import randint, random, choice
from copy import copy
from math import floor

from PyQt5.QtCore import pyqtSignal, QObject, QRect, QTimer
from PyQt5.QtMultimedia import QSound

from clases_objetos import Mesero, Chef, Mesa, Objetos
from clases_objetos_temporales import ClienteRelajado, ClienteApurado
from parametros import (ANCHO_MAPA, LARGO_MAPA, CHEFS_INICIALES,
                        dic_datos_partida, dic_datos_mapa, MESAS_INICIALES, PROB_RELAJADO,
                        DINERO_INICIAL, REPUTACION_INICIAL,
                        RONDA_INICIAL, MULTI_CLIENTES, SUMA_CLIENTES, ruta_cancion,
                        MIN_PUNTOS_REP, MAX_PUNTOS_REP, MULTI_PEDIDOS, RESTA_PEDIDOS,
                        LLEGADA_CLIENTES, PRECIO_CHEF, PRECIO_SILLA,
                        DINERO_TRAMPA, REPUTACION_TRAMPA
                        )


class DCCafe(QObject):

    senal_iniciar_gui = pyqtSignal()
    senal_recibir_mapa = pyqtSignal()
    senal_info = pyqtSignal(int, int, int, int, int, int)
    senal_ventana_post_ronda = pyqtSignal(int, int, int, int, int)
    senal_desactivar_boton_comenzar = pyqtSignal()
    senal_activar_boton_comenzar = pyqtSignal()
    senal_perder = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.reputacion = REPUTACION_INICIAL
        self.dinero = DINERO_INICIAL
        self.num_ronda = RONDA_INICIAL
        self.clientes_atendidos = 0
        self.clientes_perdidos = 0
        self.clientes_proximos = MULTI_CLIENTES * (SUMA_CLIENTES + self.num_ronda)
        self.pedidos_exitosos = 0
        self.pedidos_totales = 0
        self.clientes = []
        self.chefs = []
        self.disponibilidad = True

        self.timer_ronda = QTimer()
        self.timer_ronda.timeout.connect(self.ronda)
        self.timer_info = QTimer()
        self.timer_info.timeout.connect(self.actualizar_info)
        self.comprar = False

    def recibir_mapa(self, mapa, mapa_total):
        self.mapa_usable = mapa
        self.mapa_total = mapa_total

    def din_trampa(self):
        self.dinero = DINERO_TRAMPA

    def rep_trampa(self):
        self.reputacion = REPUTACION_TRAMPA

    def fin_trampa(self):
        self.clientes_proximos = 0
        for elem in reversed(self.clientes):
            elem.irse()
        self.timer_ronda.stop()
        self.timer_info.stop()
        self.post_ronda()

    def nueva_partida(self):
        self.chefs = []
        self.mesas = []
        self.reputacion = REPUTACION_INICIAL
        self.dinero = DINERO_INICIAL
        self.num_ronda = RONDA_INICIAL
        self.clientes_perdidos = 0
        self.clientes_atendidos = 0
        self.pedidos_totales = 0
        if len(Objetos.lista_objetos) != 0:
            for elem in reversed(Objetos.lista_objetos):
                self.eliminar(elem)
        objetos = []
        self.mesero = Mesero(randint(0, ANCHO_MAPA - 25), randint(0, LARGO_MAPA - 27), 25, 27, "", self.mapa_usable)
        objetos.append(self.mesero)
        for num_chef in range(CHEFS_INICIALES):
            chef = Chef(randint(0, ANCHO_MAPA - 59), randint(0, LARGO_MAPA - 69), 59, 69, 0, self, "", self.mapa_usable)
            objetos.append(chef)
            self.chefs.append(chef)
        for num_mesa in range(MESAS_INICIALES):
            mesa = Mesa(randint(0, ANCHO_MAPA - 24), randint(0, LARGO_MAPA - 43), 24, 43, "", self.mapa_usable)
            objetos.append(mesa)
            self.mesas.append(mesa)
        copia_objetos = copy(objetos)
        for elem in reversed(objetos):
            objetos.remove(elem)
            for ob in objetos:
                if elem.area.intersects(ob.area):
                    for objeto in copia_objetos:
                        objeto.setParent(None)
                        objeto.area = QRect()
                        Objetos.lista_objetos.remove(objeto)
                    self.mesas = []
                    self.chefs = []
                    self.nueva_partida()
                    return
        self.empezar_ronda()
        self.timer_info.start(1)

    def cargar_partida(self):
        self.mesas = []
        self.reputacion = int(dic_datos_partida["reputacion"])
        self.dinero = int(dic_datos_partida["dinero"])
        self.num_ronda = int(dic_datos_partida["rondas"])
        self.clientes_proximos = MULTI_CLIENTES * (SUMA_CLIENTES + self.num_ronda)
        x = dic_datos_mapa["mesero"][0]
        y = dic_datos_mapa["mesero"][1]
        self.mesero = Mesero(x, y, 25, 27, "", self.mapa_usable)
        cont_chef = 1
        cont_mesa = 1
        for elem in list(dic_datos_mapa.keys()):
            if f"chef_{cont_chef}" == elem:
                x = dic_datos_mapa[elem][0]
                y = dic_datos_mapa[elem][1]
                platos = int(dic_datos_partida[f"platos_{elem}"])
                chef = Chef(x, y, 59, 69, platos, self, "", self.mapa_usable)
                cont_chef += 1
                self.pedidos_totales += int(platos)
                self.chefs.append(chef)
        self.pedidos_exitosos = self.pedidos_totales / 2
        for elem in list(dic_datos_mapa.keys()):
            if f"mesa_{cont_mesa}" == elem:
                x = dic_datos_mapa[elem][0]
                y = dic_datos_mapa[elem][1]
                mesa = Mesa(x, y, 24, 43, "", self.mapa_usable)
                self.mesas.append(mesa)
                cont_mesa += 1
        self.empezar_ronda()
        self.timer_info.start(1)

    def iniciar_juego(self, h):
        self.senal_recibir_mapa.emit()
        if h is False:
            self.nueva_partida()
        elif h is True:
            self.cargar_partida()
        self.senal_iniciar_gui.emit()

    def mov_der(self):
        self.mesero.caminar_derecha()

    def mov_iz(self):
        self.mesero.caminar_izquierda()

    def mov_up(self):
        self.mesero.caminar_arriba()

    def mov_down(self):
        self.mesero.caminar_abajo()

    def stop_der(self):
        self.mesero.parar_derecha()

    def stop_iz(self):
        self.mesero.parar_izquierda()

    def stop_up(self):
        self.mesero.parar_arriba()

    def stop_down(self):
        self.mesero.parar_abajo()

    def pre_ronda(self):
        self.clientes_atendidos = 0
        self.clientes_perdidos = 0
        self.senal_activar_boton_comenzar.emit()
        self.disponibilidad = False
        self.mapa_total.setAcceptDrops(True)

    def empezar_ronda(self):
        self.mapa_total.setAcceptDrops(False)
        self.senal_desactivar_boton_comenzar.emit()
        self.soundtrack = QSound(ruta_cancion)
        self.soundtrack.play()
        self.soundtrack.setLoops(1000)
        self.clientes_proximos = MULTI_CLIENTES * (SUMA_CLIENTES + self.num_ronda)
        self.timer_info.start(1)
        self.timer_ronda.start(LLEGADA_CLIENTES)

    def ronda(self):
        self.disponibilidad = True
        if self.clientes_proximos <= 0 and len(self.clientes) == 0:
            self.timer_ronda.stop()
            self.timer_info.stop()
            self.post_ronda()
            return
        elif len(self.mesas) > 0:
            mesa = choice(self.mesas)
            if not mesa.usada and self.clientes_proximos > 0:
                if random() < PROB_RELAJADO:
                    cliente = ClienteRelajado(-70, -70, 70, 70, "", self.mapa_total)
                    self.clientes.append(cliente)
                    mesa.sentar_cliente(self)
                    self.mesas.remove(mesa)
                else:
                    cliente = ClienteApurado(-70, -70, 70, 70, "", self.mapa_total)
                    self.clientes.append(cliente)
                    mesa.sentar_cliente(self)
                    self.mesas.remove(mesa)

    def post_ronda(self):
        self.disponibilidad = False
        self.calcular_reputacion()
        self.soundtrack.stop()
        if self.reputacion > 0:
            self.senal_ventana_post_ronda.emit(self.num_ronda, self.clientes_perdidos, self.clientes_atendidos, self.dinero, self.reputacion)
            self.num_ronda += 1
            self.clientes_proximos = MULTI_CLIENTES * (SUMA_CLIENTES + self.num_ronda)
        elif self.reputacion <= 0:
            self.senal_perder.emit()

    def instanciar_chef(self, x, y):
        if self.dinero >= PRECIO_CHEF:
            chef = Chef(x, y, 59, 69, 0, self, "", self.mapa_usable)
            # if not self.mapa_usable.area.contains(chef.area):
            #     Objetos.lista_objetos.remove(chef)
            #     return
            for elem in Objetos.lista_objetos[:-1]:
                if chef.area.intersects(elem.area):
                    Objetos.lista_objetos.remove(chef)
                    return
            chef.show()
            self.dinero -= PRECIO_CHEF
            self.actualizar_info()

    def instanciar_silla(self, x, y):
        if self.dinero >= PRECIO_SILLA:
            mesa = Mesa(x, y, 24, 43, "", self.mapa_usable)
            # if not self.mapa_usable.area.contains(mesa.area):
            #     Objetos.lista_objetos.remove(mesa)
            #     return
            for elem in Objetos.lista_objetos[:-1]:
                if mesa.area.intersects(elem.area):
                    Objetos.lista_objetos.remove(mesa)
                    return
            mesa.show()
            self.dinero -= PRECIO_SILLA
            self.actualizar_info()
            self.mesas.append(mesa)

    def eliminar(self, label):
        if not self.disponibilidad:
            if label in self.mesas:
                if len(self.mesas) > 1:
                    self.mesas.remove(label)
                    Objetos.lista_objetos.remove(label)
                    label.setGeometry(-70, -70, 70, 70)
                    label.hide()
                    label.area = QRect()
                    del label
            elif label in self.chefs:
                if len(self.chefs) > 1:
                    self.chefs.remove(label)
                    Objetos.lista_objetos.remove(label)
                    label.setGeometry(-70, -70, 70, 70)
                    label.hide()
                    label.area = QRect()
                    del label
            else:
                Objetos.lista_objetos.remove(label)
                label.setGeometry(-70, -70, 70, 70)
                label.hide()
                label.area = QRect()
                del label

    def actualizar_info(self):
        self.senal_info.emit(self.reputacion, self.dinero, self.num_ronda, self.clientes_atendidos, self.clientes_perdidos, self.clientes_proximos)

    def calcular_reputacion(self):
        if self.pedidos_totales != 0:
            self.reputacion = max(MIN_PUNTOS_REP, min(MAX_PUNTOS_REP, (self.reputacion + floor(MULTI_PEDIDOS * self.pedidos_exitosos / self.pedidos_totales - RESTA_PEDIDOS))))

    def guardar_datos(self):
        with open("datos.csv", "w", encoding="utf-8") as archivo_datos:
            datos_2 = ""
            datos_1 = f"{self.dinero},{self.reputacion},{self.num_ronda}\n"
            for elem in self.chefs:
                datos_2 += f"{elem.platos_preparados},"
            archivo_datos.write(datos_1)
            archivo_datos.write(datos_2)

        with open("mapa.csv", "w", encoding="utf-8") as archivo_mapa:
            archivo_mapa.write(f"mesero,{self.mesero.pos_x},{self.mesero.pos_y}\n")
            for elem in self.mesas:
                archivo_mapa.write(f"mesa,{elem.pos_x},{elem.pos_y}\n")
            for elem in self.chefs:
                archivo_mapa.write(f"chef,{elem.pos_x},{elem.pos_y}\n")
