import threading
import time
import logging
import contextlib

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Recurso
variable1 = 0
variable2 = 0
lock=threading.Lock()

# region id_region do
# begin
#       codigo
# end

def region(do):
    global lock
    def wrapper():
        with lock:
         #   logging.info(f'{lock}, {lock.locked()}')
            do()
       # logging.info(f'{lock}, {lock.locked()}')
    return wrapper


@region
def miFuncion():
    global variable1
    variable1 += 1

@region
def miFuncion2():
    global variable1
    logging.info(f'variable1 = {variable1}')




def funcion():
    global variable1
    for i in range(1000000):
        miFuncion()



hilos = []

for i in range(4):
    t = threading.Thread(target=funcion)
    t.start()
    hilos.append(t)

for k in hilos:
    k.join()

miFuncion2()


