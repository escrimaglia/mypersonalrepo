# Arbol de Expansión Eínima (AEM)
# El rótulo de los nodos puede ser numérico o alfanumérico
# By Ed Scrimaglia and IA (parte gráfica)

import matplotlib.pyplot as plt
import networkx as nx
from typing import Any

class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = []
        self.mapeo = {}
        self.inv_mapeo = {}

    def agregar_arista(self, u: Any, v: Any, costo: int) -> None:
        if u not in self.mapeo:
            self.mapear_nodo(u)
        if v not in self.mapeo:
            self.mapear_nodo(v)

        self.grafo.append([self.mapeo[u], self.mapeo[v], costo])

    def mapear_nodo(self, nodo: Any) -> None:
        idx = len(self.mapeo) + 1
        self.mapeo[nodo] = idx
        self.inv_mapeo[idx] = nodo

    def encontrar(self, parent: list, i: int) -> int:
        if parent[i] == i:
            return i
        parent[i] = self.encontrar(parent, parent[i])
        return parent[i]

    def union(self, parent: list, rank: list, x: int, y: int) -> None:
        raiz_x = self.encontrar(parent, x)
        raiz_y = self.encontrar(parent, y)

        if raiz_x != raiz_y:
            if rank[raiz_x] < rank[raiz_y]:
                parent[raiz_x] = raiz_y
            elif rank[raiz_x] > rank[raiz_y]:
                parent[raiz_y] = raiz_x
            else:
                parent[raiz_y] = raiz_x
                rank[raiz_x] += 1

    def kruskal(self) -> None:
        resultado = []
        i, e = 0, 0

        # Ordenar las aristas por costo
        self.grafo = sorted(self.grafo, key=lambda arista: arista[2])

        # Inicializar subconjuntos
        parent = list(range(len(self.mapeo) + 1))
        rank = [0] * (len(self.mapeo) + 1)

        while e < len(self.mapeo) - 1 and i < len(self.grafo):
            u, v, costo = self.grafo[i]
            i += 1
            x = self.encontrar(parent, u)
            y = self.encontrar(parent, v)

            if x != y:
                e += 1
                resultado.append([u, v, costo])
                self.union(parent, rank, x, y)

        print("Aristas en el árbol de expansión mínima:")
        for u, v, costo in resultado:
            print(f"{self.inv_mapeo[u]} -- {self.inv_mapeo[v]} = {costo}")
        
        self.graficar(resultado)

    def graficar(self, aristas: list) -> None:
        G = nx.Graph()

        # Añadir nodos y aristas al grafo
        for u, v, costo in aristas:
            G.add_edge(self.inv_mapeo[u], self.inv_mapeo[v], weight=costo)

        pos = nx.spring_layout(G)
        
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray', linewidths=2, width=2)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)
        
        costo_total = sum(costo for _, _, costo in aristas)
        
        plt.title("Árbol de Expansión Mínima", fontsize=16, fontweight='bold', loc='center')

        # Añadir la anotación del costo total
        plt.text(
            0.5, 0.05, f"Distancia total: {costo_total}", 
            horizontalalignment='center', verticalalignment='center', 
            fontsize=14, fontweight='bold', color='black',
            transform=plt.gca().transAxes
        )
        
        plt.subplots_adjust(top=0.85)
        plt.draw()
        plt.show()

if __name__ == "__main__":
    # Crear un grafo con identificadores alfanuméricos
    grafo = Grafo(12)
    
    # Agregar aristas con identificadores alfanuméricos
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

    grafo.kruskal()
