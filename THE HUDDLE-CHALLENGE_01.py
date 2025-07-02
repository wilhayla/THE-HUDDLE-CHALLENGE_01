import random
import heapq
import math
from math import sqrt
import colorama
from colorama import init, Fore, Back, Style
import time

colorama.init()

def definir_matriz():
    
    print(Fore.BLUE + Style.BRIGHT + Back.WHITE + "Ingrese las dimensiones de la Matriz." + Style.RESET_ALL)
    
    filas = int(input("Cantidad de filas: "))
    columnas = int(input("Cantidad de columnas: "))

    matriz = [["." for _ in range(columnas)] for _ in range(filas)]

    return matriz

def imprimir_matriz(matriz):
    
    for fila in matriz:
        print(" ".join(fila))
    print("----------------------------------------------------------------------------------------------\n")

def obtener_dimensiones_matriz(matriz):
    
    cantidad_filas = len(matriz)
    
    if cantidad_filas == 0:    # si cantidad fila es 0
        cantidad_columnas = 0  # asigno cantidad columnas a 0, para validar en el metodo insertar obstaculos
    else:
        cantidad_columnas = len(matriz[0]) 
        
    return cantidad_filas, cantidad_columnas
    
def insertar_obstaculos(matriz):
    
    cantidad_filas, cantidad_columnas = obtener_dimensiones_matriz(matriz)

    if cantidad_filas == 0 or cantidad_columnas == 0:   # validacion si la fila y columna si es 0
        print("No se pueden insertar obstáculos en una matriz vacía o inválida.")
        return matriz

    cantidad_obstaculos = int(input(Fore.BLUE + Style.BRIGHT + Back.WHITE + "Cantidad de obstaculos a insertar en la matriz: " + Style.RESET_ALL))

    total_celdas = cantidad_filas * cantidad_columnas  # calculo la cantidad de celdas en total
    
    if cantidad_obstaculos > total_celdas:   # verificicion si cantidad de onstaculos sobrepasa la cantidad total de celdas
        print(f"Advertencia: Has pedido {cantidad_obstaculos} obstáculos, pero la matriz solo tiene {total_celdas} celdas.")
        cantidad_obstaculos = total_celdas  # si sobrepasa ajusto la cantidad de obstaculos, a la cantidad total de celdas

    obstaculos_colocados = 0    # cuenta cuantos obstaculos se han insertado
    intentos = 0                # cuenta cuantas veces se ha intentado colocar un obstaculo
    max_intentos = total_celdas * 2      # limite de seguridad para evitar bucle infinito con random randint si se vuelve dificil de encotar un espacio vacio.
    
    # bucle para insertar los obstaculos
    while obstaculos_colocados < cantidad_obstaculos and intentos < max_intentos:
        fila_obstaculo = random.randint(0, cantidad_filas - 1)   # asignacion aleatoria de obstaculo x
        columna_obstaculo = random.randint(0, cantidad_columnas - 1) # asignacion aleatoria de obstaculo x

        celda_obstaculo = matriz[fila_obstaculo][columna_obstaculo]
        if celda_obstaculo != "#":
            matriz[fila_obstaculo][columna_obstaculo] = "#"
            obstaculos_colocados += 1
        
        intentos += 1 

    if obstaculos_colocados < cantidad_obstaculos:   # se verifica si se colocarion todos los obtaculos
        print(f"No se pudieron colocar los {cantidad_obstaculos - obstaculos_colocados} obstáculos restantes. La matriz está llena o hay muy pocos espacios disponibles.")
            
    return matriz

def insertar_inicio_final(matriz, cantidad_filas, cantidad_columnas):
    
    print(Fore.BLUE + Style.BRIGHT + Back.WHITE + "Ingrese las cordenas del punto de partida." + Style.RESET_ALL)
    
    inicio_filas = int(input("Fila: "))
    inicio_columnas = int(input("Columna: "))
    matriz[inicio_filas][inicio_columnas] = Fore.GREEN + "I" + Style.RESET_ALL
    posicion_inicio = (inicio_filas, inicio_columnas)
    
    print(Fore.BLUE + Style.BRIGHT + Back.WHITE + "Ingrese las cordenas del punto de llegada." + Style.RESET_ALL)
    
    meta_filas = int(input("Fila: "))
    meta_columnas = int(input("Columna: "))
    matriz[meta_filas][meta_columnas] = Fore.RED + "M" + Style.RESET_ALL
    posicion_meta = (meta_filas, meta_columnas)
    
    return matriz, posicion_inicio, posicion_meta

def crear_nodo(posicion, g=float(math.inf), h=0.0, nodo_padre=None):
    
    return {
        'posicion':posicion,
        'g': g,
        'h': h,
        'f': g + h,
        'padre': nodo_padre
        }

def calculo_heuristico(posicion_actual, posicion_meta):

    x1, y1 = posicion_actual
    x2, y2 = posicion_meta

    h = sqrt((x2-x1)**2 + (y2-y1)**2)  # distancia euclidiana 

    return h


def vecinos_validos(matriz, posicion_actual):
    x, y = posicion_actual
    cantidad_filas = len(matriz)
    cantidad_columnas = len(matriz[0])
    
    posibles_movimientos = [
        (x+1, y), (x-1, y),      # Derecha, Izquierda
        (x, y+1), (x, y-1),      # Arriba, Abajo
        (x+1, y+1), (x-1, y-1),  # Diagonales
        (x+1, y-1), (x-1, y+1)   # Diagonales
    ]
    
    movimientos_validos = []
    
    for nx, ny in posibles_movimientos:
        if 0 <= nx < cantidad_filas and 0 <= ny < cantidad_columnas:
            if matriz[nx][ny] != "#":
                movimientos_validos.append((nx, ny))

    return movimientos_validos

