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

class UltimateTicTacToe(ModeloJuegoZT2):
    def inicializa(self):
        estado_inicial = [[0] * 11 for _ in range(9)]
        jugador_inicial = 1
        return estado_inicial, jugador_inicial

    def jugadas_legales(self, estado, prox_reg):
        jugadas_legales = []

        if prox_reg is None: #no hay reg prox
            for reg_idx, region in enumerate(estado):
                if region[9] == 0: # regiones no finalizadas
                    for cell_idx, val in enumerate(region[:9]):
                        if val == 0: 
                            jugadas_legales.append((reg_idx, cell_idx))
        
        else:
            region_objetivo = prox_reg
            if estado[region_objetivo][9] == 0: #si prox reg no ha finalizado se juega ahí de awebo
                return [(region_objetivo, cell_idx) for cell_idx, val in enumerate(estado[region_objetivo][:9]) if val == 0] 
            else:
                # la prox_reg ya terminó y se puede agarrar cualquiera
                for reg_idx, region in enumerate(estado):
                    if region[9] == 0:
                        for cell_idx, val in enumerate(region[:9]):
                            if val == 0:
                                jugadas_legales.append((reg_idx, cell_idx))
        return jugadas_legales

    def transicion(self, estado, jugada, jugador):
        nueva = [region.copy() for region in estado]
        reg, cell = jugada
        nueva[reg][cell] = jugador

        evaluar_ganador(nueva[reg])
        return nueva, cell
    
    def terminal(self, estado):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

        for a, b, c in combinaciones:
            if estado[a][10] == estado[b][10] == estado[c][10] != 0 and estado[a][10] != 3:
                return True
        if all(region[10] != 0 for region in estado):
            return True
        return False
    
    def ganancia(self, estado, jugador = 1):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

        for a, b, c in combinaciones:
            if estado[a][10] == estado[b][10] == estado[c][10] != 0 and estado[a][10] != 3:
                ganador = estado[a][10]
                if ganador == jugador:
                    return 1
                elif ganador != 3:
                    return -1
        if all(region[10] != 0 for region in estado):
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

def evaluar_ganador(region):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combinaciones:
            if region[a] == region[b] == region[c] != 0:
                region[10] = region[a]
                region[9] = 1
                return
        if all(cell != 0 for cell in region[:9]):
            region[10] = 3
            region[9] = 1

"""
def jugador_manual(juego, estado, ultima_celda):
    jugada = None
    jugador = 1
    print("Estado actual:")
    pprint(estado)
    print("Jugador:", jugador)

    legales = juego.jugadas_legales(estado, ultima_celda)
    print(f"Jugadas legales: {legales}")
    while True:
        entrada = input("Ingresa tu jugada como 'region celda': ")
        try:
            r, c = map(int, entrada.strip().split())
            if (r, c) in legales:
                break
            else:
                print("Jugada inválida, intenta otra jugada.")
        except:
            print("Formato inválido. Usa: region celda (ej: 0 4)")

    estado = juego.transicion(estado, jugador, (r, c))
    ultima_celda = c
    return (r, c)
"""
def jugador_manual(juego, estado, prox_reg):
    print("Estado actual:")
    pprint(estado)
    #print("Jugador:", jugador)
    legales = juego.jugadas_legales(estado, prox_reg)
    print(f"Jugadas legales: {legales}")

    while True:
        entrada = input("Ingresa tu jugada como 'region celda': ")
        try:
            r, c = map(int, entrada.strip().split())
            if (r, c) in legales:
                break
            else:
                print("Jugada inválida, intenta otra jugada.")
        except:
            print("Formato inválido. Usa: region celda (ej: 0 4)")
    return (r, c)

def jugador_minimax(juego, s, j):
    return minimax(juego, s, j)

"""
def juegar_partida():
    juego = UltimateTicTacToe()
    estado, jugador = juego.inicializa()
    prox_reg = None
    
    estado = juego.inicializa()
    while True:
        jugador = input("¿Quieres ser el jugador 1 o 2: ")
        if jugador == 1 or 2:
            break
        else:
            print("No es tan difícil decidir entre 1 y 2")
    ultima_celda = None
    
    
    print("ULTIMATE TIC-TAC-TOE")
    print(f"Las 'X' siempre empiezan y tu juegas como {'X' if jugador == 1 else 'O'}")
    
    if jugador == 1:
        g, s = juega_dos_jugadores(juego, jugador_manual, jugador_negamax)
    else:
        g, s = juega_dos_jugadores(juego, jugador_negamax, jugador_manual)
    
    print("\nSE ACABÓ EL JUEGO\n")
    pprint(s)   

    resultado = juego.ganancia(s, 1)
    if resultado == 1:
        print("¡Ganó el jugador 1!")
    elif resultado == -1:
        print("¡Ganó el jugador 2!")
    else:
        print("¡Empate!")
"""

def juegar_partida():
    juego = UltimateTicTacToe()
    estado, jugador = juego.inicializa()
    prox_reg = None                       

    print("ULTIMATE TIC-TAC-TOE")
    print(f"Las 'X' siempre empiezan y tu juegas como {'X' if jugador == 1 else 'O'}\n")

    while not juego.terminal(estado):
        if jugador == manual:  
            move = jugador_manual(juego, estado, prox_reg)
        else:
            move = jugador_negamax(juego, estado, prox_reg)
        estado, prox_reg = juego.transicion(estado, move, jugador)
        jugador = 2 if jugador == 1 else 1

    print("\n--- FIN DEL JUEGO ---\n") 
    pprint(estado)
    resultado = juego.ganancia(estado, 1)
    if resultado == 1:
        print("¡Ganó el jugador 1 (X)!")
    elif resultado == -1:
        print("¡Ganó el jugador 2 (O)!")
    else:
        print("¡Empate!")
        
if __name__ == '__main__':
    while True:
        manual = int(input("¿Quieres ser el jugador 1(X) o 2(O)?  "))
        if manual in (1,2): break
    juegar_partida()


"""
def jugar_partida():
    juego = UltimateTicTacToe()
    estado = juego.inicializa()
    jugador = 1
    ultima_celda = None

    while not juego.terminal(estado):
        print(f"\nTurno del jugador {jugador}")
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
                    print("Jugada inválida, intenta otra jugada.")
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
"""