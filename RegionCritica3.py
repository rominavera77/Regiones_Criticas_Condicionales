import threading
import time
import logging
import contextlib

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# region id_region do
# begin
#       codigo
# end


# Recurso
class recurso():
    variable1 = 0
    variable2 = 0

class region(object):
    resource = recurso()        # dentro de la clase instancio un recurso
    lock = threading.Lock()
    def __init__(self, do):     # al constructor le paso la función que voy a decorar
        self._do = do

    def __call__(self):         # devuelve todo como un ejecutable
        with region.lock:
            self._do()


@region
def miFuncion():
    region.resource.variable1 += 1


@region
def miFuncion2():
    logging.info(f'variable1 = {region.resource.variable1}')




def funcion():
    for i in range(100):
        miFuncion()


hilos = []

for i in range(4):
    t = threading.Thread(target=funcion)
    t.start()
    hilos.append(t)

for k in hilos:
    k.join()

miFuncion2()



