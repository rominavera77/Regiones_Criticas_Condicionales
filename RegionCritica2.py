import threading
import time
import logging
import contextlib     # se importa para poder usar el método with del objeto lock de la clase Threading

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Recurso
class recurso1():           # coloco las variables en una clase, uso variables de clase,                        
    variable1 = 0          #siempre usa las mismas variables
    variable2 = 0
    lock=threading.Lock()

# region id_region do
# begin
#       codigo
# end

def region(do):
    def wrapper():                                                          # uso variables de clase->recurso1.lock
        with recurso1.lock:                                                  # with aquiere el lock y lo libera
            logging.info(f'{recurso1.lock}, {recurso1.lock.locked()}')       # muestra el estado del lock -> True
            do()                                                # llama a la función callable que está en @region
            logging.info(f'variable1 = {recurso1.variable1}')
        logging.info(f'{recurso1.lock}, {recurso1.lock.locked()}')          # muestra el estado del lock -> False
    return wrapper


@region                         #declaro una región
def miFuncion():
    recurso1.variable1 += 1         #uso variables de clase -> recurso1.variable1

@region                         #declaro otra región
def miFuncion2():
    logging.info(f'variable1 = {recurso1.variable1}')




def funcion():              #implementación, corre en el hilo
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
print(recurso1.variable1, recurso1.variable2)



