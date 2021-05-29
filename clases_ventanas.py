from copy import copy

from PyQt5 import uic
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QMimeData, QPoint
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLabel, QShortcut)
from PyQt5.QtGui import QPixmap, QDrag, QKeySequence

from parametros import (ANCHO_MAPA, LARGO_MAPA, dic_chef, ruta_silla)
from clases_objetos import Objetos

window_mapa, clase_mapa = uic.loadUiType("mapa.ui")
window_tienda, clase_tienda = uic.loadUiType("tienda.ui")
window_informacion, clase_informacion = uic.loadUiType("informacion.ui")
window_post_ronda, clase_post_ronda = uic.loadUiType("ventana_post_ronda.ui")
window_perder, clase_perder = uic.loadUiType("dccancelado.ui")


class Mapa(window_mapa, clase_mapa):

    senal_instanciar_chef = pyqtSignal(int, int)
    senal_instanciar_silla = pyqtSignal(int, int)
    senal_eliminar = pyqtSignal(QLabel)

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.altura = LARGO_MAPA
        self.ancho = ANCHO_MAPA
        self.setFocus()

        self.mapa_usable = QWidget(self)
        self.mapa_usable.area = QRect(27, 90, self.ancho, self.altura)
        self.mapa_usable.setGeometry(self.mapa_usable.area)
        self.mapa_usable.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().text() == "chef":
            x = event.pos().x() - 27
            y = event.pos().y() - 90
            self.senal_instanciar_chef.emit(x, y)
        elif event.mimeData().text() == "silla":
            x = event.pos().x() - 27
            y = event.pos().y() - 90
            print(type(event.pos()))
            self.senal_instanciar_silla.emit(x, y)

    def mousePressEvent(self, event):
        x = event.pos().x() - 27
        y = event.pos().y() - 90
        for elem in Objetos.lista_objetos[1:]:
            if (event.button() == Qt.LeftButton and
               elem.geometry().contains(QPoint(x, y), True)):
                self.senal_eliminar.emit(elem)


class Tienda(window_tienda, clase_tienda):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton and
           self.label_meson.geometry().contains(event.pos())):
            drag = QDrag(self.label_meson)
            mimeData = QMimeData()

            mimeData.setText("chef")
            drag.setMimeData(mimeData)

            drag.setPixmap(QPixmap(dic_chef["meson_01.png"]))

            dropAction = drag.exec_()

        elif (event.button() == Qt.LeftButton and
              self.label_silla.geometry().contains(event.pos())
              ):
            drag = QDrag(self.label_silla)
            mimeData = QMimeData()

            mimeData.setText("silla")
            drag.setMimeData(mimeData)

            drag.setPixmap(QPixmap(ruta_silla))

            dropAction = drag.exec_()


class Info(window_informacion, clase_informacion):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)


