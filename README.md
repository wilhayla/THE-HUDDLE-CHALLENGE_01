# THE-HUDDLE-CHALLENGE_01

QUE HICE?
Un codigo en Python que resuevle obtener el camino mas corto de un punto a otro.

QUE ALGORITMO USE?
Utilize el algoritmo A Star porque es un algoritmo que no trabaja a ciegas, sabe siempre a que distancia esta del objectivo, por lo que al explorar vecinos para evaluarlos no se expande muy ampliamente como el algoritmo BFC, y DISKSTRA. A Star utiliza el mismo algoritmo de DISKSTRA pero con la diferencia que se le agrega un elemento mas que es la heristica h, el cual se encarga de verificar a que distancia se encuentra del punto a donde se quiere llegar. Me parecio un algoritmo mas preciso y mas rapido para este challenge en particular.

QUE APRENDI?
Aprendi a utilizar la cola de prioridad, y a potenciar mis conocimiento sobre estructura de datos de tipo diccionario.


THE HUDDLE-CHALLENGE_02

Para estructurar el codigo lo dividi en dos partes.
1. Clase Matriz: se encarga te toda visualizacion de la matriz con todos su elementos, como grilla, obstaculos, posicion inicio, posicion final, y el trazado del camino, y lo imprime en consola.
2. Clase Astar_Encontrar_Camino:  se encarga basicamente de generar el camino para ir de un punto a otro. Devuelve una lista con el trayecto que utilizara para trazar el camino.

La forma de interactuar entre clases se logro utilizando el concepto de COMPOSICION DE CLASES. Basicamente consiste en pasarle un objeto creado de la clase Matriz al de la clase Astar_Encotrar_Camino. A partir de alli puedo obtener informacion necesaria escencial para que el algoritmo Astar pueda funcionar, como posicion inicio y posicion meta. Estos datos los encapsulo en dicha clase asi en ese momento la clase se Inicia con sus atributos propios dentro de la clase.
