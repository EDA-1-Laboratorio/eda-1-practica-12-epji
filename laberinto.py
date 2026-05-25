"""
Práctica 12 – Estrategias para la construcción de algoritmos II
Módulo  : Parte 3 – El ratón en el laberinto

Instrucciones generales
    Implementa las funciones en el orden en que aparecen.
    Los comentarios guiados te explican cómo razonar cada paso.
    La visualización del backtracking es OBLIGATORIA; es el corazón
    de esta parte de la práctica.

Ejecuta este archivo directamente para ver los resultados:
    python3 laberinto.py
"""

import time

# ============================================================
# LABERINTO DE PRUEBA (ya definidos — no modificar)
# ============================================================

# 0 = celda libre, 1 = pared
LABERINTO_5x5 = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]

LABERINTO_SIN_SALIDA = [
    [0, 0, 0],
    [0, 1, 1],
    [0, 1, 0],
]

LABERINTO_SIMPLE = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


# ============================================================
# PARTE 3A y 3B – BACKTRACKING Y VISUALIZACIÓN
# ============================================================

def imprimir_laberinto(laberinto: list, visitados: set,
                      ruta: list, paso: int) -> None:
    """
    Imprime el estado actual del laberinto durante el backtracking.
    """
    filas = len(laberinto)
    cols  = len(laberinto[0])
    ruta_set = set(ruta)  # conversión a set para búsqueda O(1)

    # PASO 1 – Imprime el encabezado del paso.
    print(f"\n--- Paso {paso} ---")

    # PASO 2 – Recorre las filas y columnas para imprimir el símbolo correspondiente.
    for i in range(filas):
        fila_simbolos = []
        for j in range(cols):
            if i == 0 and j == 0:
                fila_simbolos.append('S')
            elif i == filas - 1 and j == cols - 1:
                fila_simbolos.append('E')
            elif laberinto[i][j] == 1:
                fila_simbolos.append('#')
            elif (i, j) in ruta_set:
                fila_simbolos.append('·')
            elif (i, j) in visitados:
                fila_simbolos.append('*')
            else:
                fila_simbolos.append('.')
        print(" ".join(fila_simbolos))


def existe_camino(laberinto: list, fila: int, col: int,
                  visitados: set, ruta: list, verbose: bool = False, pasos: list = None) -> bool:
    """
    Determina si existe un camino de (fila, col) a la salida.
    """
    filas = len(laberinto)
    cols  = len(laberinto[0])

    # PASO 1a – Verifica si (fila, col) está FUERA de los límites del laberinto.
    if fila < 0 or fila >= filas or col < 0 or col >= cols:
        return False

    # PASO 1b – Verifica si la celda es una PARED.
    if laberinto[fila][col] == 1:
        return False

    # PASO 1c – Verifica si la celda ya fue VISITADA.
    if (fila, col) in visitados:
        return False

    # PASO 1d – Verifica si llegamos a la SALIDA.
    if fila == filas - 1 and col == cols - 1:
        ruta.append((fila, col))
        if verbose and pasos is not None:
            pasos[0] += 1
            imprimir_laberinto(laberinto, visitados, ruta, pasos[0])
        return True

    # PASO 2 – Marca la celda como visitada.
    visitados.add((fila, col))
    ruta.append((fila, col))

    # Visualización si verbose está activo
    if verbose and pasos is not None:
        pasos[0] += 1
        imprimir_laberinto(laberinto, visitados, ruta, pasos[0])
        time.sleep(0.1)  # Pequeña pausa opcional para poder apreciar el flujo visual

    # PASO 3 – Explora recursivamente los cuatro vecinos.
    # Direcciones: abajo (1,0), derecha (0,1), arriba (-1,0), izquierda (0,-1)
    direcciones = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for df, dc in direcciones:
        nueva_fila = fila + df
        nueva_col  = col + dc
        if existe_camino(laberinto, nueva_fila, nueva_col, visitados, ruta, verbose, pasos):
            return True  # Propagamos el éxito hacia arriba

    # PASO 4 – BACKTRACK: ningún vecino condujo a la salida.
    ruta.pop()
    # Dejamos la celda en 'visitados' pero la quitamos de 'ruta' para que la
    # visualización de la Parte 3B muestre el rastro '*' (celda descartada).
    # Si quisieras limpiar visitados por completo usarías: visitados.discard((fila, col))
    
    if verbose and pasos is not None:
        pasos[0] += 1
        imprimir_laberinto(laberinto, visitados, ruta, pasos[0])
        time.sleep(0.1)

    return False


