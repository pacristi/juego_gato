import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
import os


nombre, clase = uic.loadUiType("ventana_inicial.ui")


class VentanaInicial(nombre, clase):

    senal_seguir_jugando = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_seguir.clicked.connect(self.seguir_jugando)
        self.boton_denuevo.clicked.connect(self.partida_nueva)

    def seguir_jugando(self):
        self.senal_seguir_jugando.emit(True)
        self.hide()

    def partida_nueva(self):
        self.senal_seguir_jugando.emit(False)
        self.hide()
