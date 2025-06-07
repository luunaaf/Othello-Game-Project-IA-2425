import tensorflow as tf
from mcts import Node, tree_policy, best_child, backup, preprocess
import numpy as np
import random
import tensorflow as tf
from mcts import uct_search
from othello_game import OthelloGame

game = OthelloGame()
model_random= tf.keras.models.load_model("othello_training_model_random_100.h5")
model_NN= tf.keras.models.load_model("othello_training_model_100.h5")

def uct_search_model_vs_model(initialState, initial_player, budget,cp):
        root = Node(state = initialState, player=initial_player)
        for _ in range(budget):
            node = tree_policy(root, cp)
            if node is None:
             break  
            reward = default_policy(node.state, node.player)
            backup(node, reward)
        best_child_node = best_child(root,cp) 
        return best_child_node.action if best_child_node else None
        

def default_policy(state, player):
    if (player == 1):
         tensor = preprocess(state, player)
         predictions = model_NN.predict(tensor, verbose=0)
         value = predictions[0][0]
         return value
    else:
        current_state = state
        current_player = 2
        while not game.is_terminal(current_state):
            actions = game.get_legal_moves(current_state, current_player)
            if not actions:
                break
            action = random.choice(actions)
            current_state = game.next_state(current_state, action, current_player)
            current_player = 3 - current_player
        return game.get_result(current_state, 2)
            
def print_board(state):
    symbols = {0: '0', 1: '1', 2: '2'}  
    for row in state:
        print(' '.join(symbols[cell] for cell in row))
    print()

def generate_data(games, budget=100, cp=1.4):
    wins_random=0
    wins_100=0
    draws = 0
    X = []
    y = []
    for game_num in range(games):
        print(f"\nGenerando partida {game_num + 1}/{games}")
        state = game.get_initial_state()
        history = []
        player = 1
        turn_count = 0

        while not game.is_terminal(state):
            legal_moves = game.get_legal_moves(state, player)
            print(f" Turno {turn_count}: Jugador {player}, {len(legal_moves)} movimientos legales")
            print_board(state) 
            if not legal_moves:
                print("Sin movimientos: se pasa turno")
                player = 3 - player
                continue

            move = uct_search_model_vs_model(state, player, budget, cp)
            if move is None or move not in legal_moves:
                print("Movimiento no válido, se pasa turno")
                player = 3 - player
                continue

            print(f"Movimiento elegido: {move}")
            history.append((state.copy(), player))
            state = game.next_state(state, move, player)
            player = 3 - player
            turn_count += 1

        p1_count = np.sum(state == 1)
        p2_count = np.sum(state == 2)
        winner = 1 if p1_count > p2_count else 2 if p2_count > p1_count else 0
        if p1_count > p2_count:
            wins_100 += 1
        elif p2_count > p1_count:
            wins_random += 1
        else:
            draws += 1
        print(f"Partida terminada. Resultado: Blancas {p1_count}, Azules {p2_count} | Ganador: {winner if winner else 'Empate'}")
        print_board(state)  # 
        for s, p in history:
            label = 1 if winner == p else -1 if winner != 0 else 0
            input_tensor = (s == p).astype(int) - (s == (3 - p)).astype(int)
            X.append(input_tensor)
            y.append(label)
    print(f"Resultados finales: Modelo random: {wins_random}, Modelo 100: {wins_100}, Empates: {draws}")

if __name__ == "__main__":
    generate_data(1)
