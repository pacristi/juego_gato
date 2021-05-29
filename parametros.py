import os
from math import floor

# rutas imagenes
ruta_logo = os.path.join(os.getcwd(), "sprites", "otros", "logo_blanco.png")
ruta_mapa = os.path.join(os.getcwd(), "sprites", "mapa", "mapa_2.png")
ruta_rectangulo = os.path.join(os.getcwd(), "sprites personales", "rectangulo_verde.png")
ruta_silla = os.path.join(os.getcwd(), "sprites", "mapa", "accesorios", "silla_mesa_roja.png")
ruta_barra_rep = os.path.join(os.getcwd(), "sprites", "otros", "logo_blanco.png")
ruta_cancion = os.path.join(os.getcwd(), "sprites_personales", "Charlie's Here.wav")

carpeta_bocadillos = os.path.join(os.getcwd(), "sprites", "bocadillos")
carpeta_chef = os.path.join(os.getcwd(), "sprites", "chef")
carpeta_cliente_hamster = os.path.join(os.getcwd(), "sprites", "clientes", "hamster")
carpeta_cliente_perro = os.path.join(os.getcwd(), "sprites", "clientes", "perro")
carpeta_mesero = os.path.join(os.getcwd(), "sprites", "mesero")

dic_bocadillos = {}
dic_chef = {}
dic_cliente_hamster = {}
dic_cliente_perro = {}
dic_mesero = {}
dic_datos_partida = {}
dic_datos_mapa = {}

for image_name in os.listdir(carpeta_bocadillos):
    nombre = image_name
    path = os.path.join(os.getcwd(), "sprites", "bocadillos", image_name)
    dic_bocadillos[nombre] = path

for image_name in os.listdir(carpeta_chef):
    nombre = image_name
    path = os.path.join(os.getcwd(), "sprites", "chef", image_name)
    dic_chef[nombre] = path

for image_name in os.listdir(carpeta_cliente_hamster):
    nombre = image_name
    path = os.path.join(os.getcwd(), "sprites", "clientes", "hamster", image_name)
    dic_cliente_hamster[nombre] = path

for image_name in os.listdir(carpeta_cliente_perro):
    nombre = image_name
    path = os.path.join(os.getcwd(), "sprites", "clientes", "perro", image_name)
    dic_cliente_perro[nombre] = path

for image_name in os.listdir(carpeta_mesero):
    nombre = image_name
    path = os.path.join(os.getcwd(), "sprites", "mesero", image_name)
    dic_mesero[nombre] = path

with open("datos.csv", 'r', encoding="utf-8") as datos:
    lista_datos = []
    for line in datos.readlines():
        line = line.rstrip("\n")
        lista_datos.append(line.split(","))
    dic_datos_partida["dinero"] = lista_datos[0][0]
    dic_datos_partida["reputacion"] = lista_datos[0][1]
    dic_datos_partida["rondas"] = lista_datos[0][2]
    contador = 1
    for num in lista_datos[1]:
        dic_datos_partida[f"platos_chef_{contador}"] = num
        contador += 1

with open("mapa.csv", "r", encoding="utf-8") as archivo_mapa:
    lista_mapa = []
    for line in archivo_mapa.readlines():
        line = line.rstrip("\n")
        lista_mapa.append(line.split(","))
        contador_mesa = 1
        contador_chef = 1
    for entidad in lista_mapa:
        if entidad[0] == "mesa":
            entidad[0] = f"mesa_{contador_mesa}"
            contador_mesa += 1
        elif entidad[0] == "chef":
            entidad[0] = f"chef_{contador_chef}"
            contador_chef += 1
        dic_datos_mapa[entidad[0]] = (int(entidad[1]), int(entidad[2]))


PRECIO_CHEF = 300
PRECIO_SILLA = 100
RONDA_INICIAL = 1
EXPERIENCIA_INICIAL_CHEF = 1
PLATOS_INTERMEDIO = 10
EXPERIENCIA_INTERMEDIA = 2
PLATOS_EXPERTO = 30
EXPERIENCIA_EXPERTO = 3
NUMERADOR_PROB_FALLAR = 0.3
SUMA_NIVEL_PROB_FALLAR = 1
PRECIO_BOCADILLO = 5
MIN_TIEMPO_PREPARACION = 0
MAX_TIEMPO_PREPARACION = 15
MULTI_PREP = 2
MIN_PROB_PROP = 0
SUM_PROB_PROP = 1
MULTI_PROB_PROP = 0.05
DENOM_PROB_PROP = 3
LLEGADA_CLIENTES = 5000
PROPINA = 2
TIEMPO_ESPERA_RELAJADO = 30
PROB_RELAJADO = 0.7
TIEMPO_ESPERA_APURADO = 20
PROB_APURADO = 0.3
MAX_PUNTOS_REP = 5
MIN_PUNTOS_REP = 0
MULTI_PEDIDOS = 4
RESTA_PEDIDOS = 2
MULTI_CLIENTES = 5
SUMA_CLIENTES = 1
DINERO_INICIAL = 100
REPUTACION_INICIAL = 5
CHEFS_INICIALES = 1
MESAS_INICIALES = 2
CLIENTES_INICIALES = 10
RAPIDEZ_DEL_RELOJ = 1
VEL_MOVIMIENTO = 5
LARGO_MAPA = 235
ANCHO_MAPA = 495
DINERO_TRAMPA = 9999
REPUTACION_TRAMPA = 5
