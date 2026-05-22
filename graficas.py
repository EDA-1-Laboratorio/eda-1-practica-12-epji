"""
Práctica 12 – Estrategias para la construcción de algoritmos II
Módulo  : Experimento gráfico — T(n) medido vs cota teórica Big O

Instrucciones
    Este módulo genera gráficas que contrastan el tiempo de ejecución
    medido experimentalmente contra la función teórica que lo acota (Big O).

    La idea central de Big O es geométrica:
        T(n) = O(f(n))  si existe una constante c > 0 tal que
        T(n) ≤ c · f(n)  para todo n suficientemente grande.

    En cada gráfica verás:
        — Una curva de puntos: el tiempo medido T(n).
        — Una curva sólida:    c · f(n), la cota teórica escalada.
    Si la implementación es correcta, la curva medida quedará siempre
    POR DEBAJO de la cota teórica.

Requisito
    pip install matplotlib   (o: python3 -m pip install matplotlib)

Ejecuta este archivo directamente:
    python3 graficas.py
"""

import time
import math
import sys

try:
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
except ImportError:
    print("ERROR: matplotlib no está instalado.")
    print("Instálalo con:  python3 -m pip install matplotlib")
    sys.exit(1)

# Importa las funciones que ya implementaste en los otros módulos.
# Si aún no las tienes implementadas, este archivo fallará con un error
# de importación — completa primero los otros módulos.
try:
    from fibonacci_escaleras import fib_recursivo, fib_memo, fib_bottom_up
    from caminos_cuadricula  import caminos_recursivo, caminos_memo, caminos_bottom_up
    from n_reinas            import contar_soluciones
except ImportError as e:
    print(f"Error al importar módulos de la práctica: {e}")
    print("Asegúrate de ejecutar este archivo desde la misma carpeta que los demás.")
    sys.exit(1)


# ============================================================
# UTILIDAD DE MEDICIÓN
# ============================================================

def medir(funcion, *args, repeticiones: int = 5) -> float:
    """
    Retorna el tiempo promedio (en segundos) de ejecutar funcion(*args).
    """
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(*args)
        tiempos.append(time.perf_counter() - inicio)
    return sum(tiempos) / len(tiempos)


# ============================================================
# FUNCIÓN AUXILIAR: ESCALAR LA COTA TEÓRICA
# ============================================================
#
# CÓMO PENSARLO:
#   La cota teórica f(n) (por ejemplo, 2ⁿ) puede estar en unidades
#   completamente distintas a los segundos de T(n). Para compararlas
#   visualmente, necesitamos encontrar la constante c tal que:
#
#       c · f(n)  quede "justo por encima" de todos los puntos T(n).
#
#   Una forma simple: elige c como el máximo de T(n)/f(n) sobre todos
#   los valores medidos, y multiplica por un factor de holgura (1.2 ó 2)
#   para que la cota siempre quede visible por encima.
#
#   Esta constante c no tiene interpretación física precisa; su propósito
#   es puramente visual: mostrar que T(n) ≤ c · f(n).

def escalar_cota(ns: list, tiempos: list, f) -> list:
    """
    Calcula c · f(n) escalado para que quede por encima de todos los tiempos.

    Parámetros:
        ns      – lista de valores de n.
        tiempos – lista de T(n) medidos (misma longitud que ns).
        f       – función teórica, recibe n y devuelve un número positivo.

    Retorna:
        Lista de valores c · f(n) para cada n en ns.

    CÓMO IMPLEMENTARLO:
        1. Calcula f(n) para cada n en ns → lista fn_vals.
           Protege contra divisiones por cero: si f(n) == 0, usa 1e-12.
        2. Calcula las razones T(n)/f(n) para cada par.
        3. c = max(razones) * 1.5   (factor de holgura del 50 %)
        4. Retorna [c * f(n) para n en ns].
    """
    # PASO 1 – Evalúa f en cada n.
    #   fn_vals = [max(f(n), 1e-12) for n in ns]

    # PASO 2 – Calcula las razones T(n)/f(n).
    #   razones = [t / fn for t, fn in zip(tiempos, fn_vals)]

    # PASO 3 – Constante de escalado con holgura.
    #   c = max(razones) * 1.5

    # PASO 4 – Retorna la cota escalada.
    #   return [c * fn for fn in fn_vals]

    pass  # TODO


# ============================================================
# GRÁFICA 1: FIBONACCI — recursivo O(2ⁿ) vs memo/bottom-up O(n)
# ============================================================
#
# CÓMO PENSARLO:
#   Queremos ver en una sola gráfica las tres curvas de tiempo.
#   La recursiva debería crecer MUCHO más rápido que las otras dos.
#   Eso hace que las curvas de memo y bottom-up sean casi planas
#   si usamos el mismo eje Y.
#
#   Solución: usa DOS subgráficas (subplots):
#     - Izquierda:  solo la recursiva con su cota 2ⁿ.
#     - Derecha:    memo y bottom-up con su cota n.
#
#   Cada subgráfica tiene:
#     - Puntos/línea discontinua (--o): tiempo medido T(n).
#     - Línea sólida (—):              cota teórica c · f(n).
#     - Leyenda, etiquetas de ejes, título.

