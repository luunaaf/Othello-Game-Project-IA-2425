import numpy as np
import random
import tensorflow as tf
from keras.callbacks import EarlyStopping
from mcts import uct_search
from othello_game import OthelloGame


game = OthelloGame()

def print_board(state):
    symbols = {0: '0', 1: '1', 2: '2'}  
    for row in state:
        print(' '.join(symbols[cell] for cell in row))
    print()

def generate_data(games, budget=100, cp=1.4):
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

            move = uct_search(state, player, budget, cp)
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
        print(f"Partida terminada. Resultado: Blancas {p1_count}, Azules {p2_count} | Ganador: {winner if winner else 'Empate'}")
        print_board(state)  # 
        for s, p in history:
            label = 1 if winner == p else -1 if winner != 0 else 0
            input_tensor = (s == p).astype(int) - (s == (3 - p)).astype(int)
            X.append(input_tensor)
            y.append(label)

    return np.array(X), np.array(y)


early_stop = EarlyStopping(
    monitor='val_loss',    # métrica que se monitorea
    patience=5,            # cuántas épocas sin mejora esperar antes de parar
    restore_best_weights=True  # recupera los mejores pesos automáticamente
)

# diseñamos la red neuronal

def create_model(input_shape=(8, 8, 1)):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1, activation='tanh')  # salida entre -1 y 1
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss='mean_squared_error',
        metrics=['mae']
    )
    return model


if __name__ == "__main__":
    X, y = generate_data(games=40, budget=10, cp=0.4)
    X = X.reshape(-1, 8, 8, 1).astype('float32') 
    y = y.astype('float32')

    model = create_model()
    model.fit(
    X, y,
    epochs=50,
    batch_size=64,
    validation_split=0.2,
    callbacks=[early_stop] 
    )

    model.save("othello_training_model_40_cp04.h5")
