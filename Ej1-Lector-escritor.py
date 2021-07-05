import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Recurso1(Recurso):        # guardo la variable  en un recurso,
    dato1 = 0                  # lo inicializo en 0
    numLectores = 0              # le doy una capacidad máxima

recurso1 = Recurso1()

def condicionEscritor():                # declaro la condición para que el escritor ejecute su zona crítica
    return regionEscritor.recurso.numLectores == 0     # el número de lectores leyendo debe ser 0

def condicionLector():                  # el lector siempre puede leer
    return True

regionEscritor = RegionCondicional(recurso1, condicionEscritor)     # instancio la región condicional del escritor 
                                                                    #y le paso el recurso y la condición para ejecutar su zona crítica
regionLector = RegionCondicional(recurso1,condicionLector)         # instancio la región solo con el Recurso porque solo necesita 
                                                                     # EXCLUSIÓN MUTUA, FALLA -> lo cambio a Región condicional para que accedan al mismo recurso

@regionEscritor.condicion
def seccionCriticaEscritor():
    regionEscritor.recurso.dato1 = random.randint(0,100)
    logging.info(f'Agrego el elemento {regionEscritor.recurso.dato1}')

@regionLector.condicion
def seccionCriticaLector():
    regionLector.recurso.numLectores += 1
    logging.info(f'Lector lee dato1 = {regionLector.recurso.dato1}')
    time.sleep(1)
    regionLector.recurso.numLectores -= 1


def Escritor():
    while True:
        seccionCriticaEscritor()
        time.sleep(random.randint(1,4))

def Lector():
    while True:
        seccionCriticaLector()
        time.sleep(random.randint(3,6))


def main():
    nlector = 10
    nescritor = 2

    for k in range(nlector):
        threading.Thread(target=Lector, daemon=True).start()

    for k in range(nescritor):
        threading.Thread(target=Escritor, daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()