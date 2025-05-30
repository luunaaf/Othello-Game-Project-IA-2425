import numpy as np
import random
import tensorflow as tf
from othello_game import OthelloGame

game = OthelloGame()

def generate_data(games):
    X = []
    y = []

    for _ in range(games):
        state = game.get_initial_state()
        history = []
        player = 1

        while not game.is_terminal(state):
            legal_moves = game.get_legal_moves(state, player)
            if not legal_moves:
                player = 3 - player
                continue
            move = random.choice(legal_moves)
            history.append((state.copy(), player))
            state = game.next_state(state, move, player)
            player = 3 - player

        player_1_count = np.sum(state == 1)
        player_2_count = np.sum(state == 2)

        if player_1_count > player_2_count:
            winner = 1
        elif player_2_count > player_1_count:
            winner = 2
        else:
            winner = 0

        for s, p in history:
            label = 1 if winner == p else -1 if winner != 0 and winner != p else 0
            input_tensor = (s == p).astype(int) - (s == (3 - p)).astype(int)
            X.append(input_tensor)
            y.append(label)

    return np.array(X), np.array(y)

# diseñamos la red neuronal

def create_model(input_shape=(8, 8, 1)):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),  # tablero 8×8 con 1 canal (cada celda puede ser 0, 1 o 2)
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(32, activation='relu'),# capa oculta con función de activación ReLU
        tf.keras.layers.Dense(1, activation='tanh')# en capa de salida se utiliza 'tanh' para que la salida sea entre -1 y 1
    ])
    model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss= tf.keras.losses.MeanSquaredError(),
    metrics=[tf.keras.metrics.MeanAbsoluteError()]

    )

    return model

if __name__ == "__main__":
    X, y = generate_data(100)
    X = X.reshape(-1, 8, 8, 1).astype('float32') 
    y = y.astype('float32')

    model = create_model()
    model.fit(X, y, epochs=20, batch_size=64, validation_split=0.2)

    model.save("othello_training_model.h5")




