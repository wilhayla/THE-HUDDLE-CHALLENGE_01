import random
import heapq
import math
from math import sqrt
import colorama
from colorama import init, Fore, Back, Style
init(autoreset=True)
import time

class Matriz:
    def __init__(self, filas, columnas):
        self.cantidad_filas = filas
        self.cantidad_columnas = columnas
        self.punto_inicio = "I"
        self.punto_meta = "M"
        self.obstaculo = "#"
        self.espacio_libre = "."
        self.simbolo_camino = "*" 
        self.matriz = [[self.espacio_libre for _ in range(self.cantidad_columnas)] for _ in range(self.cantidad_filas)]
        self.posicion_inicio = None
        self.posicion_meta = None

    def __str__(self):
        filas_strings = []
        for fila in self.matriz:
            fila_con_colores = []
            for celda in fila:
                # Aplicar colores para la visualización basándose en el contenido puro
                if celda == self.punto_inicio:
                    fila_con_colores.append(Fore.GREEN + celda + Style.RESET_ALL)
                elif celda == self.punto_meta:
                    fila_con_colores.append(Fore.RED + celda + Style.RESET_ALL)
                elif celda == self.obstaculo:
                    fila_con_colores.append(Fore.YELLOW + Back.BLACK + celda + Style.RESET_ALL)
                elif celda == self.simbolo_camino:
                    fila_con_colores.append(Fore.CYAN + celda + Style.RESET_ALL)
                else: # Espacio libre
                    fila_con_colores.append(celda) 
            filas_strings.append(" ".join(fila_con_colores))
        return "\n".join(filas_strings) + "\n----------------------------------------------------------------------------------------------\n"
    
    def insertar_obstaculos(self):
        while True:
            try:
                cantidad_obstaculos = int(input(Fore.BLUE + Style.BRIGHT + Back.WHITE + "Cantidad de obstaculos a insertar en la matriz: " + Style.RESET_ALL))
                if cantidad_obstaculos <= 0:
                    print(Fore.RED + "La cantidad de obstaculos no puede ser igual o menor a 0." + Style.RESET_ALL)
                    continue
                break
            except ValueError:
                print(Fore.RED + "Entrada invalida. Ingrese un numero entero." + Style.RESET_ALL)

        total_celdas = self.cantidad_filas * self.cantidad_columnas

        if cantidad_obstaculos > total_celdas: 
            print(Fore.RED + f"Advertencia: Has pedido {cantidad_obstaculos} obstáculos, pero la matriz solo tiene {total_celdas} celdas." + Style.RESET_ALL)
            cantidad_obstaculos = total_celdas

        obstaculos_colocados = 0
        intentos = 0
        max_intentos = total_celdas * 2 

        while obstaculos_colocados < cantidad_obstaculos and intentos < max_intentos:
            fila_obstaculo = random.randint(0, self.cantidad_filas - 1)
            columna_obstaculo = random.randint(0, self.cantidad_columnas - 1)
            
            # Solo compara el contenido puro
            if self.matriz[fila_obstaculo][columna_obstaculo] == self.espacio_libre:
                self.matriz[fila_obstaculo][columna_obstaculo] = self.obstaculo
                obstaculos_colocados += 1

            intentos += 1 

        if obstaculos_colocados < cantidad_obstaculos:
            print(Fore.RED + f"No se pudieron colocar los {cantidad_obstaculos - obstaculos_colocados} obstáculos restantes. La matriz está llena o hay muy pocos espacios disponibles." + Style.RESET_ALL)

    def insertar_inicio_final(self):
        # INICIO
        while True:
            print(Fore.BLUE + Style.BRIGHT + Back.WHITE + "Ingrese las coordenadas del punto de partida." + Style.RESET_ALL)
            try:
                inicio_fila = int(input("Fila: "))
                inicio_columna = int(input("Columna: "))
                self.posicion_inicio = (inicio_fila, inicio_columna)

                if not (0 <= inicio_fila < self.cantidad_filas and 0 <= inicio_columna < self.cantidad_columnas):
                    print(Fore.RED + "Coordenadas fuera de los límites de la matriz. Intente de nuevo." + Style.RESET_ALL)
                    continue
                
                # Compara el contenido puro
                if self.matriz[inicio_fila][inicio_columna] == self.obstaculo: 
                    print(Fore.RED + "Posición incorrecta. No puede coincidir con un obstáculo. Intente de nuevo." + Style.RESET_ALL)
                    continue

                self.matriz[inicio_fila][inicio_columna] = self.punto_inicio # Sin códigos de color aquí
                break

            except ValueError:
                print(Fore.RED + "Entrada inválida. Ingrese números enteros para las coordenadas." + Style.RESET_ALL)

        # META
        while True:
            print(Fore.BLUE + Style.BRIGHT + Back.WHITE + "Ingrese las cordenas del punto de llegada." + Style.RESET_ALL)
            try:
                meta_fila = int(input("Fila: "))
                meta_columna = int(input("Columna: "))
                self.posicion_meta = (meta_fila, meta_columna)

                if not (0 <= meta_fila < self.cantidad_filas and 0 <= meta_columna < self.cantidad_columnas):
                    print(Fore.RED + "Coordenadas fuera de los límites de la matriz. Intente de nuevo." + Style.RESET_ALL)
                    continue
                
                # Compara el contenido puro
                if self.matriz[meta_fila][meta_columna] == self.obstaculo: 
                    print(Fore.RED + "Posición incorrecta. No puede coincidir con un obstáculo. Intente de nuevo." + Style.RESET_ALL)
                    continue
                
                # Asegurarse de que meta no sea el mismo que inicio
                if self.posicion_inicio == self.posicion_meta:
                    print(Fore.RED + "La posición de llegada no puede ser igual a la de partida. Intente de nuevo." + Style.RESET_ALL)
                    continue

                self.matriz[meta_fila][meta_columna] = self.punto_meta # Sin códigos de color aquí
                
                break

            except ValueError:
                print(Fore.RED + "Entrada inválida. Por favor, ingrese números enteros para las coordenadas." + Style.RESET_ALL)  

    # Nuevo método para mostrar el camino encontrado
    def mostrar_camino(self, camino):
        if not camino:
            print(Fore.RED + "No se encontró un camino para mostrar." + Style.RESET_ALL)
            return

        print(Fore.CYAN + Style.BRIGHT + "Camino encontrado (animación):" + Style.RESET_ALL)
        
        # Copiar la matriz actual si quieres poder restaurarla después
        # matriz_original = [fila[:] for fila in self.matriz]

        for r, c in camino:
            # No sobrescribir el punto de inicio o meta con el marcador del camino
            if (r, c) == self.posicion_inicio or (r, c) == self.posicion_meta:
                continue
            
            self.matriz[r][c] = self.simbolo_camino # Guarda el símbolo puro en la matriz

            print(self) # __str__ se encarga de aplicar los colores
            time.sleep(0.7) 
        
        # Opcional: Si quieres restaurar la matriz a su estado inicial sin el camino marcado
        # self.matriz = matriz_original

