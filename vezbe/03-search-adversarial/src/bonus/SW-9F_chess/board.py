"""
    @authors:    SW F/2013   Dragutin Marjanovic
                 SW 9/2013   Bojan Blagojevic
    @emails:     dmarjanovic94@gmail.com
                 datiglavaradi@gmail.com
"""

from __future__ import print_function

from pieces import *

class Board:
    """
    Klasa koja implementira strukturu table.
    """

    def __init__(self, rows=20, cols=20):
        self.rows = rows  # broj redova
        self.cols = cols  # broj kolona
        self.elems = ['.',   # prazno polje
                      'bp',  # crni pijun
                      'br',  # crni top
                      'bn',  # crni konj
                      'bb',  # crni lovac
                      'bk',  # crni kralj
                      'bq',  # crna kraljica
                      'wp',  # beli pijun
                      'wr',  # beli top
                      'wn',  # beli konj
                      'wb',  # beli lovac
                      'wk',  # beli kralj
                      'wq']  # bela kraljica

        # atributi koji pamte da li su se topovi ili kraljevi pomjerili (rokada)
        self.wk_moved = False
        self.bk_moved = False
        self.wrl_moved = False
        self.wrr_moved = False
        self.brl_moved = False
        self.brr_moved = False
        
        #atribut koji pamti koja se figura posljednja pomjerila (en passant)
        self.last_row = -1
        self.last_col = -1
        
        self.data = [['.'] * cols for _ in range(rows)]

    def load_from_file(self, file_path):
        """
        Ucitavanje table iz fajla.
        :param file_path: putanja fajla.
        """
        board_f = open(file_path, 'r')
        row = board_f.readline().strip('\n')
        self.data = []
        while row != '':
            self.data.append(list(row.split()))
            row = board_f.readline().strip('\n')
        board_f.close()

    def save_to_file(self, file_path):
        """
        Snimanje table u fajl.
        :param file_path: putanja fajla.
        """
        if file_path:
            f = open(file_path, 'w')
            for row in range(self.rows):
                f.write(''.join(self.data[row]) + '\n')
            f.close()

    def move_piece(self, from_row, from_col, to_row, to_col):
        """
        Pomeranje figure.
        :param from_row: prethodni red figure.
        :param from_col: prethodna kolona figure.
        :param to_row: novi red figure.
        :param to_col: nova kolona figure.
        """
        if to_row < len(self.data) and to_col < len(self.data[0]):
            t = self.data[from_row][from_col]
            self.data[from_row][from_col] = '.'
            self.data[to_row][to_col] = t
            self.move_of_king_and_rook(from_row, from_col, to_row, to_col)
            self.last_row = to_row
            self.last_col = to_col
    
    def move_of_king_and_rook(self, from_row, from_col, to_row, to_col):
        """
        Provjera da li su se kraljevi ili topovi pomijerali zbog rokade
        """  
        #provjere da li su kraljevi ili topovi inicirali pomijeranje
        if(from_row == 7 and from_col == 0):
            self.wrl_moved = True
        elif(from_row == 7 and from_col == 7):
            self.wrr_moved = True
        elif(from_row == 7 and from_col == 4):
            self.wk_moved = True
        elif(from_row == 0 and from_col == 0):
            self.brl_moved = True
        elif(from_row == 0 and from_col == 7):
            self.brr_moved = True
        elif(from_row == 0 and from_col == 4):
            self.bk_moved = True
        
        #provjera da li je neko pojeo topove
        if(to_row == 7 and to_col == 0):
            self.wrl_moved = True
        elif(to_row == 7 and to_col == 7):
            self.wrr_moved = True
        elif(to_row == 0 and to_col == 0):
            self.brl_moved = True
        elif(to_row == 0 and to_col == 7):
            self.brr_moved = True
        


    def small_rocade_move(self, color):
        """
        Mala rokada podrazumijeva da pozicije mijenjaju kralj i top sa desne strane.
        """
        if(color == 'w'):
            self.data[7][5] = 'wr' 
            self.data[7][6] = 'wk' 
            self.data[7][4] = '.'
            self.data[7][7] = '.'
            self.wk_moved = True
            self.last_row = 7
            self.last_col = 6

        else:
            self.data[0][5] = 'br' 
            self.data[0][6] = 'bk' 
            self.data[0][4] = '.'
            self.data[0][7] = '.'
            self.bk_moved = True
            self.last_row = 0
            self.last_col = 6

    def big_rocade_move(self, color):
        """
        Velika rokada podrazumijeva da pozicije mijenjaju kralj i top sa lijeve strane.
        """
        if(color == 'w'):
            self.data[7][3] = 'wr' 
            self.data[7][2] = 'wk' 
            self.data[7][4] = '.'
            self.data[7][0] = '.'
            self.wk_moved = True
            self.last_row = 7
            self.last_col = 2
        else:
            self.data[0][3] = 'wr' 
            self.data[0][2] = 'wk' 
            self.data[0][4] = '.'
            self.data[0][0] = '.'
            self.bk_moved = True
            self.last_row = 0
            self.last_col = 2

    def en_passant(self, from_row, from_col, to_row, to_col):
        """
        En passant potez - potrebno je da se data figura pomjeri ukoso na novu poziciju i da pojede
        pijuna koji je u ovom slucaju ispod/iznad date figure(bijela/crna) na novoj poziciji.
        """
        t = self.data[from_row][from_col]
        self.data[from_row][from_col] = '.'
        self.data[to_row][to_col] = t        
        self.data[from_row][to_col] = '.'

    def clear(self):
        """
        Ciscenje sadrzaja cele table.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] = '.'

    def find_position(self, element):
        """
        Pronalazenje specificnog elementa unutar table.
        :param element: kod elementa.
        :returns: tuple(int, int)
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == element:
                    return row, col
        return None, None

    def determine_piece(self, row, col):
        """
        Odredjivanje koja je figura na odredjenoj poziciji na tabli.
        :param row: red.
        :param col: kolona.
        :return: objekat figure (implementacija klase Piece).
        """
        elem = self.data[row][col]
        if elem != '.':
            side = elem[0]  # da li je crni (b) ili beli (w)
            piece = elem[1]  # kod figure
            if piece == 'p':
                return Pawn(self, row, col, side)
            if piece == 'n':
                return Knight(self, row, col, side)
            if piece == 'b':
                return Bishop(self, row, col, side)
            if piece == 'r':
                return Rook(self, row, col, side)
            if piece == 'k':
                return King(self, row, col, side)
            if piece == 'q':
                return Queen(self, row, col, side)
                
    
    # Metoda koja provjerava da li je sah        
    def is_check(self, side, king_position = None):
        if king_position is None:
            king_position = self.find_position(str(side) + 'k')
            
        if side == 'w':
            op_side = 'b'
        else:
            op_side = 'w'

        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] != '.' and (not self.data[row][col].startswith(side)) and self.data[row][col] != op_side + 'k':
                    piece = self.determine_piece(row, col)
                    positions = piece.get_legal_moves()
                    
                    if king_position in positions:
                        return True
                                   
        return False