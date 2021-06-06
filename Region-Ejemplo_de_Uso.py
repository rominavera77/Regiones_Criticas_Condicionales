import logging
from region import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

""" 
El presente ejemplo muestra la implementación de contadores concurrentes utilizando
la clase Region para implementar acceso a recurso en regiones con exclusión mútua.
Se muestran los ejemplos utilizando recursos derivados de la clase Recurso, y con otros
tipos de recursos (por ejemplo listas).
 
"""

# Creación de una clase derivada de Recurso para agrupar variables
class Recurso1(Recurso):
    variable1 = 0
    variable2 = 0

# Instanciación de un recurso con la clase derivada
recurso1 = Recurso1()

# Declaración de recurso lista (requiere un lock)
lista = [0,1]
# Declaración del lock para proteger la lista
lock1 = threading.Lock()

#Creación de una región asociada al recurso1
region1 = Region(recurso1)

#Creación de una región asociada al recurso lista
region2 = Region(lista, lock1)

#Creación del un código (función) a ejecutar en la región1 asociada a recurso1
#(protegido con el lock de recurso1)
@region1.region
def miFuncion1():
    recurso1.variable1 += 1

#Creación de otro código (función) a ejecutar en la región1 asociada a recurso1
#(protegido con el lock de recurso1)
@region1.region
def otraFuncion1():
    region1.recurso.variable2 -= 1

#Creación del un código (función) a ejecutar en la región2 asociada al recurso "lista"
#(protegido con el lock1)
@region2.region
def miFuncion2():
    region2.recurso[0] += 1
    region2.recurso[1] += 4

# Implementación de códigos para hilos que utilizan la región1 (recurso = recurso1)
def funcion():
    for i in range(1000000):
        miFuncion1()

def funcion2():
    for i in range(200000):
        otraFuncion1()

# Implementación de códigos para hilos que utilizan la región2 (recurso = lista)
def funcion3():
    for i in range(1000000):
        miFuncion2()

hilos = []
for i in range(4):
    t = threading.Thread(target=funcion)
    p = threading.Thread(target=funcion2)
    q = threading.Thread(target=funcion3)
    t.start()
    p.start()
    q.start()
    hilos.append(t)
    hilos.append(p)
    hilos.append(q)

for k in hilos:
    k.join()

#Valores finales de las variables en los recursos
print(f'recurso1.variable1 = {recurso1.variable1}')
print(f'recurso1.variable2 = {recurso1.variable2}')
print(f'lista[0] = {lista[0]}, lista[1] = {lista[1]}')




