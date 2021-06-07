# Regiones Críticas Condicionales

La programación concurrente consiste en controlar (al acceder a las Secciones Críticas):

- **Exclusión Mutua**
- **Condición de Sincronización**

**Sección Crítica:** Secciones de código donde se accede a recursos visibles por todos los hilos/procesos pero que no pueden ser utilizados por mas de un proceso a la vez.

### Las primitivas básicas en los lenguajes de programación son:

- **Mutex  ( Lock )**
- **Semáforos**
  En general, se puede resolver todo con Semáforos, ya que un Mutex se puede implementar con un semáforo binario (inicializado en 1)

Con estas primitivas básicas se pueden resolver problemas de **Exclusión Mútua** y **Condiciones de Sincronización**.

Si se utilizan únicamente estas primitivas, es responsabilidad del programador elegir correctamente las variables y semáforos/mutex que permitan resolver las condiciones de sincronización y situaciones de exclusión mútua.

En programas complejos, esto se torna muy complicado de resolver como así también de depurar errores.

Los semáforos se utilizan de la misma forma para resolver para exclusión mutua y sincronización, por lo que no es fácil determinar que semáforos se utilizan para exclusión mutua y cuales para condiciones de sincronización-

Son necesarios entonces, mecanismos que permitan al programador tratar en forma diferente los problemas de sincronización y el acceso exclusivo a la sección crítica.

**Regiones Críticas Condicionales**:  Son mecanismos estructurados que permiten diferenciar el control de acceso a la sección crítica de la implementación de las condiciones de sincronización.

*Se describen a continuación las estructuras para implementar estos mecanismos utilizando pseudocódigo, que puede traducirse a lenguajes de programación de alto nivel. Se mantienen algunas primitivas en inglés, ya que en algunos lenguajes existen expresiones similares.*

## Recursos

Para asegurar el acceso y uso correcto de las Variables Compartidas, las mismas se declaran de una manera especial, agrupandolas en ***resources*** (recursos).

> **resource** <id_recurso> : var1, var2, var2....

- Una variable NO puede estar en 2 recursos a la vez
- Todas las variables compartidas tienen que estar en un recurso.

## Región
Las variables definidas en recursos se tienen que acceder de una forma especial, utilizando la construcción ***region*** (región)

> **region** <id_recurso> **do*
> 
> **begin**
>
> >Operaciones con las variable que pertenecen al recurso **id_recurso**
>
> **end**

Ejemplo:

    resource Variables: var1, var2
    
    region Variables do
    begin
    	var1 += 1	
    	var2 = var1 * 5
    end

- Todo lo que se ejecuta dentro de la región, se ejecuta en **exclusión mutua**.
- Si un proceso quiere ejecutar una región, y está libre, procede a ejecutarla, si está ocupada, se bloquea y se coloca en la **cola principal**.
- Hay una cola principal por **recurso**. Si hay n regiones asociadas al mismo recurso, todas los procesos que se bloquean al intentar accederlas se colocan en la cola principal del recurso.
- Este esquema resuelve en forma estructurada la **Exclusión Mutua** únicamente.

## Implementación en Python

En el presente repositorio se encuentran los ejemplos de implementación que vimos durante la clase del 4/4:

1 - Implementación utilizando una función ***decorator*** y los recursos como variables globales

    RegionCritica1.py

2 -  Implementación utilizando una función ***decorator*** y los recursos agrupados en una clase sin instanciar (variables de clase)

    RegionCritica2.py

3 -  Implementación utilizando una *clase* ***decorator*** y los recursos agrupados en una clase instanciada (variables de instancia)

    RegionCritica3.py

### Código complementario para los ejercicios:
1 - Módulo ***region*** que provee clases para instanciar regiones críticas con acceso protegido a recursos.

    region.py

2 - Ejemplo de uso del módulo que muestra la implementación de contadores concurrentes utilizando la clase Region para implementar acceso a recurso en regiones con exclusión mútua.

Se muestran los ejemplos utilizando recursos derivados de la clase Recurso, y con otros  
tipos de recursos (por ejemplo listas).

    Region-Ejemplo_de_Uso.py


## Región Condicional

La estructura ***region*** descripta más arriba solo resuelve la exclusión mútua. Para resolver las condiciones de sincronización hay que utilizar regiones críticas condicionales:

> **region** *\<id_recurso\>* **with** *\<condicion\>*  **do**
> **begin**
> > operaciones con variables compartidas pertenecientes al recurso ***id_recurso***
>
> **end**

***<condición>*** es una expresión booleana, que permite implementar la condición de sincronización.

