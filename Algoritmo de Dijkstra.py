# Sofia Galilea Morales Bejarano
# Objetivo del programa:
# Desarrollar un simulador del algoritmo de Dijkstra que muestre paso a paso el proceso para encontrar 
# el camino más corto entre dos nodos de un grafo, permitiendo visualizar 
# cómo se seleccionan los nodos, cómo se actualizan las distancias y cuál 
# es la ruta mínima resultado final.

import heapq
import matplotlib.pyplot as plt

INF = float('inf')

def crear_grafo_de_ejemplo():
    """
    Grafo de ejemplo:
      A --4-- B
      |  \2
      2   C --1-- B
          | \8
          |  E
          D --2-- E --3-- Z
          \6
           Z

    Representado como diccionario de diccionarios:
    grafo[origen][destino] = peso
    """
    grafo = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
        'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
        'E': {'C': 10, 'D': 2, 'Z': 3},
        'Z': {'D': 6, 'E': 3}
    }
    return grafo

# Posiciones (x, y) para dibujar los nodos en el plano
POSICIONES = {
    'A': (0, 1),
    'B': (2, 2),
    'C': (2, 0),
    'D': (4, 1),
    'E': (6, 1),
    'Z': (8, 1),
}

def imprimir_tabla(grafo, dist, visitados, prev):
    print("Nodo | Distancia estimada | Visitado | Predecesor")
    for v in sorted(grafo.keys()):
        d = dist[v]
        d_str = "INF" if d == INF else str(d)
        pred = prev[v] if prev[v] is not None else "-"
        vis = "Sí" if v in visitados else "No"
        print(f"  {v}   | {d_str:^18} | {vis:^8} | {pred:^10}")
    print()

def reconstruir_camino(prev, origen, destino):
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        if actual == origen:
            break
        actual = prev[actual]
    camino.reverse()
    if not camino or camino[0] != origen:
        return None
    return camino

def dibujar_grafo(grafo, dist, visitados, actual=None, paso=0):
    """
    Dibuja el grafo:
    - Nodo actual en rojo
    - Nodos visitados en verde
    - Nodos no visitados en gris
    - Encima de cada nodo se muestra su distancia actual
    """
    plt.clf()  # Limpiar figura

    # Dibujar aristas
    for u in grafo:
        x_u, y_u = POSICIONES[u]
        for v, peso in grafo[u].items():
            # Para no dibujar dos veces la misma arista
            if list(grafo.keys()).index(v) <= list(grafo.keys()).index(u):
                continue
            x_v, y_v = POSICIONES[v]
            plt.plot([x_u, x_v], [y_u, y_v])
            # Etiqueta del peso en el punto medio
            xm, ym = (x_u + x_v) / 2, (y_u + y_v) / 2
            plt.text(xm, ym + 0.1, str(peso), ha='center', fontsize=9)

    # Dibujar nodos
    for nodo, (x, y) in POSICIONES.items():
        if nodo == actual:
            color = 'red'       # nodo actual
        elif nodo in visitados:
            color = 'green'     # ya visitado
        else:
            color = 'lightgray' # pendiente

        plt.scatter(x, y, s=500, edgecolors='black')
        plt.scatter(x, y, s=400, color=color)

        # Texto del nodo
        plt.text(x, y, nodo, ha='center', va='center', fontsize=12, weight='bold')

        # Mostrar distancia arriba del nodo
        d = dist[nodo]
        d_str = "INF" if d == INF else str(d)
        plt.text(x, y + 0.4, f"d={d_str}", ha='center', fontsize=9)

    plt.title(f"Algoritmo de Dijkstra - Paso {paso}")
    plt.axis('off')
    plt.tight_layout()
    plt.pause(1.5)  # Pausa para que se vea la animación

def dijkstra_paso_a_paso(grafo, origen):
    dist = {v: INF for v in grafo}
    prev = {v: None for v in grafo}
    dist[origen] = 0
    visitados = set()
    cola_prioridad = [(0, origen)]
    paso = 0

    print("=== Simulación paso a paso del algoritmo de Dijkstra ===")
    print(f"Nodo origen: {origen}\n")
    imprimir_tabla(grafo, dist, visitados, prev)

    # Preparar figura de matplotlib
    plt.ion()           # Modo interactivo
    plt.figure(figsize=(8, 3))
    dibujar_grafo(grafo, dist, visitados, actual=None, paso=paso)

    while cola_prioridad:
        distancia_actual, u = heapq.heappop(cola_prioridad)

        if u in visitados:
            continue

        paso += 1
        print(f"--- Paso {paso}: seleccionamos el nodo '{u}' con distancia actual {distancia_actual} ---")
        visitados.add(u)

        # Dibujar estado actual
        dibujar_grafo(grafo, dist, visitados, actual=u, paso=paso)
        imprimir_tabla(grafo, dist, visitados, prev)

        # Relajación
        for v, peso in grafo[u].items():
            if v in visitados:
                continue
            nueva_distancia = dist[u] + peso
            print(f"Revisando arista {u} -> {v} (peso {peso}). "
                  f"Nueva distancia posible: {dist[u]} + {peso} = {nueva_distancia}")
            if nueva_distancia < dist[v]:
                print(f"  Mejora! Actualizamos distancia de {v}: {dist[v]} -> {nueva_distancia} "
                      f"y predecesor {prev[v]} -> {u}")
                dist[v] = nueva_distancia
                prev[v] = u
                heapq.heappush(cola_prioridad, (nueva_distancia, v))

        print()
        imprimir_tabla(grafo, dist, visitados, prev)

    print("=== Resultado final ===")
    imprimir_tabla(grafo, dist, visitados, prev)

    for destino in sorted(grafo.keys()):
        if destino == origen:
            continue
        camino = reconstruir_camino(prev, origen, destino)
        if camino is None:
            print(f"No hay camino desde {origen} hasta {destino}.")
        else:
            print(f"Camino mínimo de {origen} a {destino}: {' -> '.join(camino)} "
                  f"(costo = {dist[destino]})")

    # Dejar la última imagen fija hasta que cierres la ventana
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    grafo = crear_grafo_de_ejemplo()
    origen = 'A'
    dijkstra_paso_a_paso(grafo, origen)
