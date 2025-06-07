import numpy as np
import math
import random
from othello_game import OthelloGame
import tensorflow as tf

"""" El algoritmo MCTS viene definido por los pasos selección, expansión, simulación y backtracking"""
model = tf.keras.models.load_model("othello_training_model_100.h5")
game = OthelloGame()

class Node:
    def __init__ (self, state, player, parent=None):
        self.parent = parent
        self.children = []
        self.untried_actions = game.get_legal_moves(state, player)
        self.wins = 0
        self.visits = 0
        self.state = state
        self.player = player
        self.q_value = 0.0
        self.action = None
    
    def is_not_fully_expanded(self):
        return len(self.children) != len(game.get_legal_moves(self.state, self.player))
    
    
def uct_search(initialState, initial_player, budget,cp):
        root = Node(state = initialState, player=initial_player)
        for _ in range(budget):
            node = tree_policy(root, cp)
            if node is None:
             break  
            reward = default_policy(node.state, node.player)
            backup(node, reward)
        best_child_node = best_child(root,cp) 
        return best_child_node.action if best_child_node else None

def preprocess(state, player):
    return ((state == player).astype(int) - (state == (3 - player)).astype(int)).reshape(1, 8, 8, 1)

def default_policy(state, player):
    tensor = preprocess(state, player)
    predictions = model.predict(tensor, verbose=0)
    value = predictions[0][0]
    return value

def tree_policy(node, cp):
    while node is not None and not game.is_terminal(node.state):
         if(node.is_not_fully_expanded()):
              return expand(node)
         else:  
              node=best_child(node,cp)
    return node

def expand(node):
    a = node.untried_actions.pop()
    n_state = game.next_state(node.state, a, node.player)
    child = Node(state = n_state, parent=node, player=3 - node.player)
    child.action = a
    node.children.append(child)
    return child

def best_child(node, c): #c = parametro de exploracion
    # Si no hay hijos, no se puede elegir uno
    if not node.children:
        return None 
    
    best_children = []
    best_reward = -math.inf
    
    for child in node.children:
        if child.visits == 0 :
             uct_value = math.inf
        else:
            exploitation = child.q_value / child.visits
            exploration = c * math.sqrt((2*math.log(node.visits))/(child.visits))
            uct_value = exploitation + exploration

        if (uct_value > best_reward ):
             best_children = [child]
             best_reward = uct_value
        elif(uct_value == best_reward ):
            best_children.append(child)
           
    return random.choice(best_children)

def backup(node, reward):
    while node is not None:
        node.visits += 1
        node.q_value += reward
        reward = -reward
        node = node.parent







