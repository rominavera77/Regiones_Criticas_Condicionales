import threading

""" 
Este módulo implementa clases para instanciar Regiones Críticas y Regiones Críticas Condicionales
para implementar soluciones que requieren Exclusión Mútua y Condiciones de Sincronización.
"""

# Region Crítica (no condicional)
class Region(object):
    ''' Clase Region, define una región asociada a un Recurso (conjunto de variables) protejido por
    un Lock que puede pertenecer al Recurso o ser provisto en al instanciar la clase.

    PseudoCódigo
    ----------------------------------------------
    region <recurso> do
    ... instrucciones
    ----------------------------------------------

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
            self.lock = recurso.mutex
        else:
            self.lock = lock

    def region(self, do):
        def wrapper():
            with self.lock:
                do()
        return wrapper


class Recurso(object):
    '''
    Clase "Recurso" para crear conjuntos de variables compartidas asociadas a un Mutex (lock o semáforo).

    Los recursos (variables u objetos) a proteger se los debe agrupar en una clase heredada de esta clase.

    Al heredar de esta clase, la clase derivada tendrá un Mutex asociado que utilizará por defecto las
    instancias de la clase Region.

    !!!El uso de esta clase es OBLIGATORIO cuando se instancian regiones críticas condicionales con la clase
    "RegionCondicional". !!!!

    Lor herencia de la clase "Recurso" incluye todos los objetos necesarios (semáforos y contadores) para
    implementar Regiones Condicionales con la clase "RegionCondicional"

    Por ejemplo:
    Agrupación de variables en clase derivada de Recurso
    class r1(Recurso):
        variable1 = 0
        variable2 = 0

    Instanciación de un recurso:
    R1 = r1()

    Acceso a las variables_
    R1.variable1 = 0

    '''
    def __init__(self):
        self.mutex = threading.Semaphore(1)
        self.wait = threading.Semaphore(0)
        self.count = 0
        self.temp = 0

# Region Crítica (no condicional)
class RegionCondicional():
    ''' Clase RegionCondicional, define una región asociada a un Recurso (conjunto de variables) y una Condición
    (función que retorna una valor booleano) implementando los accesos con exclusión mútua al recurso y condiciones
    de sincronización.

    PARA INSTANCIAR ESTA CLASE ES OBLIGATORIO UTILIZAR RECURSOS DERIVADOS DE LA CLASE Recurso

    La clases derivadas de Recurso, heredan todos los objetos necesarios (semáforos y contadores) para implementar
    la Región Crítica Condicional.

    PseudoCódigo
    ----------------------------------------------
     region <recurso> with <condition> do
     ... instrucciones
    ----------------------------------------------

    Pasos Para implementar una región condicional:

    1 - Agrupar las variables y objetos compartidos en una "instancia" de una clase derivada de la clase Recurso
        Por ej:     #Declarar la clase rerivada de Recurso
                    class miRecurso(Recurso):
                        miVariable1 = 0
                        miLista = []

                    #Instanciar el Recurso
                    unRecurso = miRecurso()

    2 - Declarar una función que retorne un valor booleano de acuerdo a la condición que se quiera implementar:
        Por ej:      def condicion1()
                        return unRecurso.miVariable1 > 0

    3 - Instanciar la región crítica condicional con el recurso y la condición:
        Por ej:     regionCondicional1 = RegionCondicional(miRecurso, condicion1)

    Nota: Si hay varias condiciones a sincronizar con el mismo recurso, se deben crear varias instancias de
        RegiónCondicional, una por cada condición y **todas asociadas al mismo recurso**.

    4 - Implementación del código de la región.
        La clase Region provee un método decorador (condicion) que implementa y controla la región condicional.
        El código a ejecutar, se debe implementar en una función, y luego esta función debe ser decorada con el
        decorador "condicion" de la instancia de la clase.  Esto asegurar la exclusión mútua y la condición de
        sincronización asociada correspondiente.
        Por ej:     @regionCondicional1.condicion
                        def seccionCritica1():
                            regionCondicional1.recurso.miLista.append(10)


    En el programa principal o código del hilo se podrá incluir esta función en forma segura y sincronizada:
    ...
    seccionCritica1()
    ...
    '''
    def __init__(self, recurso, condition):
        self.condition = condition
        self.recurso = recurso

    def condicion(self, do):
        def wrapper():
            self.recurso.mutex.acquire()
            if not(self.condition()):
                self.recurso.count += 1
                self.recurso.mutex.release()
                self.recurso.wait.acquire()
                while not(self.condition()):
                    self.recurso.temp += 1
                    if self.recurso.temp < self.recurso.count:
                        self.recurso.wait.release()
                    else:
                        self.recurso.mutex.release()
                    self.recurso.wait.acquire()
                self.recurso.count = self.recurso.count-1
    #Codigo region critica
            do()
    #Fin Código región critica
            if self.recurso.count > 0:
                self.recurso.temp = 0
                self.recurso.wait.release()
            else:
                self.recurso.mutex.release()
        return wrapper