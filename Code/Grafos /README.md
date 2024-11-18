# Algoritmos para resolver problemas de Grafos

![plot](./Figura/Grafo.png)

## Dijkstra: resolución de problemas de camino mas corto (shortest path)

- El gráfico puede ser de tipo circular o jerárquico (árbol)

- Cuando en el gráfico tipo Jerárquico, se note una superposición de aristas, cambiar a tipo de gráfico circular

- El grafo puede ser dirigido o no dirigido

- Se deben ingresar las aristas en formato (origen, destina, costo)

### Código Dijkstra

- dijkstra_orig_to_allnodes.py: resuelve el shortest path entre el nodo original y cada nodo del grafo e imprime el resultado en consola

- Se debe seleccionar nodo origen

- dijkstra_orig_dest.py: resuelve el shortest path entre el nodo original y el nodo final

- Se deben seleccionar nodo origen y nodo destino

##

## Kruskal: resolución de problemas de Arbol de Expansión Mínima

- Se deben ingresar las aristas en formato (origen, destina, costo)

### Código Kruskal

- arbol_expansion_minima.py: grafica e imprime en consola el AEM y calcula la distancia total
