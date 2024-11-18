# Dijkstra para el cálculo de la menor distancia entre dos nodos (origin y final)
# Se imprime la menor distancia entre ambos
# Se grafica el grafo
# El rótulo de los nodos puede ser numérico o alfanumérico
# Se seleccionan el nodo origen y el nodo final
# By Ed Scrimaglia and IA (parte gráfica)

import heapq
import networkx as nx
import matplotlib.pyplot as plt
from typing import Any, Tuple
from networkx.drawing.nx_agraph import graphviz_layout

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

    def dijkstra(self, inicio: Any, final: Any) -> Tuple[float, dict[Any, Any]]:
        distancias = {nodo: float('infinity') for nodo in self.grafo}
        distancias[inicio] = 0
        predecesores = {nodo: None for nodo in self.grafo}
        cola_prioridad = [(0, inicio)]
        procesados = set()

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

            if nodo_actual == final:
                return distancias[final], predecesores

            if nodo_actual in procesados:
                continue

            procesados.add(nodo_actual)

            for vecino, costo in self.grafo[nodo_actual]:
                nueva_distancia = distancia_actual + costo

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        return float('infinity'), predecesores

    def reconstruir_camino(self, predecesores: dict[Any, Any], nodo_final: Any) -> list:
        camino = []
        nodo_actual = nodo_final
        while nodo_actual is not None:
            camino.insert(0, nodo_actual)
            nodo_actual = predecesores[nodo_actual]
        return camino

    # Graficar grafo tipo circular (IA)
    def graficar_grafo_circular(self, distancia_total: int, nodo_origen: str, camino_resaltado: list = []) -> None:
        G = nx.DiGraph() if self.dirigido else nx.Graph()

        for origen in self.grafo:
            for destino, costo in self.grafo[origen]:
                G.add_edge(origen, destino, weight=costo)

        # Layout Circular
        pos = nx.circular_layout(G)

        # Tamaño del gráfico
        plt.figure(figsize=(13, 8))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray', width=2)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos , edge_labels=edge_labels, font_color='red', font_size=12)

        if camino_resaltado:
            camino_edges = [(camino_resaltado[i], camino_resaltado[i+1]) for i in range(len(camino_resaltado) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=camino_edges, edge_color='blue', width=2)
            nx.draw_networkx_nodes(G, pos, nodelist=camino_resaltado, node_color='yellow', node_size=600)
            camino_edge_labels = {edge: edge_labels[edge] for edge in camino_edges if edge in edge_labels}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=camino_edge_labels, font_color='blue', font_size=12)

        if not nodo_origen in camino_resaltado:
            nx.draw_networkx_nodes(G, pos, nodelist=[nodo_origen], node_color='yellow', node_size=600)

        plt.text(
            0.5, 0.05, f"Menor distancia: {distancia_total}", 
            horizontalalignment='center', verticalalignment='center', 
            fontsize=14, fontweight='bold', color='black',
            transform=plt.gca().transAxes
        )

        plt.title("Grafo con el camino más corto resaltado", fontsize=12, fontweight='bold')
        plt.show()

    # Graficar grafo tipo Arbol (IA)
    def graficar_grafo_arbol(self, distancia_total: int, nodo_origen: str, camino_resaltado: list = []) -> None:
        G = nx.DiGraph() if self.dirigido else nx.Graph()

        for origen in self.grafo:
            for destino, costo in self.grafo[origen]:
                G.add_edge(origen, destino, weight=costo)

        # Layout jerárquico
        pos = graphviz_layout(G, prog='dot')

        # Tamaño del gráfico
        plt.figure(figsize=(13, 8))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray', width=2)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)

        if camino_resaltado:
            camino_edges = [(camino_resaltado[i], camino_resaltado[i+1]) for i in range(len(camino_resaltado) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=camino_edges, edge_color='blue', width=2)
            nx.draw_networkx_nodes(G, pos, nodelist=camino_resaltado, node_color='yellow', node_size=600)
            camino_edge_labels = {edge: edge_labels[edge] for edge in camino_edges if edge in edge_labels}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=camino_edge_labels, font_color='blue', font_size=12)

        if not nodo_origen in camino_resaltado:
            nx.draw_networkx_nodes(G, pos, nodelist=[nodo_origen], node_color='yellow', node_size=600)

        plt.text(
            0.5, 0.05, f"Menor distancia: {distancia_total}", 
            horizontalalignment='center', verticalalignment='center', 
            fontsize=14, fontweight='bold', color='black',
            transform=plt.gca().transAxes
        )

        plt.title("Grafo en formato jerárquico con el camino más corto resaltado", fontsize=12, fontweight='bold')
        plt.show()

if __name__ == "__main__":
    dirigido = True
    tipo_grafico = "circular"

    grafo = Grafo(dirigido)
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

    nodo_inicial = "CO"
    nodo_final = "MJ"

    distancia, predecesores = grafo.dijkstra(nodo_inicial, nodo_final)

    tipo_grafo = "dirigido" if dirigido else "no dirigido"
    camino = grafo.reconstruir_camino(predecesores, nodo_final)
    
    if distancia < float('infinity'):
        print (f"El camino más corto desde {nodo_inicial} hasta {nodo_final} es: {camino}. La distancia es {distancia}")
    else:
        print (f"No hay camino desde el nodo {nodo_inicial} al nodo {nodo_final}")
       
    if tipo_grafico.lower() == "circular":
        grafo.graficar_grafo_circular(distancia, nodo_inicial, camino_resaltado=camino)
    elif tipo_grafico.lower() == "arbol":
        grafo.graficar_grafo_arbol(distancia, nodo_inicial, camino_resaltado=camino)
    else:
        print ("Tipo de gráfico debe ser Circular o Arbol")
