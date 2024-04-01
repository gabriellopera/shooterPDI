# Shooter

## Procesamiento Digital de Imagenes

## *Integrantes:*
+ Johan Andrés Asprilla
+ Gabriel Antonio Lopera Madrid

Creacion del Juego Flappy Bird https://youtu.be/jrUJ8EsnctI?si=t4wwFZ7AhnQbuo31
Basado en el Repositorio https://github.com/mundo-python/shooter-pygame

Esta version del juego Shooter, usa la cámara para captura los datos y poder controlar la nave espacial, se utiliza un objeto verde para mover la nave en el eje x y otro objeto azul para activar los disparos de la nave. La finalidad de este juego es aplicar los conocimientos adquiridos en procesamiento digital de imagenes en lo que se lleva del curso.

Para poder jugar el juego es necesario la version de Python 3.8 o superior y tener todas las librerias descargadas; esto se realiza a traves del comando `pip install XXX(libreria)` en la Terminal del IDE en el cual se hizo la implementacion y por medio de la terminal se ejecuta el comando  `python shooter.py` o simplmente al ubicarse en el archivo se le da play. Este repositorio se puede clonar en cualquier IDE (recomendamos el uso de Visual Studio Code) y se hace a traves del comando `git clone https://github.com/gabriellopera/shooterPDI.git

### IDE:
* Visual Studio Code 

### Librerias:
+ numpy
+ imutils
+ cv2 
+ pygame 
+ random
+ threading

## **Modo de Uso:**
1. Inicialmente se puede iniciar el Juego con la Tecla Space o UP.
2. Se coloca el objeto frente la camara(Debe ser de color verde y azul).
3. Se mueve el objeto verde en el eje X y el objeto azul con la simple captura comienza a disparar.

Sistema de Puntuacion:
* Cada piedra destruida sumará un score para llevar el sistema de puntuación.

Game Over:
* Si la nave pierde la vida completa (rectangulo superior izquierdo) finalizará el juego.

