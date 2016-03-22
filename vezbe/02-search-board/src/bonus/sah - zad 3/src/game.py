# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:47:34 2016

@author: Mijura
"""
from board import Board
import Tkinter as tk
import os
from PIL import Image, ImageTk
from switch_figure import Switch
import tkFileDialog


def update_board(row, col, color):
    data = board.data
    text = board.text
    delete_elems(row, col)
    elem = data[row][col]
    d, i = elem, elem
    if ',' in elem:
        s = elem.split(',')
        d = s[0]
        i = s[1]

    draw_rectangle(row, col, color)
        
    if i in board_to_icons:
        
        icon = icons[board_to_icons[i]]
        draw_rectangle(row, col, color)        
        draw_icon(row, col, icon)
    
def draw_rectangle(row, col, color, width=1):
    rect = get_cell_rectangle(row, col)
    elem_id = canvas.create_rectangle(rect, width=width, fill=color, outline='gray')
    save_elem_id(elem_id, row, col)

def save_elem_id(elem_id, row, col):
    if len(grid_elem_ids[row][col]) == 0:
        grid_elem_ids[row][col] = []
    grid_elem_ids[row][col].append(elem_id)

def get_cell_rectangle(row, col):
    return col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size

def draw_icon(row, col, icon):
    rect = get_cell_rectangle(row, col)
    elem_id = canvas.create_image(rect[0]+2, rect[1]+2, image=icon, anchor=tk.NW)
    canvas.icons[elem_id] = icon
    save_elem_id(elem_id, row, col)

def delete_elems(row, col):
    if 0 <= row < rows and 0 <= col < cols:
        for elem_id in grid_elem_ids[row][col]:
            canvas.delete(elem_id)
            if elem_id in canvas.icons:
                del canvas.icons[elem_id]
        grid_elem_ids[row][col] = []
        
def delete_texts(row, col):
    if 0 <= row < rows and 0 <= col < cols:
        for elem_id in grid_text_ids[row][col]:
            canvas.delete(elem_id)
            if elem_id in canvas.icons:
                del canvas.icons[elem_id]
        grid_text_ids[row][col] = []
        board.text[row][col] = ''
        
def display_board():
    canvas.delete(tk.ALL)
    color = 'white'
    for row in range(len(board.data)):
        for col in range(len(board.data[0])):
            update_board(row, col, color)
            
            board.fill_field(row, col, color)
            if(col!=7):
                if(color=='white'):
                    color='black'
                else:
                    color='white'

def load_board(from_file=None):      # filename passed when reopening (resetting) same file
    load_board_from_file(from_file)
    display_board()
    
def load_board_from_file(filename=None):
    if filename is None:
        filename = tkFileDialog.askopenfilename(defaultextension='.brd',
                                                filetypes=(('board files', '*.brd'), ('All files', '*.*')))
    board.load_from_file(filename)
    return filename

player_on_move=False;
positions = list()
ex_position = set();
ex_id =""

def left_click(event, row=None, col=None):
        
        
    global player_on_move,positions,ex_position,ex_id
    
    if row is None and col is None:
        cx = event.x
        cy = event.y
        col = cx // cell_size  # column
        row = cy // cell_size  # row
    #board.switch_cell(row, col)
    #update_board(row, col,'white')"""
    
    
    if(player_on_move):
        
        if((row,col) in positions):
            row_,col_ = ex_position
            board.data[row_][col_]="."
            board.data[row][col]=ex_id
            display_board()
            
        player_on_move=False;
        return;        
        
    if(board.data[row][col]!='.'):
        player_on_move=True;
        s = Switch(board,(row,col))
        positions = s.get_positions(board.data[row][col])
        ex_position = (row,col)
        ex_id = board.data[row][col]
    
        
            
#  main program #
rows = 8  # broj redova table
cols = 8  # broj kolona table
cell_size = 60  # velicina celije


board = Board(rows=rows, cols=cols)

grid_elem_ids = [[[]] * cols for _ in range(rows)]
grid_text_ids = [[[]] * cols for _ in range(rows)]

# mapiranje sadrzaja table na boju celije
board_to_colors = {'.': 'white'}
# mapiranje sadrzaja table na ikonicu
board_to_icons = {'1': 'w-p.png',           #beli pesak
                  '2': 'w-r.png',           #beli top
                  '3': 'w-kn.png',          #beli skakac
                  '4': 'w-b.png',           #beli laufer
                  '5': 'w-q.png',           #bela kraljica
                  '6': 'w-ki.png',          #beli kralj
                  'a': 'b-p.png',           #crni pesak
                  'b': 'b-r.png',           #crni top
                  'c': 'b-kn.png',          #crni skakac
                  'd': 'b-b.png',           #crni laufer
                  'e': 'b-q.png',           #crna kraljica
                  'f': 'b-ki.png'}          #crni kralj
                  
root = tk.Tk()
root.title('Šah')
top = tk.Menu(root)  # win=top-level window



# define the user interaction widgets
canvas = tk.Canvas(root, width=cols * cell_size + 1, height=rows * cell_size + 1,
                   highlightthickness=0, bd=0, bg='white')

# load icons
canvas.icons = dict()
icons = dict()
for f in os.listdir('icons'):
    if(f=='Thumbs.db'):
        continue
    icon = Image.open(os.path.join('icons', f))
    icon = icon.resize((cell_size - 2, cell_size - 2), Image.ANTIALIAS)  # resize icon to fit cell
    icon = ImageTk.PhotoImage(icon)
    icons[f] = icon
    
# put everything on the screen
display_board()
canvas.bind('<Button-1>', left_click)  # bind left mouse click event to function left_click
canvas.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

# load default board
load_board('boards/board.brd')

root.mainloop()