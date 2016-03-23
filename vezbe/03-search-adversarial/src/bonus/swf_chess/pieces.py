"""
    @author:    SW 15/2013   Dragutin Marjanovic
    @email:     dmarjanovic94@gmail.com
"""

from __future__ import print_function

from abc import *


class Piece(object):
    """
    Apstraktna klasa za sahovske figure.
    """
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side

    @abstractmethod
    def get_legal_moves(self):
        """
        Apstraktna metoda koja treba da za konkretnu figuru vrati moguce sledece poteze (pozicije).
        """
        pass

    def get_value(self):
        """
        Vrednost figure modifikovana u odnosu na igraca.
        Figure crnog (MAX igrac) imaju pozivitnu vrednost, a belog (MIN igrac) negativnu.
        :return: float
        """
        return self.get_value_() if self.side == 'b' else self.get_value_() * -1.

    @abstractmethod
    def get_value_(self):
        """
        Apstraktna metoda koja treba da vrati vrednost za konkretnu figuru.
        """
        pass


class Pawn(Piece):
    """
    Pijun
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        if side == 'w':  # beli pijun
            # jedan unapred, ako je polje prazno
            if row > 0 and self.board.data[row-1][col] == '.':
                d_rows.append(-1)
                d_cols.append(0)
            # dva unapred, ako je pocetna pozicija i ako je polje prazno
            if row == self.board.rows - 2 and self.board.data[row-1][col] == '.' and self.board.data[row-2][col] == '.':
                d_rows.append(-2)
                d_cols.append(0)
            # ukoso levo, jede crnog
            if col > 0 and row > 0 and self.board.data[row-1][col-1].startswith('b'):
                d_rows.append(-1)
                d_cols.append(-1)
            # ukoso desno, jede crnog
            if col < self.board.cols - 1 and row > 0 and self.board.data[row-1][col+1].startswith('b'):
                d_rows.append(-1)
                d_cols.append(1)
        else:  # crni pijun
            # TODO 2: Implementirani moguci sljedeci potezi za crnog pijuna
            # jedan unapijred, ako je polje prazno
            if row < 7 and self.board.data[row+1][col] == '.':
                d_rows.append(1)
                d_cols.append(0)
            # dva unaprijed, ako je pocetna pozicija i ako je polje prazno
            if row == 1 and self.board.data[row+1][col] == '.' and self.board.data[row+2][col] == '.':
                d_rows.append(2)
                d_cols.append(0)
            # ukoso lijevo, jede bijelog
            if col > 0 and row < 7 and self.board.data[row+1][col-1].startswith('w'):
                d_rows.append(1)
                d_cols.append(-1)
            # ukoso desno, jede crnog
            if col < self.board.cols - 1 and row < 7 and self.board.data[row+1][col+1].startswith('w'):
                d_rows.append(1)
                d_cols.append(1)
            

        for d_row, d_col in zip(d_rows, d_cols):
                new_row = row + d_row
                new_col = col + d_col
                if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                    legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):
        return 1.  # pijun ima vrednost 1


class Knight(Piece):
    """
    Konj
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        
        d_rows = [1, 1, -1, -1, 2, 2, -2, -2]
        d_cols = [2, -2, 2, -2, 1, -1, 1, -1]
        
        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if (self.side == 'w' and 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols 
                and (self.board.data[new_row][new_col] == '.' or self.board.data[new_row][new_col].startswith('b'))):
                legal_moves.append((new_row, new_col))
            
            if (self.side == 'b' and 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols 
                and (self.board.data[new_row][new_col] == '.' or self.board.data[new_row][new_col].startswith('w'))):
                legal_moves.append((new_row, new_col))

        return legal_moves
        

    def get_value_(self):
        return 7.


