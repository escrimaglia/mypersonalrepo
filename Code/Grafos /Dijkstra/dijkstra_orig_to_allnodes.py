# Algoritmo de Dijkstra para el cálculo de la menor distancia entre un nodo inicial y todos los demas
# Se imprime la menor distancia entre el nodo inicial y cada uno de los demas nodos
# El rótulo de los nodos puede ser numérico o alfanumérico
# Se selecciona el nodo origen
# By Ed Scrimaglia

import heapq
from typing import Any

class Grafo:
    def __init__(self, dirigido: bool = True):
        self.grafo = {}
        self.dirigido = dirigido

    def agregar_arista(self, origen: Any, destino: Any, costo: int) -> None:
        if origen not in self.grafo:
            self.grafo[origen] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[origen].append((destino, costo))
        if not self.dirigido:
            self.grafo[destino].append((origen, costo))

    def dijkstra(self, inicio: Any) -> dict[Any,(None, float)]:
        distancias = {nodo: float('infinity') for nodo in self.grafo}
        distancias[inicio] = 0
        predecesores = {nodo: None for nodo in self.grafo}
        cola_prioridad = [(0, inicio)]
        procesados = set()

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
            # El nodo ya fue procesado y se ignora
            if nodo_actual in procesados:
                continue

            procesados.add(nodo_actual)
            for vecino, costo in self.grafo[nodo_actual]:
                distancia = distancia_actual + costo

                # Si la ruta hacia el vecino es mas corta
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (distancia, vecino))

        return distancias, predecesores

    def reconstruir_camino(self, predecesores: dict[Any,None], nodo_final: Any) -> list:
        #Reconstruir el camino más corto desde el nodo inicial hasta nodo_final
        camino = []
        nodo_actual = nodo_final
        while nodo_actual is not None:
            camino.insert(0, nodo_actual)
            nodo_actual = predecesores[nodo_actual]
        return camino

if __name__ == "__main__":
    # Crear el tipo de grafo
    dirigido = True
    grafo = Grafo(dirigido)
    
    # Agregar aristas (origen, destino, costo)
    grafo.agregar_arista("CO", "FR", 565)
    grafo.agregar_arista("CO", "VM",702)
    grafo.agregar_arista("CO", "R4", 210)
    grafo.agregar_arista("CO", "R3", 153)
    grafo.agregar_arista("CO", "CP", 397)
    grafo.agregar_arista("CO", "CA", 347)
    grafo.agregar_arista("CP", "CA", 187)
    grafo.agregar_arista("CP", "FU", 252)
    grafo.agregar_arista("CP", "R3", 244)
    grafo.agregar_arista("CP", "MJ", 164)
    grafo.agregar_arista("R3", "MJ", 248)
    grafo.agregar_arista("R3", "R4", 135)
    grafo.agregar_arista("RO", "R4", 121)
    grafo.agregar_arista("RO", "MJ", 360)
    grafo.agregar_arista("RO", "SF", 486)
    grafo.agregar_arista("RO", "VM", 351)
    grafo.agregar_arista("RO", "VT", 365)
    grafo.agregar_arista("CA", "FU", 287)
    grafo.agregar_arista("VM", "VT", 238)
    grafo.agregar_arista("VM", "FR", 165)
    grafo.agregar_arista("SF", "MJ", 312)
    grafo.agregar_arista("SF", "FU", 640)

    nodo_inicio = "CO"

    msg = "Grafo dirigido:"
    if not dirigido:
        msg = f"Grafo no dirigido:"

    distancias, predecesores = grafo.dijkstra(nodo_inicio)

    print (f"Tipo de grafo: {msg}")
    print (f"Nodo de inicio: {nodo_inicio}")
    for nodo, distancia in distancias.items():
        if distancia < float('infinity'):
            camino = grafo.reconstruir_camino(predecesores, nodo)
            print (f"La distancia desde el nodo {nodo_inicio} al nodo {nodo} es {distancia}, camino: {camino}")
        else:
            print (f"No hay camino desde el nodo {nodo_inicio} al nodo {nodo}")
