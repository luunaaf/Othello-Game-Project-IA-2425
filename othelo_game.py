import numpy as np

class OteloGame:
    def __init__(self):
        #Inicimaliza el tablero de Othello, es un tablero 8x8 con las fichas iniciales colocadas (1 = Blanco, 2 = Negro)
        board = np.zeros((8, 8), dtype=int)
        board[3][3] = board[4][4] = 1
        board[3][4] = board[4][3] = 2 
        return board

   # def initial_state(self):


    def get_legal_moves(self, state, player):
        # Si el oponente es 1 (blanco) pues yo soy el 2 (negro) y viceversa
        opponent = 3 - player
        places = []
        # Todas las posibles direciones que una ficha puede tomar desde la casilla en la que esta
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for x in range(8):
            for y in range(8):
                # si una celda no esta vacia, me la salto
                if state[x][y] != 0:
                    continue

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    found_opponent = False
                    # mientras estemos en el tablero
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        #seguimos en la direccion donde hemos visto un oponente
                        if state[nx][ny] == opponent:
                            found_opponent = True
                        #si encontramos nuestra pieza, comprobar que haya oponentes
                        elif state[nx][ny] == player:
                            if found_opponent:
                                places.append((x, y))
                            break
                        else:
                            break
                        nx += dx
                        ny += dy

                    if (x, y) in places:
                        break  

        return places

    def next_state(self, state, move, player):
        new_state = state.copy()
        new_state[move[0]][move[1]] = 1 if player == 1 else 2
        return new_state

    def is_terminal(self, state):
        return np.all(state != 0)

    def get_result(self, state, perspective):
        p1 = np.sum(state == 1)
        p2 = np.sum(state == 2)
        if p1 == p2:
            return 0
        return 1 if (p1 > p2 and perspective == 1) or (p2 > p1 and perspective == -1) else -1
    
    def is_not_fully_expanded(self, game):
        return len(self.children) != len(game.get_legal_moves(self.state, self.player))
    
    def get_result(self, state, perspective):
        p1 = np.sum(state == 1)
        p2 = np.sum(state == 2)
        if p1 == p2:
            return 0
        return 1 if (p1 > p2 and perspective == 1) or (p2 > p1 and perspective == -1) else -1