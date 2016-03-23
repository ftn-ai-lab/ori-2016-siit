"""
    @author:    SW 15/2013   Dragutin Marjanovic
    @email:     dmarjanovic94@gmail.com
"""

from __future__ import print_function

from abc import *
from state import State
import sys

MAX_FLOAT = sys.float_info.max
MIN_FLOAT = -MAX_FLOAT


class AdversarialSearch(object):
    """
    Apstraktna klasa za suparnicku/protivnicku pretragu.
    """

    def __init__(self, board, max_depth):
        """
        :param board: tabla koja predstavlja pocetno stanje.
        :param max_depth: maksimalna dubina pretrage (koliko poteza unapred).
        :return:
        """
        self.initial_state = State(board, parent=None)
        self.max_depth = max_depth

    @abstractmethod
    def perform_adversarial_search(self):
        """
        Apstraktna metoda koja vrsi pretragu i vraca sledece stanje.
        """
        pass


class Minimax(AdversarialSearch):
    def minimax(self, state, depth):
        if depth == self.max_depth:
            return state.calculate_value()
            
        max_player = depth % 2 == 0
        min_player = not max_player
       
        next_states = state.generate_next_states(max_player)
        best_value = MAX_FLOAT if min_player else MIN_FLOAT
        next_state_best = None
         
        for next_state in next_states:
            next_state_value = self.minimax(next_state, depth + 1)
           
            if max_player and next_state_value > best_value:
                best_value = next_state_value
                next_state_best = next_state
               
            if min_player and next_state_value < best_value:
                best_value = next_state_value
                next_state_best = next_state
       
        if depth == 0:
            return next_state_best
           
        return best_value
            
        
    def perform_adversarial_search(self):
        # TODO 1: Implementiran minimax algoritam
        return self.minimax(self.initial_state, 0)


class AlphaBeta(AdversarialSearch):
    def alphabeta(self, state, depth, alpha, beta):
        if depth == self.max_depth:
            return state.calculate_value()
         
        max_player = depth % 2 == 0
        min_player = not max_player
       
        next_states = state.generate_next_states(max_player)
        best_value = MAX_FLOAT if min_player else MIN_FLOAT
        next_state_best = None
         
        for next_state in next_states:
            next_state_value = self.alphabeta(next_state, depth + 1, alpha, beta)
           
            if max_player and next_state_value > best_value:
                best_value = next_state_value
                next_state_best = next_state
                alpha = max(alpha, next_state_value)
               
            if min_player and next_state_value < best_value:
                best_value = next_state_value
                next_state_best = next_state
                beta = min(beta, next_state_value)
               
            if beta <= alpha:
                break
       
        if depth == 0:
            return next_state_best
           
        return best_value
        

    def perform_adversarial_search(self):
        # TODO 4: Implementiran alpha-beta algoritam
        return self.alphabeta(self.initial_state, 0, MIN_FLOAT, MAX_FLOAT)
