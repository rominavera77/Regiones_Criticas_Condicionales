import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Recurso1(Recurso):
    elementos = []
    maxElementos = 10

recurso1 = Recurso1()

def condicionProductor():
    return len(recurso1.elementos) < recurso1.maxElementos

def condicionConsumidor():
    return len(recurso1.elementos) > 0


regionProductor = RegionCondicional(recurso1, condicionProductor)
regionConsumidor = RegionCondicional(recurso1, condicionConsumidor)

@regionProductor.condicion
def seccionCriticaProductor():
    regionProductor.recurso.elementos.append(random.randint(0,100))
    logging.info(f'Hay {len(regionProductor.recurso.elementos)} elementos, : {regionProductor.recurso.elementos}')

@regionConsumidor.condicion
def seccionCriticaConsumidor():
    logging.info(f'Retiro el elemento {regionConsumidor.recurso.elementos.pop(0)}, longitud de lista {len(regionConsumidor.recurso.elementos)}')


def Productor():
    while True:
        seccionCriticaProductor()
        time.sleep(random.randint(1,2))

def Consumidor():
    while True:
        seccionCriticaConsumidor()
        time.sleep(random.randint(1,5))


threading.Thread(target=Productor, daemon=True).start()
threading.Thread(target=Consumidor, daemon=True).start()

time.sleep(300)