import numpy as np
from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
#from minimax import minimax_iterativo

class UltimateTicTacToe(ModeloJuegoZT2):
    def inicializa(self):
        self.tablero = np.zeros((3, 3, 3, 3), dtype=int) 
        self.jugador = 1
        return (self.tablero, self.jugador)
    
    def jugadas_legales(self, s, j):
        jugadas_legales = []
        for i in range(3):
            for j in range(3):
                if np.any(s[i][j] == 0): #si hay un tavlero vacio
                    for x in range(3):
                        for y in range(3):
                            if s[i][j][x][y] == 0: #si hay una celda vacia en el tablero
                                jugadas_legales.append((i,j,x,y))
        return jugadas_legales
    
    def transicion(self, s, a, jug):
        nuevo_tablero = s.copy()
        i, j, x, y = a
        nuevo_tablero[i][j][x][y] = jug
        return nuevo_tablero
    
    def terminal(self, s):
        return self.es_ganador(1) or self.es_ganador(2) or np.all(s != 0)
    
    def ganancia(self, s):
        if self.es_ganador(1):
            return 1
        elif self.es_ganador(2):
            return -1
        else:
            return 0
        
    #cuenta como evalua??
    def es_ganador(self, jugador):
        for i in range(3):
            for j in range(3):
                if np.all(self.tablero[i][j] == jugador):
                    return True
        
        for i in range(3):
            if np.all(self.tablero[i, :, :, :] == jugador) or np.all(self.tablero[:, i, :, :] == jugador):
                return True
            
        if np.all(np.diagonal(self.tablero, axis1=0, axis2=1) == jugador) or np.all(np.diagonal(np.fliplr(self.tablero), axis1=0, axis2=1) == jugador):
            return True
        
        return False
    
    #hacer bonito despues
    def pprint_tablero(tablero):
        for i in range(3):
            for j in range(3):
                print(f"Tablero {i},{j}:")
                print(tablero[i][j])
                print()
    
    #definir funcion pa jugar
def juega_ultimate_tic_tac_toe():
    print("vamo a jugar")

if __name__ == '__main__':
    juega_ultimate_tic_tac_toe()