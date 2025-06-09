import tensorflow as tf
from mcts import Node, tree_policy, best_child, backup, preprocess
import numpy as np
import random
import tensorflow as tf
from mcts import uct_search
from othello_game import OthelloGame

game = OthelloGame()
model_10= tf.keras.models.load_model("othello_training_model_40_cp04.h5")
model_150= tf.keras.models.load_model("othello_training_model_40_cp14.h5")
        


            
def print_board(state):
    symbols = {0: '0', 1: '1', 2: '2'}  
    for row in state:
        print(' '.join(symbols[cell] for cell in row))
    print()

def generate_data(games, budget=100, cp=1.4):
    wins_10 = 0
    wins_150 = 0
    draws = 0

    for game_num in range(games):
        print(f"\nGenerando partida {game_num + 1}/{games}")
        state = game.get_initial_state()
        player = 1
        turn_count = 0

        if game_num % 2 == 0:
            models = {1: model_10, 2: model_150}
        else:
            models = {1: model_150, 2: model_10}

        def default_policy(state, player):
            tensor = preprocess(state, player)
            model = models[player]
            value = model.predict(tensor, verbose=0)[0][0]
            return value

        while not game.is_terminal(state):
            legal_moves = game.get_legal_moves(state, player)
            if not legal_moves:
                player = 3 - player
                continue

            move = uct_search_model_vs_model(state, player, budget, cp, default_policy)
            if move is None or move not in legal_moves:
                player = 3 - player
                continue

            state = game.next_state(state, move, player)
            player = 3 - player
            turn_count += 1

        p1_count = np.sum(state == 1)
        p2_count = np.sum(state == 2)
        winner = 1 if p1_count > p2_count else 2 if p2_count > p1_count else 0

        if winner == 1:
            if models[1] == model_10:
                wins_10 += 1
            else:
                wins_150 += 1
        elif winner == 2:
            if models[2] == model_10:
                wins_10 += 1
            else:
                wins_150 += 1
        else:
            draws += 1

    print(f"Resultados finales en {games} partidas:")
    print(f"Modelo cp 0.4 ganó: {wins_10} veces")
    print(f"Modelo cp 1.4 ganó: {wins_150} veces")
    print(f"Empates: {draws}")

def uct_search_model_vs_model(initialState, initial_player, budget, cp, default_policy):
    root = Node(state=initialState, player=initial_player)
    for _ in range(budget):
        node = tree_policy(root, cp)
        if node is None:
            break
        reward = default_policy(node.state, node.player)
        backup(node, reward)
    best_child_node = best_child(root, cp)
    return best_child_node.action if best_child_node else None

if __name__ == "__main__":
    generate_data(20,10,1.4)