class VentanaPrincipal(QMainWindow):

    senal_mapa_usable = pyqtSignal(QLabel, QWidget)
    senal_comenzar_ronda = pyqtSignal()
    senal_caminar_arriba = pyqtSignal()
    senal_caminar_abajo = pyqtSignal()
    senal_caminar_derecha = pyqtSignal()
    senal_caminar_izquierda = pyqtSignal()
    senal_parar_arriba = pyqtSignal()
    senal_parar_abajo = pyqtSignal()
    senal_parar_derecha = pyqtSignal()
    senal_parar_izquierda = pyqtSignal()
    senal_din_trampa = pyqtSignal()
    senal_fin_trampa = pyqtSignal()
    senal_rep_trampa = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.mapa = Mapa(self)
        self.tienda = Tienda(self)
        self.info = Info(self)
        self.setGeometry(200, 100, 900, 500)
        self.setStyleSheet("background-color:#1c7743;")

        self.shortcut_dinero = QShortcut(QKeySequence("M"), self)
        self.shortcut_dinero.activated.connect(self.din_trampa)

        self.shortcut_fin = QShortcut(QKeySequence("F"), self)
        self.shortcut_fin.activated.connect(self.fin_trampa)

        self.shortcut_rep = QShortcut(QKeySequence("R"), self)
        self.shortcut_rep.activated.connect(self.rep_trampa)

        self.info.move(10, 10)
        self.mapa.move(10, 130)
        self.tienda.move(600, 130)

        self.info.boton_comenzar.clicked.connect(self.empezar_ronda)
        self.info.boton_salir.clicked.connect(self.close)
        # self.info.boton_pausa

    def empezar_ronda(self):
        self.senal_comenzar_ronda.emit()

    def desactivar_boton_comenzar(self):
        self.info.boton_comenzar.setEnabled(False)

    def activar_boton_comenzar(self):
        self.info.boton_comenzar.setEnabled(True)

    def mapa_usable(self):
        self.senal_mapa_usable.emit(self.mapa.mapa_usable, self.mapa)

    def actualizar_gui(self):
        self.show()

    def ubicar_elementos(self, elemento, area, imagen):
        elemento.setGeometry(area)
        elemento.setPixmap(imagen)

    def actualizar_info(self, reputacion, dinero, num_ronda, atendidos,
                        perdidos, proximos
                        ):
        self.info.barra_reputacion.setValue(reputacion * 20)
        self.info.cantidad_dinero.setText(f"${dinero}")
        self.info.label_ronda.setText(f"RONDA N°{num_ronda}")
        self.info.label_atendidos.setText(f"{atendidos}")
        self.info.label_perdidos.setText(f"{perdidos}")
        self.info.label_proximos.setText(f"{proximos}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.senal_caminar_arriba.emit()
        elif event.key() == Qt.Key_S:
            self.senal_caminar_abajo.emit()
        elif event.key() == Qt.Key_D:
            self.senal_caminar_derecha.emit()
        elif event.key() == Qt.Key_A:
            self.senal_caminar_izquierda.emit()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W:
            self.senal_parar_arriba.emit()
        elif event.key() == Qt.Key_S:
            self.senal_parar_abajo.emit()
        elif event.key() == Qt.Key_D:
            self.senal_parar_derecha.emit()
        elif event.key() == Qt.Key_A:
            self.senal_parar_izquierda.emit()

    def din_trampa(self):
        self.senal_din_trampa.emit()

    def fin_trampa(self):
        self.senal_fin_trampa.emit()

    def rep_trampa(self):
        self.senal_rep_trampa.emit()

    def salir(self):
        self.close()


class VentanaPostRonda(window_post_ronda, clase_post_ronda):

    senal_pre_ronda = pyqtSignal()
    senal_guardar = pyqtSignal()
    senal_salir = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.boton_salir.clicked.connect(self.salir)
        self.boton_guardar.clicked.connect(self.guardar)
        self.boton_continuar.clicked.connect(self.continuar)

    def post_ronda(self, num_ronda, perdidos, atendidos, dinero, reputacion):
        self.label_ronda.setText(f"RESUMEN RONDA N°{num_ronda}")
        self.num_perdidos.setText(str(perdidos))
        self.num_atendidos.setText(str(atendidos))
        self.num_dinero.setText(f"${dinero}")
        self.num_reputacion.setText(f"{reputacion}/5")
        self.show()

    def continuar(self):
        self.hide()
        self.senal_pre_ronda.emit()
        self.boton_guardar.setEnabled(True)

    def guardar(self):
        self.senal_guardar.emit()
        self.boton_guardar.setEnabled(False)

    def salir(self):
        self.senal_salir.emit()
        self.close()


class Perder(window_perder, clase_perder):

    senal_salir = pyqtSignal()
    senal_jugar_denuevo = pyqtSignal(bool)

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.boton_salir.clicked.connect(self.close)
        self.boton_denuevo.clicked.connect(self.jugar_denuevo)

    def mostrar(self):
        self.senal_salir.emit()
        self.show()

    def jugar_denuevo(self):
        self.senal_jugar_denuevo.emit(False)
        self.close()