def grafica_fibonacci(ax_recursivo, ax_lineal):
    """
    Genera las subgráficas de Fibonacci en los ejes dados.

    Parámetros:
        ax_recursivo – eje matplotlib para la versión O(2ⁿ).
        ax_lineal    – eje matplotlib para las versiones O(n).

    CÓMO IMPLEMENTARLO:

    PASO 1 – Define los valores de n a medir.
        Para recursivo: range pequeño (e.g. 5, 10, 15, 20, 25, 30).
        Para memo/bottom-up: range más grande (e.g. 50, 100, ..., 500).

    PASO 2 – Mide los tiempos para cada n (usa la función medir()).
        t_rec = [medir(fib_recursivo, n) for n in ns_rec]
        etc.

    PASO 3 – Calcula las cotas teóricas con escalar_cota().
        Para recursivo: f = lambda n: 2**n
        Para lineal:    f = lambda n: n

    PASO 4 – Grafica en ax_recursivo:
        ax_recursivo.plot(ns_rec, t_rec,  '--o', label='T(n) medido')
        ax_recursivo.plot(ns_rec, cota_rec, '-',  label='c · 2ⁿ  (cota O(2ⁿ))')
        ax_recursivo.set_title('fib_recursivo — O(2ⁿ)')
        ax_recursivo.set_xlabel('n')
        ax_recursivo.set_ylabel('Tiempo (s)')
        ax_recursivo.legend()

    PASO 5 – Grafica en ax_lineal de forma similar para memo y bottom-up.
        Puedes poner las dos curvas medidas en el mismo eje para comparar.
    """
    pass  # TODO


# ============================================================
# GRÁFICA 2: CAMINOS EN CUADRÍCULA — recursivo O(2^(m+n)) vs DP O(m·n)
# ============================================================
#
# CÓMO PENSARLO:
#   Para una cuadrícula cuadrada (m = n = d), la recursión es O(2^(2d))
#   y bottom-up es O(d²).
#   Usa dimensiones d ∈ {3, 5, 7, 9, 11, 13} para el recursivo (crece rápido)
#   y d ∈ {10, 50, 100, ..., 500} para bottom-up.

def grafica_caminos(ax_recursivo, ax_dp):
    """
    Genera las subgráficas de caminos en cuadrícula.

    CÓMO IMPLEMENTARLO:
        Similar a grafica_fibonacci pero con caminos_recursivo(d, d)
        y caminos_bottom_up(d, d).

        Para el recursivo:
            f_rec = lambda d: 2 ** (2 * d)   ← O(2^(m+n)) con m=n=d

        Para bottom-up:
            Nota: caminos_bottom_up devuelve (total, tabla).
            Envuelve la llamada para medir solo el tiempo:
            medir(lambda d=d: caminos_bottom_up(d, d))

        Para DP: f_dp = lambda d: d * d    ← O(m·n) = O(d²)
    """
    pass  # TODO


# ============================================================
# GRÁFICA 3: N REINAS — contar_soluciones O(n!)
# ============================================================
#
# CÓMO PENSARLO:
#   El backtracking con poda no es exactamente n!, pero n! es la cota
#   superior sin poda. Con poda el algoritmo es mucho mejor, por lo que
#   la curva medida debería quedarse MUY por debajo de c · n!.
#   Eso también es pedagógicamente valioso: ver que la poda ayuda.
#
#   Usa n ∈ {4, 6, 8, 10, 12} (13+ es muy lento para el laboratorio).

def grafica_n_reinas(ax):
    """
    Genera la gráfica de N reinas en el eje dado.

    CÓMO IMPLEMENTARLO:
        ns = [4, 6, 8, 10, 12]
        t_reinas = [medir(contar_soluciones, n, repeticiones=1) for n in ns]

        Para la cota:
            f_fact = lambda n: math.factorial(n)
            cota = escalar_cota(ns, t_reinas, f_fact)

        Grafica T(n) medido y c · n!.
        Añade una segunda cota c · n^n como referencia (¿más ajustada?).

        Nota para el reporte: ¿por qué T(n) está TAN por debajo de n!?
        La poda descarta ramas enteras del árbol. Un nodo a profundidad k
        con m columnas inválidas elimina (n-k)! caminos de golpe.
    """
    pass  # TODO


# ============================================================
# FUNCIÓN PRINCIPAL: GENERA TODAS LAS GRÁFICAS
# ============================================================

def main():
    """
    Genera una figura con todas las gráficas de la práctica.

    CÓMO IMPLEMENTARLO:
        PASO 1 – Crea la figura y los ejes con plt.subplots o gridspec.
            fig = plt.figure(figsize=(14, 10))
            gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

            ax_fib_rec  = fig.add_subplot(gs[0, 0])
            ax_fib_lin  = fig.add_subplot(gs[0, 1])
            ax_cam_rec  = fig.add_subplot(gs[0, 2])
            ax_cam_dp   = fig.add_subplot(gs[1, 0])
            ax_reinas   = fig.add_subplot(gs[1, 1])

        PASO 2 – Llama a cada función de gráfica.
            grafica_fibonacci(ax_fib_rec, ax_fib_lin)
            grafica_caminos(ax_cam_rec, ax_cam_dp)
            grafica_n_reinas(ax_reinas)

        PASO 3 – Agrega un título general.
            fig.suptitle(
                'Práctica 12 – T(n) medido vs cota teórica Big O',
                fontsize=14, fontweight='bold'
            )

        PASO 4 – Muestra y/o guarda la figura.
            plt.savefig('grafica_p12.png', dpi=150, bbox_inches='tight')
            plt.show()
            print("Gráfica guardada en grafica_p12.png")
    """
    print("Generando gráficas... (puede tardar ~30 segundos)")

    # TODO: implementa los pasos descritos arriba.

    pass


if __name__ == "__main__":
    main()