def encontrar_camino(laberinto: list, verbose: bool = False) -> list | None:
    """
    Wrapper que inicializa estructuras y llama a existe_camino.
    """
    visitados = set()
    ruta = []
    pasos = [0]  # Contador mutable para la visualización paso a paso

    if existe_camino(laberinto, 0, 0, visitados, ruta, verbose, pasos):
        return ruta
    return None


# ============================================================
# PARTE 3C – CONTAR TODOS LOS CAMINOS
# ============================================================

def contar_caminos(laberinto: list, fila: int, col: int, visitados: set) -> int:
    """
    Cuenta todos los caminos distintos de (fila, col) a la salida.
    """
    filas = len(laberinto)
    cols  = len(laberinto[0])

    # PASO 1a – Fuera de límites → return 0
    if fila < 0 or fila >= filas or col < 0 or col >= cols:
        return 0

    # PASO 1b – Pared → return 0
    if laberinto[fila][col] == 1:
        return 0

    # PASO 1c – Ya visitada → return 0
    if (fila, col) in visitados:
        return 0

    # PASO 2 – Marca como visitada.
    visitados.add((fila, col))

    # PASO 3 – ¿Llegamos a la salida?
    if fila == filas - 1 and col == cols - 1:
        cantidad = 1  # Encontramos UN camino completo
    else:
        cantidad = 0
        # Exploramos las 4 direcciones sumando sus resultados
        for df, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            cantidad += contar_caminos(laberinto, fila + df, col + dc, visitados)

    # PASO 4 – SIEMPRE backtrack: desmarcamos para permitir otras rutas válidas
    visitados.discard((fila, col))

    # PASO 5 – return cantidad
    return cantidad


# ============================================================
# EXPERIMENTOS
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("PARTE 3A – Buscar un camino en LABERINTO_5x5")
    print("=" * 50)
    camino = encontrar_camino(LABERINTO_5x5, verbose=False)
    if camino:
        print(f"  Camino encontrado ({len(camino)} pasos):")
        print(f"  {camino}")
    else:
        print("  No existe camino.")

    print("\n" + "=" * 50)
    print("PARTE 3B – Visualización paso a paso (laberinto simple 3x3)")
    print("=" * 50)
    camino_simple = encontrar_camino(LABERINTO_SIMPLE, verbose=True)
    if camino_simple:
        print(f"\n  Camino final: {camino_simple}")

    print("\n" + "=" * 50)
    print("PARTE 3A – Laberinto sin salida")
    print("=" * 50)
    camino_ns = encontrar_camino(LABERINTO_SIN_SALIDA)
    if camino_ns is None:
        print("  Correctamente detectado: no existe camino. ✓")
    else:
        print(f"  ERROR: debería ser None, se obtuvo {camino_ns}")

    print("\n" + "=" * 50)
    print("PARTE 3C – Contar todos los caminos")
    print("=" * 50)
    for nombre, lab in [("simple 3x3", LABERINTO_SIMPLE),
                        ("5x5 con paredes", LABERINTO_5x5)]:
        total = contar_caminos(lab, 0, 0, set())
        print(f"  {nombre}: {total} camino(s)")

    print()
    print("  Reflexión: caminos_bottom_up(3,3) de la Parte 2 = 6 (solo abajo/derecha)")
    print("  contar_caminos(LABERINTO_SIMPLE) con 4 direcciones da 12.")
    print("  ¿Por qué son distintos? Escribe la respuesta en tu reporte.")
