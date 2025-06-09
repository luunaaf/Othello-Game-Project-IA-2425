import tensorflow as tf
import numpy as np
import random
from othello_game import OthelloGame
from mcts import Node, tree_policy, best_child, backup, preprocess

game = OthelloGame()
model = tf.keras.models.load_model("othello_training_model_100_nn.h5")

def default_policy(state, player):
    tensor = preprocess(state, player)
    value = model.predict(tensor, verbose=0)[0][0]
    return value

def uct_search_model(state, player, budget, cp):
    root = Node(state=state, player=player)
    for _ in range(budget):
        node = tree_policy(root, cp)
        if node is None:
            break
        reward = default_policy(node.state, node.player)
        backup(node, reward)
    best_child_node = best_child(root, cp)
    return best_child_node.action if best_child_node else None

def print_board(state):
    symbols = {0: '0', 1: '1', 2: '2'}
    for row in state:
        print(' '.join(symbols[cell] for cell in row))
    print()

def generate_data(games=20, budget=100, cp=0.5):
    wins_model = 0
    wins_random = 0
    draws = 0

    for game_num in range(games):
        print(f"\n📘 Partida {game_num + 1}/{games}")
        state = game.get_initial_state()
        player = 1
        turn_count = 0

        # Alternar: el modelo juega como jugador 1 o 2
        model_player = 1 if game_num % 2 == 0 else 2
        print(f"Modelo juega como jugador {model_player}")

        while not game.is_terminal(state):
            legal_moves = game.get_legal_moves(state, player)
            print(f"Turno {turn_count}: Jugador {player}, {len(legal_moves)} movimientos")
            print_board(state)

            if not legal_moves:
                print("Sin movimientos, se pasa turno")
                player = 3 - player
                continue

            if player == model_player:
                move = uct_search_model(state, player, budget, cp)
            else:
                move = random.choice(legal_moves)

            if move is None or move not in legal_moves:
                print("Movimiento inválido, se pasa turno")
                player = 3 - player
                continue

            print(f"Movimiento elegido: {move}")
            state = game.next_state(state, move, player)
            player = 3 - player
            turn_count += 1

        p1_count = np.sum(state == 1)
        p2_count = np.sum(state == 2)
        winner = 1 if p1_count > p2_count else 2 if p2_count > p1_count else 0

        print(f"\n Final: Blancas ={p1_count}, Azules ={p2_count} → Ganador: {'Empate' if winner == 0 else winner}")
        print_board(state)

        if winner == model_player:
            wins_model += 1
        elif winner == 0:
            draws += 1
        else:
            wins_random += 1

    print(f"\n Resultados finales tras {games} partidas:")
    print(f" Modelo ganó: {wins_model}")
    print(f" Random ganó: {wins_random}")
    print(f" Empates: {draws}")

if __name__ == "__main__":
    generate_data(games=20, budget=10, cp=0.5)
