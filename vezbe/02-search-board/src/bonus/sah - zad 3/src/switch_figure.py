# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:54:49 2016

@author: Mijura
"""
from abc import *

class Switch(object):
    
    """
    Command pattern 
    
    Klasa Switch sadrzi recnik svih figura i na osnovu prosledjenog stringa iz game.py
    poziva metodu get_legal_position() za odgovarajucu figuru

    """

    def __init__(self,board,position):
        self.figures ={
                "1":Pawn(board,'white',position),
                "2":Rook(board,'white',position),
                "a":Pawn(board,'black',position),
                "3":Knight(board,'white',position),
                "4":Bishop(board,'white',position),
                "5":Queen(board,'white',position),
                "6":King(board,'white',position),
                "b":Rook(board,'black',position),
                "c":Knight(board,'black',position),
                "d":Bishop(board,'black',position),
                "e":Queen(board,'black',position),
                "f":King(board,'black',position)
                
                
        }
    
    def get_positions(self, figure):
        if(figure in self.figures):
            return self.figures[figure].get_legal_positions()
        
class Figure(object):
    """Apstraktna klasa koja opisuje figuru
    atributi: 1) board - trenutno stanje na tabli
              2) color - boja figure
              3) position - pozicija figure
              4) enemies - protivnicke figure
              5) friends - prijateljske figure"""
    
    @abstractmethod
    def __init__(self,board, color, position=None):
        self.board = board
        self.color = color
        self.position = position
        if(color=='white'):
            self.enemies=['a','b','c','d','e','f']
            self.friends=['1','2','3','4','5','6']
        else:
            self.friends=['a','b','c','d','e','f']
            self.enemies=['1','2','3','4','5','6']
        
            
    @abstractmethod
    def get_legal_positions(self):
        """
        Apstraktna metoda koja treba da vrati moguce (legalne) sledece pozicije na osnovu trenutne pozicije.
        :return: list
        """
        pass
        
    
    
class Pawn(Figure):
    """Klasa koja predstavlja pesaka (nasledjuje figuru),
    redefinise metodu get_legal_positions() za odredjivanje mogucih sledecih polja na tabli"""
    
    def __init__(self,board, color, position):
        super(self.__class__, self).__init__(board, color, position)
        
    
    def get_legal_positions(self):
        # d_rows (delta rows), d_cols (delta columns)
        # moguci smerovi kretanja pesaka(na koso jedno polje ako jede figuru,
        # jedno polje napred, i dva polja napred ukoliko se nalazi na pocetnoj poziciji)
                
        #ovo su pozicije za crnog pesaka, za belog pesaka potrebno je d_rows i d_cols
        #pomnoziti sa -1 jer se on krece u suprotnom smeru
        
        d_rows = [1,  1, 1, 2]
        d_cols = [1, -1, 0, 0]

        row, col = self.position  # trenutno pozicija
        
        new_positions = []
        for d_row, d_col in zip(d_rows, d_cols):  # za sve moguce smerove
        
            if(self.color=='white'):# ako je beli pesak mnozimo d_row,d_col sa -1
                d_row =-1*d_row
                d_col =-1*d_col
                
            new_row = row + d_row  # nova pozicija po redu
            new_col = col + d_col  # nova pozicija po koloni
            
            # ako nova pozicija nije van table 
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                
                id_new_figure = self.board.data[new_row][new_col]
            
                if(self.color=='black'):
                    #ako hoce da jede protivnicku figuru
                    if(d_row==1 and d_col==1 or d_row==1 and d_col== -1):
                        #ako je protivnicka figura i ako nije kralj
                        if( id_new_figure in self.enemies and id_new_figure!='6'):
                            new_positions.append((new_row, new_col))            
                    
                    #kretanje dva polja unapred
                    elif(d_row==2 and d_col==0):
                         #ako se nalazi na startnoj poziciji 
                        #i ako slobodna pozicija dva mesta unapred
                        #i ako jedno mesto ispred se ne nalazi figura 
                        if(row==1 and id_new_figure=='.' 
                            and self.board.data[row+1][col] =='.'):
                                new_positions.append((new_row, new_col))
                                
                    elif(d_row==1 and d_col==0):
                        #ako je polje slobodno
                        if(id_new_figure=='.'):
                            new_positions.append((new_row, new_col))
                
                else:#ako je beli pesak 
                    #ako hoce da jede protivnicku figuru
                    if(d_row==-1 and d_col==-1 or d_row==-1 and d_col== 1):
                        #ako je protivnicka figura i ako nije kralj
                        if( id_new_figure in self.enemies and id_new_figure!='f'):
                                new_positions.append((new_row, new_col))            
                    
                    #kretanje dva polja unapred
                    elif(d_row==-2 and d_col==0):
                        #ako se nalazi na startnoj poziciji 
                        #i ako slobodna pozicija dva mesta unapred
                        #i ako jedno mesto ispred se ne nalazi figura 
                        if(row==6 and id_new_figure=='.' 
                            and self.board.data[row-1][col] =='.'):
                                new_positions.append((new_row, new_col))
                                
                    #kretanje jedno mesto unapred
                    elif(d_row==-1 and d_col==0):
                        #ako je polje slobodno
                        if(id_new_figure=='.'):
                            new_positions.append((new_row, new_col))
        return new_positions

class Knight(Figure):
    """Klasa koja predstavlja skakaca (nasledjuje figuru),
    redefinise metodu get_legal_positions() za odredjivanje mogucih sledecih polja na tabli"""
    
    
    def __init__(self,board, color, position):
        super(self.__class__, self).__init__(board, color, position)
        
    
    def get_legal_positions(self):
        # d_rows (delta rows), d_cols (delta columns)
        # moguce sledece pozicije za skakaca( to su sve moguce kombinacije na "Г")
        d_rows = [2,  2, 1,  1, -2, -2, -1, -1]
        d_cols = [1, -1, 2, -2, -1,  1,  2, -2]

        row, col = self.position  # trenutno pozicija
        
        new_positions = []
        for d_row, d_col in zip(d_rows, d_cols):  # za sve moguce skokove
            
            new_row = row + d_row  # nova pozicija po redu
            new_col = col + d_col  # nova pozicija po koloni
            
            # ako nova pozicija nije van table 
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                
                id_new_figure = self.board.data[new_row][new_col]
                
                #ukoliko se na novom polju ne nalazi prijateljska figura i
                #ako se ne nalazi kralj
                if(id_new_figure not in self.friends
                    and id_new_figure!='6' and id_new_figure!='f'):
                        new_positions.append((new_row, new_col))
        
        return new_positions
                        
class Rook(Figure):
    """Klasa koja predstavlja topa (nasledjuje figuru),
    redefinise metodu get_legal_positions() za odredjivanje mogucih sledecih polja na tabli"""
    
    
    def __init__(self,board, color, position):
        super(self.__class__, self).__init__(board, color, position)
        
    
        
    def get_legal_positions(self):

        row, col = self.position  # trenutno pozicija
        
        new_positions = []
            
        #odredjivanje koliko polja sme da ide napred
        for i in range(1,8):
            if(row+i< 8):
                if(self.board.data[row+i][col] in self.friends):
                    break;
                if(self.board.data[row+i][col]!='6' and self.board.data[row+i][col]!='f'):
                    new_positions.append((row+i, col))
            
        #odredjivanje koliko polja sme da ide nazad
        for i in range(1,8):
            if(row-i>= 0):
                if(self.board.data[row-i][col] in self.friends):
                    break;
                if(self.board.data[row-i][col]!='6' and self.board.data[row-i][col]!='f'):
                    new_positions.append((row-i, col))
            
        #odredjivanje koliko polja sme da ide desno
        for i in range(1,8):
            if(col+i< 8): 
                if(self.board.data[row][col+i] in self.friends):
                    break;
                if(self.board.data[row][col+i]!='6' and self.board.data[row][col+i]!='f'):
                    new_positions.append((row, col+i))    
        
        #odredjivanje koliko polja sme da ide levo
        for i in range(1,8):
            if(col-i>=0): 
                if(self.board.data[row][col-i] in self.friends):
                    break;
                if(self.board.data[row][col-i]!='6' and self.board.data[row][col-i]!='f'):
                    new_positions.append((row, col-i))

        return new_positions

class Bishop(Figure):
    """Klasa koja predstavlja lovca (nasledjuje figuru),
    redefinise metodu get_legal_positions() za odredjivanje mogucih sledecih polja na tabli"""
    
    
    def __init__(self,board, color, position):
        super(self.__class__, self).__init__(board, color, position)
        
    
    def get_legal_positions(self):
        row, col = self.position  # trenutno pozicija
        
        new_positions = []
        
        #odredjivanje dozvoljenih polja gore desno
        for i in range(1,8):
            if(row+i< 8 and col+i<8):
                if(self.board.data[row+i][col+i] in self.friends):
                    break;
                if(self.board.data[row+i][col+i]!='6' and self.board.data[row+i][col+i]!='f'):
                    new_positions.append((row+i, col+i))
            
        #odredjivanje dozvoljenih polja dole levo
        for i in range(1,8):
            if(row-i>= 0 and col-i>=0):
                if(self.board.data[row-i][col-i] in self.friends):
                    break;
                if(self.board.data[row-i][col-i]!='6' and self.board.data[row-i][col-i]!='f'):
                    new_positions.append((row-i, col-i))
            
        #odredjivanje dozvoljenih polja dole desno
        for i in range(1,8):
            if(row-i>=0 and col+i< 8): 
                if(self.board.data[row-i][col+i] in self.friends):
                    break;
                if(self.board.data[row-i][col+i]!='6' and self.board.data[row-i][col+i]!='f'):
                    new_positions.append((row-i, col+i))    
        
        #odredjivanje dozvoljenih polja gore levo
        for i in range(1,8):
            if(row+i<8 and col-i>=0): #ako nije preslo okvir table
                #ako na putu ima prijateljsku figuru ne moze vise da ide na koso
                if(self.board.data[row+i][col-i] in self.friends):
                    break;
                #ako nije kralj na novoj poziciji pozicija je validna
                if(self.board.data[row+i][col-i]!='6' and self.board.data[row+i][col-i]!='f'):
                    new_positions.append((row+i, col-i))

        return new_positions
        

class Queen(Figure):
    """Klasa koja predstavlja kraljicu (nasledjuje figuru),
    redefinise metodu get_legal_positions() za odredjivanje mogucih sledecih polja na tabli"""
    
    
    def __init__(self,board, color, position):
        super(self.__class__, self).__init__(board, color, position)
        
    
    def get_legal_positions(self):
        """posto se kraljica ponasa kao lovac i kao top 
           (tj. njeni dozvoljeni potezi predstavljaju uniju poteza lovca i topa)
           instanciracemo lovca i topa i napraviti uniju njihovih dozvoljenih poteza
        """
        b = Bishop(self.board,self.color,self.position)
        r = Rook(self.board,self.color,self.position)
        
        new_positions = b.get_legal_positions()
        for x in r.get_legal_positions():
            new_positions.append(x)
            
        return new_positions
        
class King(Figure):
    """Klasa koja predstavlja skakaca (nasledjuje figuru),
    redefinise metodu get_legal_positions() za odredjivanje mogucih sledecih polja na tabli"""
    
    
    def __init__(self,board, color, position):
        super(self.__class__, self).__init__(board, color, position)
        
    
    def get_legal_positions(self):
        d_rows = [1, 1,  1, 0,  0, -1, -1, -1]
        d_cols = [1, 0, -1, 1, -1, -1,  0, -1]

        row, col = self.position  # trenutno pozicija
        
        new_positions = []
        for d_row, d_col in zip(d_rows, d_cols):  # za sve moguce smerove
        
            new_row = row + d_row  # nova pozicija po redu
            new_col = col + d_col  # nova pozicija po koloni
            
            # ako nova pozicija nije van table 
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                
                id_new_figure = self.board.data[new_row][new_col]
                # ako je protivnicka figura i ako nije kralj ili ako je slobodno polje
                if( id_new_figure in self.enemies and id_new_figure!='f' 
                    or id_new_figure=="."):
                        new_positions.append((new_row, new_col))
        
        return new_positions
            