class Bishop(Piece):
    """
    Lovac
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        
        # Dijagonalno desno i dole
        for i, j in zip(range(row + 1, self.board.rows), range(col + 1, self.board.cols)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
                    
        # Dijagonalno desno i gore
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, self.board.cols)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
                    
        # Dijagonalno lijevo i dole
        for i, j in zip(range(row + 1, self.board.rows), range(col - 1, -1, -1)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
                    
        # Dijagonalno lijevo i gore
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
        
        return legal_moves

    def get_value_(self):
        return 6.
        


class Rook(Piece):
    """
    Top
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        
        # Dole
        for i in xrange(row + 1, self.board.rows):
            if self.board.data[i][col] == '.':
                legal_moves.append((i, col))
                    
            if side == 'w' and self.board.data[i][col].startswith('b'):
                legal_moves.append((i, col))
                break
                    
            if side == 'b' and self.board.data[i][col].startswith('w'):
                legal_moves.append((i, col))
                break
                
            if self.board.data[i][col].startswith(side):
                break
                
        # Gore
        for i in xrange(row - 1, -1, -1):
            if self.board.data[i][col] == '.':
                legal_moves.append((i, col))
                    
            if side == 'w' and self.board.data[i][col].startswith('b'):
                legal_moves.append((i, col))
                break
                    
            if side == 'b' and self.board.data[i][col].startswith('w'):
                legal_moves.append((i, col))
                break
                
            if self.board.data[i][col].startswith(side):
                break
                
        # Desno
        for i in xrange(col + 1, self.board.cols):
            if self.board.data[row][i] == '.':
                legal_moves.append((row, i))
                    
            if side == 'w' and self.board.data[row][i].startswith('b'):
                legal_moves.append((row, i))
                break
                    
            if side == 'b' and self.board.data[row][i].startswith('w'):
                legal_moves.append((row, i))
                break
                
            if self.board.data[row][i].startswith(side):
                break
                
        # Lijevo
        for i in xrange(col - 1, -1, -1):
            if self.board.data[row][i] == '.':
                legal_moves.append((row, i))
                    
            if side == 'w' and self.board.data[row][i].startswith('b'):
                legal_moves.append((row, i))
                break
                    
            if side == 'b' and self.board.data[row][i].startswith('w'):
                legal_moves.append((row, i))
                break
                
            if self.board.data[row][i].startswith(side):
                break
        
        return legal_moves

    def get_value_(self):
        return 15.


class Queen(Piece):
    """
    Kraljica
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        
        # Dijagonalno desno i dole
        for i, j in zip(range(row + 1, self.board.rows), range(col + 1, self.board.cols)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
                    
        # Dijagonalno desno i gore
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, self.board.cols)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
                    
        # Dijagonalno lijevo i dole
        for i, j in zip(range(row + 1, self.board.rows), range(col - 1, -1, -1)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
                    
        # Dijagonalno lijevo i gore
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if self.board.data[i][j] == '.':
                legal_moves.append((i, j))
                    
            if side == 'w' and self.board.data[i][j].startswith('b'):
                legal_moves.append((i, j))
                break
                    
            if side == 'b' and self.board.data[i][j].startswith('w'):
                legal_moves.append((i, j))
                break
                
            if self.board.data[i][j].startswith(side):
                break
                
        # Dole
        for i in xrange(row + 1, self.board.rows):
            if self.board.data[i][col] == '.':
                legal_moves.append((i, col))
                    
            if side == 'w' and self.board.data[i][col].startswith('b'):
                legal_moves.append((i, col))
                break
                    
            if side == 'b' and self.board.data[i][col].startswith('w'):
                legal_moves.append((i, col))
                break
                
            if self.board.data[i][col].startswith(side):
                break
                
        # Gore
        for i in xrange(row - 1, -1, -1):
            if self.board.data[i][col] == '.':
                legal_moves.append((i, col))
                    
            if side == 'w' and self.board.data[i][col].startswith('b'):
                legal_moves.append((i, col))
                break
                    
            if side == 'b' and self.board.data[i][col].startswith('w'):
                legal_moves.append((i, col))
                break
                
            if self.board.data[i][col].startswith(side):
                break
                
        # Desno
        for i in xrange(col + 1, self.board.cols):
            if self.board.data[row][i] == '.':
                legal_moves.append((row, i))
                    
            if side == 'w' and self.board.data[row][i].startswith('b'):
                legal_moves.append((row, i))
                break
                    
            if side == 'b' and self.board.data[row][i].startswith('w'):
                legal_moves.append((row, i))
                break
                
            if self.board.data[row][i].startswith(side):
                break
                
        # Lijevo
        for i in xrange(col - 1, -1, -1):
            if self.board.data[row][i] == '.':
                legal_moves.append((row, i))
                    
            if side == 'w' and self.board.data[row][i].startswith('b'):
                legal_moves.append((row, i))
                break
                    
            if side == 'b' and self.board.data[row][i].startswith('w'):
                legal_moves.append((row, i))
                break
                
            if self.board.data[row][i].startswith(side):
                break
        
        return legal_moves

    def get_value_(self):
        return 50.


class King(Piece):
    """
    Kralj
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        
        d_rows = [-1, -1, -1, 0, 0, 1, 1, 1]
        d_cols = [-1, 0, 1, -1, 1, -1, 0, 1]
        
        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if (self.side == 'w' and 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols 
                and (self.board.data[new_row][new_col] == '.' or self.board.data[new_row][new_col].startswith('b'))):
                legal_moves.append((new_row, new_col))
            
            if (self.side == 'b' and 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols 
                and (self.board.data[new_row][new_col] == '.' or self.board.data[new_row][new_col].startswith('w'))):
                legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):
        return 300.
