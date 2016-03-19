from __future__ import print_function

from collections import deque
from abc import *
from state import *


class Search(object):
    """
    Apstraktna klasa za pretragu.
    """

    def __init__(self, board):
        self.board = board
        self.max_depth = 2

    def search(self, initial_state):
        """
        Implementirana pretraga.

        :param initial_state: Inicijalno stanje. Tip: implementacija apstraktne klase State.
        :return: path, processed_list, states_list
        """
        # inicijalizacija pretrage
        initial_state = initial_state(self.board)  # pocetno stanje
        states_list = deque([initial_state])  # deque - "brza" lista u Python-u
        states_set = {initial_state.unique_hash()}  # set - za brzu pretragu stanja

        processed_list = deque([])  # deque procesiranih stanja
        processed_set = set()  # set procesiranih stanja

        # pretraga
        while len(states_list) > 0:  # dok ima stanja za obradu
            curr_state = self.select_state(states_list)  # preuzmi sledece stanje za obradu
            states_set.remove(curr_state.unique_hash())  # izbaci stanja iz seta stanja

            processed_list.append(curr_state)  # ubaci stanje u listu procesiranih stanja
            processed_set.add(curr_state.unique_hash())  # ubaci stanje u set procesiranih stanja

            if curr_state.is_final_state():  # ako je krajnje stanje
                # rekonsturisi putanju
                return Search.reconstruct_path(curr_state), processed_list, states_list

            # ako nije krajnje stanje
            # izgenerisi sledeca moguca stanja
            new_states = curr_state.get_next_states()
            # iz liste sledecih mogucih stanja izbaci ona koja su vec u listi i koja su vec procesirana
            new_states = [new_state for new_state in new_states if
                          new_state.unique_hash() not in processed_set and
                          new_state.unique_hash() not in states_set]
            # dodaj sledeca moguca stanja na kraj liste stanja
            states_list.extend(new_states)
            # dodaj sledeca moguca stanja u set stanja
            states_set.update([new_state.unique_hash() for new_state in new_states])
            
            # while petlja treba da se zavrsi i ako je lista cvorova neprazna, ali su u njoj svorovi vece dubine od max_depth
            if all(s.depth>self.max_depth for s in states_list):
                break
        
        # Samo u slucaju IterativeDepthFirstSearch-a pokrecemo opet, ali samo ako je dubina manja od 128.
        if isinstance(self, IterativeDepthFirstSearch) and self.max_depth < 128:
             self.max_depth += 1
             return self.search(RobotState)        
        
        return None, processed_list, states_list

    @staticmethod
    def reconstruct_path(final_state):
        path = []
        while final_state is not None:
            path.append(final_state.position)
            final_state = final_state.parent
        return reversed(path)

    @abstractmethod
    def select_state(self, states):
        """
        Apstraktna metoda koja, na osnovu liste svih mogucih sledecih stanja,
        bira sledece stanje za obradu.
        *** STRATEGIJA PRETRAGE SE IMPLEMENTIRA OVERRIDE-ovanjem OVE METODE ***

        :param states: lista svih mogucih sledecih stanja
        :return: odabrano sledece stanje za obradu
        """
        pass


class BreadthFirstSearch(Search):
    def select_state(self, states):
        # struktura podataka je red (queue)
        # dodaj na kraj (linija 50), uzimaj sa pocetka
        return states.popleft()


class DepthFirstSearch(Search):
    def select_state(self, states):
        # TODO 1: Implementirati DFS
        return states.pop()


class IterativeDepthFirstSearch(Search):
    def select_state(self, states):
        # TODO 2: Implementirati IDFS
        while len(states) != 0:
             state = states.pop()
             if state.depth <= self.max_depth:
                 return state


class GreedySearch(Search):
    def select_state(self, states):
        # TODO 3: Implementirati GS
        # implementirati get_cost metodu u RobotState
        best = states[0]
        for state in states:
            if(best.get_cost() > state.get_cost()):
                best = state
        states.remove(best);
        return best


class AStarSearch(Search):
    def select_state(self, states):
        # TODO 4: Implementirati A*
        # implementirati get_cost i get_current_cost metode u RobotState
        best = states[0]
        for state in states:
            if(best.get_cost() + best.get_current_cost()> state.get_cost() + state.get_current_cost()):
                best = state
        states.remove(best);
        return best

