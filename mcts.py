import numpy as np
import math
import random
"""" El algoritmo MCTS viene definido por los pasos selección, expansión, simulación y backtracking"""
class Node:
    def __init__ (self, state, player, parent):
        self.parent = parent
        self.children = []
        self.untried_actions = None
        self.wins = 0
        self.visits = 0
        self.state = state
        self.player = player
        self.q_value = 0.0
    
    def is_not_fully_expanded(self, game):
        return len(self.children) != len(game.get_legal_moves(self.state, self.player))
    
    def is_terminal(self, state):
        return np.all(state != 0)

def uct_search(initialState, budget,cp, game):
        root = Node(state = initialState)
        for i in range(budget):
            node = tree_policy(root, cp, game)
            reward = default_policy(node.state)
            backup(node, reward)
        best_child_node = best_child(root,cp) 
        return best_child_node.action

def default_policy(state, game):
    current_state = state
    current_player = 1
     # TODO

def tree_policy(node, cp, game):
    while node.is_non_terminal(game):
         if(node.is_not_fully_expanded(node)):
              return expand(node)
         else:
              node=best_child(node,cp)
    return node

def expand(node, game):
    a = node.untried_actions
    next_state = game.next_state(node.state, a, node.player)
    child = Node(state = next, parent=node, player= -v.player)
    child.action = a
    # TODO
    #child.untried_actions = game.get_legal_moves(next_state, child.player)
    node.children.append(child)
    return child

def best_child(node, c): #c = parámetro de exploración
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

def backup(state, reward):
     while state is not None:
          state.visitis += 1
          state.q_value += reward
          state = state.parent
     






