# Tarea 02: DCCafé :school_satchel:

## Consideraciones generales :octocat:

la tarea no tiene implementada la función de pausa y las funciones de trampa están implementadas con otras teclas. Tampoco implementé un reloj interno :disappointed:. El resto si está implementado.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Ventana de Inicio: Hecha completa

    * <Código<sub>1</sub>>: ```ventana_inicial_designer.py``` línea 21

    * <Código<sub>2</sub>>: ```DCCafe.py``` línea 107

    * <Código<sub>3</sub>>: ```DCCafe.py``` línea 68

* Ventana de Juego: Al comprar mesas y chefs, se pueden poner sobre el borde :sweat_smile:

    * Generales: Hecha completa

        * <Código<sub>4</sub>>: ```DCCafe.py``` línea 273

    * Ventana de pre-ronda: Se pueden dropear objetos en posiciones no válidas y hay un error en el que no se puede eliminar el chef original.

        * <Código<sub>1</sub>>: ```clases_ventanas.py``` línea 65

        * <Código<sub>3</sub>>: ```clases_ventanas.py``` línea 51

    * Ventana de ronda: Hecha completa

        * <Código<sub>2</sub>>: ```DCCafe.py``` línea 187

    * Ventana de post-ronda: Hecha completa

        * <Código<sub>2</sub>>: ```clases_ventanas.py``` línea 201

        * <Código<sub>4</sub>>: ```DCCafe.py``` línea 208


* Entidades: En general esta parte le faltan algunas señales, principalmente de las animaciones e imagenes.

    * Jugador: Hecha completa (El movimiento puede ser que esté un poco rápido)

        * <Código<sub>1</sub>>: ```clases_objetos.py``` línea 53

        * <Código<sub>2</sub>>: ```clases_objetos.py``` línea 54

        * <Código<sub>3</sub>>: ```clases_objetos.py``` línea 194 y 281

    * Chef: Hecha completa

        * <Código<sub>1</sub>>: ```clases_objetos.py``` línea 239

        * <Código<sub>2</sub>>: ```clases_objetos.py``` línea 248

        * <Código<sub>3</sub>>: ```clases_objetos.py``` línea 227

    * Bocadillos: Hecha completa

        * <Código<sub>1</sub>>: ```clases_objetos.py``` línea 234

        * <Código<sub>2</sub>>: ```clases_objetos_temporales.py``` línea 35

    * Clientes: Hecha completa

        * <Código<sub>1</sub>>: ```clases_objetos_temporales.py``` línea 64 y 98

        * <Código<sub>2</sub>>: ```clases_objetos_temporales.py``` línea 43

    * DCCafé: Hecha completa

        * <Código<sub>1</sub>>: ```clases_objetos_temporales.py``` línea 64 y 98

        * <Código<sub>2</sub>>: ```clases_objetos_temporales.py``` línea 43

* Tiempo: Me faltó hacer todo :sob:

* Funcionalidades Extra: Las implementé pero con otra combinacion de teclas (No supe como hacerlo solo con letras)

    * <Código<sub>1</sub>>: ```clases_objetos.py``` línea 122

    * <Código<sub>2</sub>>: ```clases_objetos.py``` línea 125

    * <Código<sub>3</sub>>: ```clases_objetos.py``` línea 128

* General: Hay unos problemas de separacion entre back y front end princiálmente al hacer animaciones e instanciar nuevas entidades

* Bonus: No Hecho

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```mapa.csv``` en ```t02```
2. ```datos.csv``` en ```t02```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: ```uic```
2. ```PyQt5.QtCore```: ```Qt / QRect / pyqtSignal / QMimeData / QPoint / QTimer / QObject```
3. ```PyQt5.QtWidgets```: ```QWidget / QMainWindow / QLabel / QShortcut / QApplication```
4. ```PyQt5.QtGui```: ```QPixmap / QDrag / QKeySequence```
5. ```PyQt5.QtMultimedia```: ```QSound```
6. ```copy```: ```copy()```
7. ```sys```
8. ```random```: ```choice() / random() / randint()```
9. ```math```: ```floor()```
10. ```os```: ```función() / módulo```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases_ventanas.py```: Contiene las clases de las ventanas
2. ```clases_objetos.py```: Contiene las clases de los objetos que no desaparecen y sus funciones
3. ```clases_objetos_temporales.py```: Contiene las clases de los objetos que desaparecen (como los clientes) y sus funciones
4. ```DCCafe.py```: Contiene la clase del dccafé y las funciones principales del juego
5. ```parametros.py```: Contiene los parametros, rutas de imagenes y datos de archivos
6. ```ventana_inicial_designer.py```: Contiene la clase de la ventana inicial

PD: Para esta tarea utilicé código de la documentacion de pyqt5 y de qt en general, y de actividades anteriores.