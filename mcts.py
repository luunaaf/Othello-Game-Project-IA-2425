import numpy as np
import math
import random
from othello_game import get_legal_moves, next_state, is_terminal, is_non_terminal,get_result
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
    
    def is_not_fully_expanded(self):
        return len(self.children) != len(get_legal_moves(self.state, self.player))
    
    
    

def uct_search(initialState, budget,cp):
        root = Node(state = initialState)
        for _ in range(budget):
            node = tree_policy(root, cp)
            reward = default_policy(node.state)
            backup_negamax(node, reward)
        best_child_node = best_child(root,cp) 
        return best_child_node.action

def default_policy(s):
    current_state = s
    current_player = 1
    while not is_terminal(current_state):
        actions = get_legal_moves(current_state, current_player)
        if not actions:
            break
        action = random.choice(actions)
        current_state = next_state(current_state, action, current_player)
        current_player *= -1
    return get_result(current_state, 1)

def tree_policy(node, cp):
    while is_non_terminal():
         if(node.is_not_fully_expanded(node)):
              return expand(node)
         else:
              node=best_child(node,cp)
    return node

def expand(node):
    a = node.untried_actions
    next_state = next_state(node.state, a, node.player)
    child = Node(state = next, parent=node, player= -v.player)
    child.action = a
    child.untried_actions = get_legal_moves(next_state, child.player)
    node.children.append(child)
    return child

def best_child(node, c): #c = parametro de exploracion
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

def backup_negamax(state, reward):
     while state is not None:
          state.visitis += 1
          state.q_value += reward
          reward = -reward
          state = state.parent
     






