import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class RecursoDato(Recurso):
    dato1 = 0
    numLectores = 0

datos = RecursoDato()

def condicionLector():
    return True

def condicionEscritor():
    return regionEscritor.recurso.numLectores == 0

regionLector = RegionCondicional(datos, condicionLector)
regionEscritor = RegionCondicional(datos, condicionEscritor)


@regionLector.condicion
def doLector1():
    datos.numLectores += 1

@regionLector.condicion
def doLector2():
    datos.numLectores -= 1

@regionEscritor.condicion
def doEscritor():
    regionEscritor.recurso.dato1 = random.randint(0,100)
    logging.info(f'Escritor escribe dato1 = {regionEscritor.recurso.dato1}')

def Lector():
    while True:
        doLector1()
        logging.info(f'Lector lee dato1 = {regionLector.recurso.dato1}')
        time.sleep(1)
        doLector2()
        time.sleep(random.randint(3,6))

def Escritor():
    while True:
        doEscritor()
        time.sleep(random.randint(1,4))



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