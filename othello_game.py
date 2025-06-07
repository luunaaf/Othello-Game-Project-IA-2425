import numpy as np

class OthelloGame:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = 2

    def get_initial_state(self):
        return self.board.copy()

    def get_legal_moves(self, state, player):
        opponent = 3 - player
        places = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for x in range(8):
            for y in range(8):
                if state[x][y] != 0:
                    continue

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    found_opponent = False
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        if state[nx][ny] == opponent:
                            found_opponent = True
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
        legal_moves = self.get_legal_moves(state, player)
        if move not in legal_moves:
            return state  
        new_state = state.copy()
        new_state[move[0]][move[1]] = player
        self.capture_pieces(new_state, move, player)
        return new_state

    def capture_pieces(self, state, move, player):
        opponent = 3 - player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = move[0] + dx, move[1] + dy
            path = []

            while 0 <= nx < 8 and 0 <= ny < 8 and state[nx][ny] == opponent:
                path.append((nx, ny))
                nx += dx
                ny += dy

            if 0 <= nx < 8 and 0 <= ny < 8 and state[nx][ny] == player:
                for px, py in path:
                    state[px][py] = player

    def is_terminal(self, state):
        return not self.get_legal_moves(state, 1) and not self.get_legal_moves(state, 2)

    def get_result(self, state, perspective):
        result = 0
        p1 = np.sum(state == 1)
        p2 = np.sum(state == 2)
        
        if (p1 > p2 and perspective == 1) or (p2 > p1 and perspective == -1):
            result = 1
        elif (p1 < p2 and perspective == 1) or (p2 < p1 and perspective == -1):
            result = -1

        return result

    def get_next_player(self, state, current_player):
        """Devuelve el próximo jugador que puede mover. Si ninguno puede, devuelve None."""
        opponent = 3 - current_player
        if self.get_legal_moves(state, opponent):
            return opponent
        elif self.get_legal_moves(state, current_player):
            return current_player
        else:
            return None

    
    