class AStar_Buscar_Camino:
    def __init__(self, mapa): # COMPOSICION de clase, la clase Astar recibe un objeto de la clase matriz
        self.mapa = mapa # self.mapa es la instancia de Matriz
        self.filas = mapa.cantidad_filas
        self.columnas = mapa.cantidad_columnas
        self.posicion_inicio = mapa.posicion_inicio
        self.posicion_meta = mapa.posicion_meta
        self.obstaculo = mapa.obstaculo

    def crear_nodo(self, posicion, g=float(math.inf), h=0.0, nodo_padre=None):
        return {
            'posicion': posicion,
            'g': g,
            'h': h,
            'f': g + h,
            'padre': nodo_padre
        }
    
    def calculo_heuristico(self, posicion_actual, posicion_meta):
        x1, y1 = posicion_actual
        x2, y2 = posicion_meta
        h = sqrt((x2-x1)**2 + (y2-y1)**2)  # distancia euclidiana 
        return h

    # Este método ya no necesita recibir el objeto matriz como parámetro
    def vecinos_validos(self, posicion_actual):
        x, y = posicion_actual
        
        posibles_movimientos = [
            (x+1, y), (x-1, y),     # Derecha, Izquierda
            (x, y+1), (x, y-1),     # Arriba, Abajo
            (x+1, y+1), (x-1, y-1),  # Diagonales
            (x+1, y-1), (x-1, y+1)   # Diagonales
        ]

        movimientos_validos = []

        for nx, ny in posibles_movimientos:
            if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                # Accede directamente a la matriz interna del objeto Matriz (self.mapa)
                if self.mapa.matriz[nx][ny] != self.obstaculo: # Compara contenido puro
                    movimientos_validos.append((nx, ny))

        return movimientos_validos

    def reconstruccion_camino(self, nodo_meta):  
        camino = []
        nodo_posicion_actual = nodo_meta      
        while nodo_posicion_actual is not None:  
            camino.append(nodo_posicion_actual['posicion'])    
            nodo_posicion_actual = nodo_posicion_actual['padre']                                       
        return camino[::-1]
    
    def encontrar_camino(self):
        nodo_comienzo = self.crear_nodo(self.posicion_inicio, g=0.0, h=self.calculo_heuristico(self.posicion_inicio, self.posicion_meta))
        lista_abierta = [(nodo_comienzo['f'], nodo_comienzo['posicion'])]   
        diccionario_cerrado = {self.posicion_inicio: nodo_comienzo}     
        conjunto_eval_pos = set()   

        while lista_abierta:
            costo_f, posicion_actual = heapq.heappop(lista_abierta)
            nodo_actual = diccionario_cerrado[posicion_actual]   
                                                                    
            if posicion_actual == self.posicion_meta:
                trayecto = self.reconstruccion_camino(nodo_actual)
                return trayecto
            else:
                conjunto_eval_pos.add(posicion_actual)

            # Llama a vecinos_validos sin el parámetro 'self.mapa'
            for posicion_vecino in self.vecinos_validos(posicion_actual): 
                if posicion_vecino in conjunto_eval_pos:
                    continue
                
                dx = abs(posicion_vecino[0] - posicion_actual[0])   
                dy = abs(posicion_vecino[1] - posicion_actual[1])   
                                                                    
                if dx != 0 and dy != 0:
                    coste_de_moverse = math.sqrt(2)   
                else:
                    coste_de_moverse = 1              

                g_tentativo = nodo_actual['g'] + coste_de_moverse     
                                                                        
                if posicion_vecino not in diccionario_cerrado:
                    nodo_vecino = self.crear_nodo(
                        posicion_vecino,
                        g_tentativo,
                        h = self.calculo_heuristico(posicion_vecino, self.posicion_meta),
                        nodo_padre = nodo_actual
                    )   
                    heapq.heappush(lista_abierta, (nodo_vecino['f'], posicion_vecino))
                    diccionario_cerrado[posicion_vecino] = nodo_vecino     

                elif g_tentativo < diccionario_cerrado[posicion_vecino]['g']:
                    nodo_vecino = diccionario_cerrado[posicion_vecino]
                    nodo_vecino['g'] = g_tentativo
                    nodo_vecino['f'] = g_tentativo + nodo_vecino['h']
                    nodo_vecino['padre'] = nodo_actual

        return []
    
# MAIN
while True:
    try:
        filas = int(input("Cantidad de filas: "))
        columnas = int(input("Cantidad de columnas: "))
        if filas <= 0 or columnas <= 0:
            print(Fore.RED + "Inserte una cantidad valida distinto a 0." + Style.RESET_ALL)
            continue
        break
    except ValueError:
        print(Fore.RED + "Entrada inválida. Por favor, ingrese un número entero." + Style.RESET_ALL)

matriz = Matriz(filas, columnas)
print(matriz)
matriz.insertar_obstaculos()
print(matriz)
matriz.insertar_inicio_final()
print(matriz)

camino_buscador = AStar_Buscar_Camino(matriz)
camino = camino_buscador.encontrar_camino()

if not camino:
    print(Fore.RED + "NO SE PUDO ENCONTRAR UN CAMINO" + Style.RESET_ALL) 
else:
    # Llama al nuevo método de la clase Matriz para mostrar el camino
    matriz.mostrar_camino(camino)   # colaboracion de clases
    
print(Fore.CYAN + Style.BRIGHT + "El camino encotrado es:" + Style.RESET_ALL)
print(camino)

