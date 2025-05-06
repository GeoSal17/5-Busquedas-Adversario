from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from juegos_simplificado import minimax
from minimax import jugador_negamax


"""
[
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 0]  # R0
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R5
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # R8
]

region[0] a region[8]: juego
region[9]: terminó (0 no, 1 si) 
region[10]: ganador (0 ninguno, 1, 2, 3 empate)

0 1 2 | 0 1 2 | 0 1 2 
3 4 5 | 3 4 5 | 3 4 5 
6 7 8 | 6 7 8 | 6 7 8 
---------------------
0 1 2 | 0 1 2 | 0 1 2
3 4 5 | 3 4 5 | 3 4 5
6 7 8 | 6 7 8 | 6 7 8
---------------------
0 1 2 | 0 1 2 | 0 1 2
3 4 5 | 3 4 5 | 3 4 5
6 7 8 | 6 7 8 | 6 7 8
"""

# ¿CÓMO IMPLEMENTAR PROXIMA REGION?????
# COMO DIFERENCIAR LA JUGADA DE CUANDO SE PUEDE ESCOGER REGION Y CUANDO NO

class UltimateTicTacToe(ModeloJuegoZT2):
    def inicializa(self):
        return [[0] * 11 for _ in range(9)]

    def jugadas_legales(self, estado, prox_reg):
        jugadas_legales = []

        if prox_reg is None:
            for r_idx, region in enumerate(estado):
                if region[10] == 0: #no hay region prox
                    for c_idx, val in enumerate(region[:9]):
                        if val == 0:
                            jugadas_legales.append((r_idx, c_idx))
        
        else:
            region_objetivo = prox_reg
            if estado[region_objetivo][10] == 0:
                return [(region_objetivo, c_idx) for c_idx, val in enumerate(estado[region_objetivo][:9]) if val == 0]
            else:
                # la prox_reg ya terminó y se puede agarrar cualquiera
                for r_idx, region in enumerate(estado):
                    if region[10] == 0:
                        for c_idx, val in enumerate(region[:9]):
                            if val == 0:
                                jugadas_legales.append((r_idx, c_idx))
        return jugadas_legales

    def transicion(self, estado, jugador, jugada):
        nueva = [region.copy() for region in estado]
        r, c = jugada
        nueva[r][c] = jugador
        verificar_ganador_local(nueva[r])
        return nueva
    
    def terminal(self, estado):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combinaciones:
            if estado[a][9] == estado[b][9] == estado[c][9] != 0 and estado[a][9] != 3:
                return True
        if all(region[9] != 0 for region in estado):
            return True
        return False
    
    def ganancia(self, estado, jugador):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combinaciones:
            if estado[a][9] == estado[b][9] == estado[c][9] != 0 and estado[a][9] != 3:
                ganador = estado[a][9]
                if ganador == jugador:
                    return 1
                elif ganador != 3:
                    return -1
        if all(region[9] != 0 for region in estado):
            return 0  # empate global
        return None  # continua si no ha terminado
    
def pprint(tablero):
    def celda_a_str(valor, idx):
        if valor == 1:
            return 'X'
        elif valor == 2:
            return 'O'
        else:
            return str(idx)

    filas = []
    for fila_grande in range(3):  # regiones horizontales
        for fila_pequena in range(3):  # filas dentro de la región
            fila = []
            for col_grande in range(3):  # regiones verticales
                region = 3 * fila_grande + col_grande
                for col_pequena in range(3):  # celdas dentro de la región
                    idx = 3 * fila_pequena + col_pequena
                    valor = tablero[region][idx]
                    fila.append(celda_a_str(valor, idx))
                if col_grande < 2:
                    fila.append('|')
            filas.append(' '.join(fila))
        if fila_grande < 2:
            filas.append('-' * 23)
    
    print('\n'.join(filas))

def verificar_ganador_local(region):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combinaciones:
            if region[a] == region[b] == region[c] != 0:
                region[9] = region[a]
                region[10] = 1
                return
        if all(cell != 0 for cell in region[:9]):
            region[9] = 3
            region[10] = 1

def jugar_partida():
    juego = UltimateTicTacToe()
    estado = juego.inicializa()
    jugador = 1
    ultima_celda = None

    print("\nULTIMATE TIC-TAC-TOE\n")

    print("Lamentablemente no pude lograr que funcionara con el negamax. Creo que me sería más fácil")
    print("crear mi propio negamax para que funcione mi juego que intentar implementar este, pero a")
    print("falta de tiempo no lo hice. Sin embargo, considero que será un buen problema a resolver en")
    print("un futuro cercano con más tiempo.")
    print("(Aún se pueden ver mis intentos para que jalara el negamax en los commits para que me tengan piedad:c)\n")
    print("Por el momento no me queda más opción que dejar el juego del Ultimate Tic-Tac-Toe")
    print("completamente funcional para 2 jugadores manuales. Está divertido hasta para jugar uno solo:D\n")

    while not juego.terminal(estado):
        print(f"\nVa el jugador {jugador} que juega como {'las X' if jugador == 1 else 'los O'}")
        pprint(estado)

        legales = juego.jugadas_legales(estado, ultima_celda)
        print(f"Jugadas legales: {legales}")

        while True:
            entrada = input("Ingresa tu jugada como 'region celda': ")
            try:
                r, c = map(int, entrada.strip().split())
                if (r, c) in legales:
                    break
                else:
                    print("Jugada inválida, intenta otra vez.")
            except:
                print("Formato inválido. Usa: region celda (ej: 0 4)")

        estado = juego.transicion(estado, jugador, (r, c))
        ultima_celda = c
        jugador = 2 if jugador == 1 else 1

    pprint(estado)
    resultado = juego.ganancia(estado, 1)
    if resultado == 1:
        print("¡Ganó el jugador 1!")
    elif resultado == -1:
        print("¡Ganó el jugador 2!")
    else:
        print("¡Empate!")

if __name__ == '__main__':
    jugar_partida()
