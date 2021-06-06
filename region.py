import threading

""" 
Este módulo implementa clases para instanciar Regiones Críticas con acceso protegido a recursos.

"""

class Region(object):
    ''' Clase Region, define una región asociada a un Recurso (conjunto de variables) protejido por
    un Lock que puede pertenecer al Recurso o ser provisto en al instanciar la clase.

    Al instanciar esta clase:
    - Si se le pasa un objeto recurso R1 derivado de la clase Recurso, utilizará por defecto el lock que
    contiene R1 por lo que no es necesario especificarlo (a no ser que se quiera utilizar otro lock):
    Por ejemplo:
    Creación del Recurso:
    class r1(Recurso):
        variable1 = 0
        variable2 = 0
    R1 = r1()

    Creación de la Región (no es necesario pasar un lock, ya que utilizará el del objeto R1
    region = Region(R1)


    - Si se le pasa un recurso de cualquier otra clase R2, es obligatorio pasarle además un lock.
    Por ejemplo:
    El recurso a pasar es una lista:

    lista = [10, 20, "N"]     # Recurso lista
    lock_lista = threading.Lock()   # lock para proteger la lista
    region = Region(lista, lock_lista)

    Implementación de la Region (instrucciones)
    La clase Region provee un método decorador (region) para implementar la región.
    El código a ejecutar en la Región se debe implementar en una función.
    Está función debe ser decorada antes de ser utilizada por el programa. De esa forma se garantiza
    el acceso al recurso con exclusión mútua.

    Ejemplo:

    region1 = Region(recurso1)

    @region1.region
    def funcionZona()
        # instrucciones que acceden a recurso1

    En el programa principal o código del hilo:
    ...
    funcionZona()
    ...

    '''
    def __init__(self, recurso, lock = None):
        self.recurso = recurso
        if lock == None:
            self.lock = recurso.lock
        else:
            self.lock = lock


    def region(self, do):
        def wrapper():
            with self.lock:
                do()
        return wrapper


class Recurso(object):
    '''
    Clase Recurso para crear conjuntos de variables compartidas asociadas a un Lock.
    Al heredar de esta clase, la clase derivada tendrá un lock asociado que utilizará
    por defecto las instancias de la clase Region.
    Cualquier acceso o referencia a las variables del recurso deben ser realizadas siempre
    a través de instancias de esta clase.

    Por ejemplo:
    Agrupación de variables en clase derivada de Recurso
    class r1(Recurso):
        variable1 = 0
        variable2 = 0

    Instanciación de un recurso:
    R1 = r1()

    Acceso a las variables_
    R1.variable1 = 0

    El lock asociado (heredado) se puede referenciar como R1.lock
    Ejemplo:
    with R1.lock
        R1.variable2 += 10
    '''
    def __init__(self):
        self.lock = threading.Lock()