def reconstruccion_camino(nodo_meta):  # reconstruccion del camino desde el nodo meta
    
    camino = []
    nodo_posicion_actual = nodo_meta      # {'posicion':(x,y), 'g':g, 'h':h, 'f':f, 'padre':{'posicion':(x,y), 'g':g, 'h':h, 'f':f}}
    
    while nodo_posicion_actual is not None:  # mientras el nodo tenga un padre este bucle se ejecutara, cuando llegue al nodo inicio devolvera none porque inicion no tiene padre.
        camino.append(nodo_posicion_actual['posicion'])    
        nodo_posicion_actual = nodo_posicion_actual['padre']  # actualiza la varible nodo_poscion_actual con su nodo padre. 
                                                              # el bucle se actualiza y verifica si el nodo padre no tiene nodo padre y asi sucesivamente.
    return camino[::-1]

def encontrar_camino(matriz, posicion_inicio, posicion_meta):
    
    # inicializo el nodo de inicio, nodo a partir del cual empieza a explorar los caminos.
    # nodo_comienzo = diccionario
    nodo_comienzo = crear_nodo(posicion_inicio, g=0.0, h=calculo_heuristico(posicion_inicio, posicion_meta))
    
    # inicializo listas abiertas y cerradas
    lista_abierta = [(nodo_comienzo['f'], nodo_comienzo['posicion'])]   # (f , (x,y)) 
    diccionario_cerrado = {posicion_inicio: nodo_comienzo}    # {(x, y): {'posicion':(x,y), 'g':g, 'h':h, 'f':f, 'padre':{'posicion':(x,y), 'g':g, 'h':h, 'f':f}}}
    conjunto_eval_pos = set()   # conjunto:evita que se repitan posiciones. Optimizacion, evitar bucles infinitos y exploracion repetidas.
    
    while lista_abierta:
        costo_f, posicion_actual = heapq.heappop(lista_abierta)
        nodo_actual = diccionario_cerrado[posicion_actual]   # obtengo todos los valores de esa posicion accediento al diccionario abierto
                                                             # nodo_actual = {'posicion':(x,y), 'g':g, 'h':h, 'f':f, 'padre':{'posicion':(x,y), 'g':g, 'h':h, 'f':f}}
        if posicion_actual == posicion_meta:
            trayecto = reconstruccion_camino(nodo_actual)
            return trayecto
        else:
            conjunto_eval_pos.add(posicion_actual)
            
        # Exploracion de los vecinos a partir de la posicion actual
        for posicion_vecino in vecinos_validos(matriz, posicion_actual):
            if posicion_vecino in conjunto_eval_pos:
                continue
            
            dx = abs(posicion_vecino[0] - posicion_actual[0])   # si se mueve horizontalmente dx = 1 y dy = 0  Ej. de (2,2) a (3,2)
            dy = abs(posicion_vecino[1] - posicion_actual[1])   # si se mueve verticalmente dx = 0 y dy = 1   Ej. de (2,2) a (2,3)
                                                                # si se muevo diagonalmenete dx = 1 y dy = 1
            if dx != 0 and dy != 0:
                coste_de_moverse = math.sqrt(2)   # desplazamiento en diagonal. Teorema de pitagoras
            else:
                coste_de_moverse = 1              # desplazamiento ortogonal
                
            g_tentativo = nodo_actual['g'] + coste_de_moverse    # nodo_actual['g'] es el costo acumulado para llegar desde el punto inicio al actual.
                                                                 # g_tentativo: tentativo porque aun no se sabe si es la ruta mas corta para llegar a posicion_vecino.
            # Crear y actualizar el nuevo vecino
            if posicion_vecino not in diccionario_cerrado:
                nodo_vecino = crear_nodo(
                    posicion_vecino,
                    g_tentativo,
                    h = calculo_heuristico(posicion_vecino, posicion_meta),
                    nodo_padre = nodo_actual
                )   
                heapq.heappush(lista_abierta, (nodo_vecino['f'], posicion_vecino))
                diccionario_cerrado[posicion_vecino] = nodo_vecino    # agrego poscion vecino(clave) al diccionario con todos sus valores.
                
            elif g_tentativo < diccionario_cerrado[posicion_vecino]['g']:
                # se encontro mejor camino para esta vecino
                nodo_vecino = diccionario_cerrado[posicion_vecino]
                nodo_vecino['g'] = g_tentativo
                nodo_vecino['f'] = g_tentativo + nodo_vecino['h']
                nodo_vecino['padre'] = nodo_actual
                
    return []  # no se encontro una ruta    
            
        
# MAIN

grafico = definir_matriz()

imprimir_matriz(grafico)

insertar_obstaculos(grafico)

imprimir_matriz(grafico)

cantidad_filas, cantidad_columnas = obtener_dimensiones_matriz(grafico)

if not(cantidad_filas==0 and cantidad_columnas==0):

    matriz_con_obstaculos_inicio_meta, posicion_inicio, posicion_meta = insertar_inicio_final(grafico, cantidad_filas, cantidad_columnas)

    imprimir_matriz(matriz_con_obstaculos_inicio_meta)

    camino = encontrar_camino(matriz_con_obstaculos_inicio_meta, posicion_inicio, posicion_meta)

    if len(camino) == 0:
        print(Fore.RED + "NO SE PUDO ENCONTRAR UN CAMINO" + Style.RESET_ALL)

    for posicion in camino:
        matriz_con_obstaculos_inicio_meta[posicion[0]][posicion[1]] = Fore.CYAN + "*" + Style.RESET_ALL
        imprimir_matriz(matriz_con_obstaculos_inicio_meta)
        time.sleep(0.7)
    
    