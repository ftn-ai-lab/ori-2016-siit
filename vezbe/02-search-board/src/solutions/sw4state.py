# autor: Aleksandar Novakovic SW 4/2013

from __future__ import print_function

from abc import *
import sys

class State(object):
    """
    Apstraktna klasa koja opisuje stanje pretrage.
    """

    @abstractmethod
    def __init__(self, board, parent=None, position=None, goal_position=None):
        """
        :param board: Board (tabla)
        :param parent: roditeljsko stanje
        :param position: pozicija stanja
        :param goal_position: pozicija krajnjeg stanja
        :return:
        """
        self.board = board
        self.parent = parent  # roditeljsko stanje
        if self.parent is None:  # ako nema roditeljsko stanje, onda je ovo inicijalno stanje
            agents = board.find_position(self.get_agent_code())
            if len(agents) > 0:
                self.position = agents[0]  # pronadji pocetnu poziciju
            goals = board.find_position(self.get_agent_goal_code())
            if len(goals) > 0:
                self.goal_position = goals[0]  # pronadji krajnju poziciju
        else:  # ako ima roditeljsko stanje, samo sacuvaj vrednosti parametara
            self.position = position
            self.goal_position = goal_position
        self.depth = parent.depth + 1 if parent is not None else 1  # povecaj dubinu/nivo pretrage

    def get_next_states(self):
        new_positions = self.get_legal_positions()  # dobavi moguce (legalne) sledece pozicije iz trenutne pozicije
        next_states = []
        # napravi listu mogucih sledecih stanja na osnovu mogucih sledecih pozicija
        for new_position in new_positions:
            next_state = self.__class__(self.board, self, new_position, self.goal_position)
            next_states.append(next_state)
        return next_states

    @abstractmethod
    def get_agent_code(self):
        """
        Apstraktna metoda koja treba da vrati kod agenta na tabli.
        :return: str
        """
        pass

    @abstractmethod
    def get_agent_goal_code(self):
        """
        Apstraktna metoda koja treba da vrati kod agentovog cilja na tabli.
        :return: str
        """
        pass

    @abstractmethod
    def get_legal_positions(self):
        """
        Apstraktna metoda koja treba da vrati moguce (legalne) sledece pozicije na osnovu trenutne pozicije.
        :return: list
        """
        pass

    @abstractmethod
    def is_final_state(self):
        """
        Apstraktna metoda koja treba da vrati da li je treuntno stanje zapravo zavrsno stanje.
        :return: bool
        """
        pass

    @abstractmethod
    def unique_hash(self):
        """
        Apstraktna metoda koja treba da vrati string koji je JEDINSTVEN za ovo stanje
        (u odnosu na ostala stanja).
        :return: str
        """
        pass
    
    @abstractmethod
    def get_cost(self):
        """
        Apstraktna metoda koja treba da vrati procenu cene
        (vrednost heuristicke funkcije) za ovo stanje.
        Koristi se za vodjene pretrage.
        :return: float
        """
        pass
    
    @abstractmethod
    def get_current_cost(self):
        """
        Apstraktna metoda koja treba da vrati stvarnu trenutnu cenu za ovo stanje.
        Koristi se za vodjene pretrage.
        :return: float
        """
        pass


class RobotState(State):

    def __init__(self, board, parent=None, position=None, goal_position=None):
        super(self.__class__, self).__init__(board, parent, position, goal_position)
        # posle pozivanja super konstruktora, mogu se dodavati "custom" stvari vezani za stanje
        # TODO 6: prosiriti stanje sa informacijom da li je robot pokupio kutiju
        if self.parent is not None:                                             # ako je u pitanju koren stabla,
            self.collected_boxes = set(self.parent.collected_boxes)             # kreiraj novi set pokupljenih kutija
        else:                                                                   # a inace, prepisi kopukljene kutije od
            self.collected_boxes = set()                                        # roditelja
        boxes = self.board.find_position('b')
        for box in boxes:
            if box not in self.collected_boxes and box == self.position:        # ako smo naisli na kutiju, dodajemo je
                self.collected_boxes.add(box)                                   # u set pokupljenih kutija
                break
        if len(self.collected_boxes) == len(boxes):                             # ako su sve kutije pokupljene, za cilj
            self.goal_position = self.board.find_position('g')[0]               # se postavlja krajnji cilj (goal)
        else:                                                                   # inace se trazi najbliza kutija i ona
            min_box = (sys.float_info.max, sys.float_info.max)                  # se postavlja za cilj
            for box in boxes:
                if box not in self.collected_boxes:
                    if abs(box[0] - self.position[0]) + abs(box[1] - self.position[1])\
                            < abs(min_box[0] - self.position[0]) + abs(min_box[1] - self.position[1]):
                        min_box = box
            self.goal_position = min_box


    def get_agent_code(self):
        return 'r'

    def get_agent_goal_code(self):
        return 'g'

    def get_legal_positions(self):
        # d_rows (delta rows), d_cols (delta columns)
        # moguci smerovi kretanja robota (desno, levo, dole, gore i po dijagonalama)
        d_rows = [0, 0, 1, -1, -1, -1, 1, 1]
        d_cols = [1, -1, 0, 0, -1, 1, -1, 1]

        row, col = self.position  # trenutno pozicija
        new_positions = []
        portals = self.board.find_position('p')
        if self.position in portals:                                            # ako smo na portalu, dodaj za susede i
            for portal in portals:                                              # sve ostale portale
                if portal != self.position:
                    new_positions.append(portal)
        for d_row, d_col in zip(d_rows, d_cols):  # za sve moguce smerove
            new_row = row + d_row  # nova pozicija po redu
            new_col = col + d_col  # nova pozicija po koloni
            # ako nova pozicija nije van table i ako nije zid ('w'), ubaci u listu legalnih pozicija
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols and self.board.data[new_row][new_col] != 'w':
                new_positions.append((new_row, new_col))
        return new_positions

    # stanje je finalno ako imamo sve kutije i nalazimo se na krajnjem cilju (goal)
    def is_final_state(self):
        return len(self.board.find_position('b')) == len(self.collected_boxes) and self.position == self.goal_position

    # hash vrednost definisu pokupljene kutije i pozicija
    def unique_hash(self):
        arr = str([box for box in self.collected_boxes])
        return str(self.position) + ':' + arr

    # heuristicka vrednost koja se racuna kao manhattan udaljenost plus broj preostalih kutija pomnozenih sa
    # maksimalnom mogucom manhattan razdaljinom, kako bi pozicije sa vise prikupljenih kutija imale vecu prednost
    def get_cost(self):
        return abs(self.position[0] - self.goal_position[0]) + abs(self.position[1] - self.goal_position[1])\
               + (self.board.cols + self.board.rows) * (len(self.board.find_position('b')) - len(self.collected_boxes))