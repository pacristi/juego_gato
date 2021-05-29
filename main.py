from ventana_inicial_designer import VentanaInicial
from clases_ventanas import VentanaPrincipal, VentanaPostRonda, Perder
from DCCafe import DCCafe
from clases_objetos import Objetos
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    a = QApplication(sys.argv)

    ventana_inicial = VentanaInicial()
    ventana_principal = VentanaPrincipal()
    dccafe = DCCafe()
    ventana_post_ronda = VentanaPostRonda()
    ventana_perder = Perder()

    ventana_inicial.senal_seguir_jugando.connect(dccafe.iniciar_juego)
    dccafe.senal_recibir_mapa.connect(ventana_principal.mapa_usable)
    ventana_principal.senal_mapa_usable.connect(dccafe.recibir_mapa)
    dccafe.senal_iniciar_gui.connect(ventana_principal.actualizar_gui)

    ventana_principal.senal_caminar_arriba.connect(dccafe.mov_up)
    ventana_principal.senal_caminar_abajo.connect(dccafe.mov_down)
    ventana_principal.senal_caminar_derecha.connect(dccafe.mov_der)
    ventana_principal.senal_caminar_izquierda.connect(dccafe.mov_iz)
    ventana_principal.senal_parar_arriba.connect(dccafe.stop_up)
    ventana_principal.senal_parar_abajo.connect(dccafe.stop_down)
    ventana_principal.senal_parar_derecha.connect(dccafe.stop_der)
    ventana_principal.senal_parar_izquierda.connect(dccafe.stop_iz)
    ventana_principal.senal_comenzar_ronda.connect(dccafe.empezar_ronda)
    dccafe.senal_info.connect(ventana_principal.actualizar_info)
    dccafe.senal_ventana_post_ronda.connect(ventana_post_ronda.post_ronda)
    ventana_post_ronda.senal_pre_ronda.connect(dccafe.pre_ronda)
    ventana_post_ronda.senal_guardar.connect(dccafe.guardar_datos)
    dccafe.senal_desactivar_boton_comenzar.connect(ventana_principal.desactivar_boton_comenzar)
    dccafe.senal_activar_boton_comenzar.connect(ventana_principal.activar_boton_comenzar)
    ventana_post_ronda.senal_salir.connect(ventana_principal.salir)
    ventana_principal.mapa.senal_instanciar_chef.connect(dccafe.instanciar_chef)
    ventana_principal.mapa.senal_instanciar_silla.connect(dccafe.instanciar_silla)
    ventana_principal.mapa.senal_eliminar.connect(dccafe.eliminar)
    dccafe.senal_perder.connect(ventana_perder.mostrar)
    ventana_perder.senal_salir.connect(ventana_principal.salir)
    ventana_perder.senal_jugar_denuevo.connect(dccafe.iniciar_juego)
    ventana_principal.senal_din_trampa.connect(dccafe.din_trampa)
    ventana_principal.senal_fin_trampa.connect(dccafe.fin_trampa)
    ventana_principal.senal_rep_trampa.connect(dccafe.rep_trampa)

    ventana_inicial.show()
    sys.exit(a.exec())