1 - Antes de entrar a la región, el proceso tiene que obtener el acceso con exclusión mutua a la región, si no lo consigue (por que esta ocupada por otro proceso) se bloquea y se coloca en la **cola principal** (del recurso).

2 - Si obtiene acceso a la región, evalúa la condición y si es verdadera prosigue con las instrucciones de la región. Si es falsa, libera la exclusión mútua de la región y se bloquea en otra cola asociada a la región: **cola de eventos**.

3 - Cuando un proceso termina de ejecutar la región, primero comprueba si puede desbloquear y ceder la exclusión mutua a alguno de los procesos bloqueados en la **cola de eventos**. Para esto, reevalúa la condición para cada uno de los procesos en la cola. Si ningún proceso puede ser desbloqueado, cede la exclusión mutua al primer proceso que está en la cola principal. Si no hay procesos en la cola principal, la región queda liberada esperando otros procesos.

## Implementación en Python

En el repositorio hay un ejemplo de implementación de Regiones Críticas Condicionales.

1 Modulo ***regionCondicional*** implementa clases para instanciar Regiones Críticas y Regiones Críticas Condicionales para implementar soluciones que requieren Exclusión Mútua y Condiciones de Sincronización.

    regionCondicional.py

2 - Ejemplo de uso del módulo que muestra la implementación de la solución al problema Productor/Consumidor.

    Productor-Consumidor-Ejemplo.py


## Ejercicios:

### Ejercicio 1
Implementar la solución del siguiente problema de Lectores/Escritor utilizando las clases del módulo ***RegionCondicional***:

- Lectores y Escritores acceden todos a una variable ***datos1***.
- Cuando un escritor tiene acceso a ***datos1***, le carga un valor entero aleatorio entre 0 y 100 .
- Cuando un lector tiene acceso a ***datos1*** , imprime el valor que leyó.
- Los **escritores** deben acceder a ***datos1*** con exclusión mútua y **solo si no hay lectores leyendo.** (prioridad de lectura).
- Los lectores tienen acceso simultáneo a ***datos1*** y no necesitan exclusión mútua entre ellos al leer esta variable. Además tienen prioridad sobre los escritores. Si un escritor quiere acceder a ***datos1*** tiene que esperar a que todos los lectores hayan terminado de leer.
- Para asegurar la prioridad, se utiliza una variable ***numLectores***, que cuenta la cantidad de lectores leyendo ***datos1***. Los lectores si necesitan acceder con exclusión mutua a ***numLectores.***

Nota: El módulo ***RegionCondicional***, incluye también las clase ***Region*** para implementar regiones no condicionales.

El siguiente archivo tiene el esqueleto de la solución, pero sin control de concurrencia (si bien se ejecuta, su salida es totalmente inconsistente por que no se controlan el acceso a las secciones críticas ni las condiciones de sincronización:

    Ejercicio1.py

**Nota:** respetar los retardos (sleep) colocados, ya que fueron elegidos para minimizar condiciones de inanición.

Algunas Pistas:

- El lector tiene prioridad sobre el escritor, por lo que no necesita comprobar ninguna condición de sincronización para acceder a la región, solo necesita asegurar la exclusión mutua. Esto equivale a decir que la condición del Lector es siempre verdadera.
- Por otro lado los escritores antes de acceder a la región tienen que comprobar que no haya lectores leyendo (numLectores = 0).
- En el esqueleto las variables compartidas (datos1 y numLectores) están declaradas como globales. Es recomendable que modifiquen el código, reemplazandolas por variables instanciadas en una clase derivada de Recurso.
- Los lectores no tienen que controlar exclusion mútua a datos1, pero si a numLectores, por lo tanto los accesos de los lectores a datos1 tienen que estar fuera de las regiones de los lectores.


### Ejercicio 2
Implementar la solución al Ejercicio 1 pero dando prioridad a los Escritores.
- Lectores y Escritores acceden todos a una variable ***datos1***.
- Cuando un escritor tiene acceso a ***datos1***, le carga un valor entero aleatorio entre 0 y 100 .
- Cuando un lector tiene acceso a ***datos1*** , imprime el valor que leyó.
- Los **escritores** deben acceder a ***datos1*** con exclusión mútua.
- Los lectores tienen acceso simultáneo a ***datos1*** y no necesitan exclusión mútua entre ellos al leer esta variable.
- Los escritores tienen prioridad sobre los lectores. Si un lector quiere acceder a ***datos1*** tiene que esperar a que todos los escritores hayan terminado.


### Ejercicio 3
Implementar la solución al problema de los filósofos cenando utilizando las clases del módulo ***RegionCondicional***
- Los tenedores se pueden representar con un array o lista ***tenedores*** de valores booleanos y cada filósofo comprobar que están libres los tenedores [i] e [i + 1].

 
