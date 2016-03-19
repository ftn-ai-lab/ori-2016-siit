# autor: Aleksandar Novakovic SW 4/2013

from __future__ import print_function

import Tkinter as tk
import tkFileDialog
import tkMessageBox
import tkFont
import os
from time import sleep
import threading
from PIL import Image, ImageTk  # pip install --upgrade Pillow==3.1.1

from board import Board
from search import *
from state import *


def load_board_from_file(filename=None):
    if filename is None:
        filename = tkFileDialog.askopenfilename(defaultextension='.brd',
                                                filetypes=(('board files', '*.brd'), ('All files', '*.*')))
    board.load_from_file(filename)
    return filename


def load_board(from_file=None):      # filename passed when reopening (resetting) same file
    load_board_from_file(from_file)
    display_board()


def reload():
    global game_over
    load_board('boards/board.brd')
    game_over = False


def clear():
    board.clear()
    display_board()


def reset():
    for row in range(rows):
        for col in range(cols):
            delete_texts(row, col)
    display_board()


def key(event):
    global game_over
    k = event.keysym.lower()
    row, col, new_row, new_col = board.move_player_keyboard(k)
    if not game_over and row is not None and col is not None and new_row is not None and new_col is not None:
        update_board(row, col)
        update_board(new_row, new_col)
        if len(board.find_position('g')) == 0:
            tkMessageBox.showinfo('Result', 'You\'ve won!')
            game_over = True
            return


def switch_cell(event, row=None, col=None):
    if row is None and col is None:
        cx = event.x
        cy = event.y
        col = cx // cell_size  # column
        row = cy // cell_size  # row
    board.switch_cell(row, col)
    update_board(row, col)


def update_board(row, col):
    data = board.data
    delete_elems(row, col)
    elem = data[row][col]

    if elem in board_to_colors:
        draw_rectangle(row, col, board_to_colors[elem])
    if elem in board_to_icons:
        icon = icons[board_to_icons[elem]]
        draw_icon(row, col, icon)


def get_cell_rectangle(row, col):
    return col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size


def draw_rectangle(row, col, color, width=1):
    rect = get_cell_rectangle(row, col)
    elem_id = canvas.create_rectangle(rect, width=width, fill=color, outline='gray')
    save_elem_id(elem_id, row, col)


def draw_icon(row, col, icon):
    rect = get_cell_rectangle(row, col)
    elem_id = canvas.create_image(rect[0]+2, rect[1]+2, image=icon, anchor=tk.NW)
    canvas.icons[elem_id] = icon
    save_elem_id(elem_id, row, col)


def save_elem_id(elem_id, row, col):
    if len(grid_elem_ids[row][col]) == 0:
        grid_elem_ids[row][col] = []
    grid_elem_ids[row][col].append(elem_id)


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


def display_board():
    canvas.delete(tk.ALL)
    for row in range(len(board.data)):
        for col in range(len(board.data[0])):
            update_board(row, col)


def make_menu(win):
    top = tk.Menu(win)  # win=top-level window
    win.config(menu=top)  # set its menu option
    file_menu = tk.Menu(top)
    file_menu.add_command(label='Open...', command=load_board, underline=0)
    file_menu.add_command(label='Quit', command=sys.exit, underline=0)
    top.add_cascade(label='File', menu=file_menu, underline=0)
    edit = tk.Menu(top, tearoff=False)
    edit.add_command(label='Clear', command=clear, underline=0)
    edit.add_separator()
    top.add_cascade(label='Edit', menu=edit, underline=0)


processed = None
path = None
game_over = False


# funkcija koja se poziva na dugme SEARCH
def do_search(no):
    global processed, path
    # koju strategiju pretrage koristiti
    search = AStarSearch(board)
    # kog "agenta" koristiti
    initial_state = EnemyState

    # pokreni pretragu
    path, processed, states = search.search(initial_state, no)
    if path is None:
        return None, None
    else:
        enum_path = list(enumerate(path))
        ret_val = [None, None]
        for idx, p in enum_path:                                            # pronadji trenutnu i sledecu poziciju
            if idx == 1:                                                    # i vrati ih kao rezultat pretrage
                ret_val[1] = p
            elif idx == 0:
                ret_val[0] = p
        return ret_val


# funkija koja pokrece pretragu za svakog neprijateljskog robota pojedinacno svaki sekund
def scan():
    global game_over
    while True:
        enemies = board.find_position('e')
        num_of_enemies = len(enemies)
        from_positions = []
        to_positions = []
        for i in xrange(num_of_enemies):                                    # i je redni broj neprijatelja
            if not game_over:
                if len(board.find_position('r')) == 0:                  # ukoliko nema robota, igra je gotova
                    tkMessageBox.showinfo('Result', 'Game Over!')
                    game_over = True
                    return
                if len(board.find_position('g')) == 0:                  # ukoliko nema cilja, to znaci da je robot
                    game_over = True                                    # na toj poziciji, sto znaci da je pobedio
                    return
                result = do_search(i)                                   # nadji putanju od trenutnog neprijatelja
                from_positions.append(result[0])                        # do robota
                to_positions.append(result[1])
        move_enemies(from_positions, to_positions)                          # poremi neprijatelja na sledecu lokaciju
        if game_over:                                                       # ako je igra gotova, obavesti korisnika
            if len(board.find_position('r')) == 0:                          # i prekini
                tkMessageBox.showinfo('Result', 'Game Over!')
                game_over = True
                return
        sleep(1)                                                            # saceka jedan sekund, pa nastavi sa radom


# kada se igra pokrene, poziva se funkcija start_moving koja pravi poseban daemon thread preko kog ce se kretati
# neprijatelji
def start_moving():
    global thread, game_over
    game_over = False
    thread = threading.Timer(1, scan)
    thread.daemon = True
    thread.start()


def move_icon(from_position, to_position):                                  # pomeranje robota
    global game_over
    f = board.data[from_position[0]][from_position[1]]
    t = board.data[to_position[0]][to_position[1]]
    if f == 'e' and t == 'r':
        f = '.'
        t = 'e'
        game_over = True
    elif f == 'r' and t == 'e':
        f = '.'
        game_over = True
    else:
        f, t = t, f
    with locks[from_position[0]][from_position[1]], locks[to_position[0]][to_position[1]]:
        board.data[from_position[0]][from_position[1]] = f
        update_board(from_position[0], from_position[1])
        board.data[to_position[0]][to_position[1]] = t
        update_board(to_position[0], to_position[1])


def move_enemies(from_positions, to_positions):                             # pomeranje neprijatelja
    global game_over
    for from_position, to_position in zip(from_positions, to_positions):
        f = board.data[from_position[0]][from_position[1]]
        t = board.data[to_position[0]][to_position[1]]
        if f == 'e' and t == 'r':                                           # ako neprijatelj dodje na poziciju robota,
            f = '.'                                                         # robot nestaje
            t = 'e'
            game_over = True
        elif f == 'r' and t == 'e':
            f = '.'
            game_over = True
        else:
            f, t = t, f
        with locks[from_position[0]][from_position[1]], \
             locks[to_position[0]][to_position[1]]:                         # zakljucaj polazno i ciljno polje table
            board.data[from_position[0]][from_position[1]] = f
            update_board(from_position[0], from_position[1])
            board.data[to_position[0]][to_position[1]] = t
            update_board(to_position[0], to_position[1])

#  main program #
rows = 20  # broj redova table
cols = 20  # broj kolona table
cell_size = 40  # velicina celije

board = Board(rows=rows, cols=cols)

locks = []                                                                  # svako polje ima svoj lock objekat kako
for i in xrange(len(board.data)):                                           # bi neprijatelji mogli da rade bez
    locks.append([])                                                        # blokiranja korisnika
    for j in xrange(len(board.data[i])):
        locks[i].append(threading.RLock())

grid_elem_ids = [[[]] * cols for _ in range(rows)]
grid_text_ids = [[[]] * cols for _ in range(rows)]

# mapiranje sadrzaja table na boju celije
board_to_colors = {'.': 'white',
                   'w': 'gray',
                   'g': 'orangered',
                   'p': 'yellow'}
# mapiranje sadrzaja table na ikonicu
board_to_icons = {'r': 'robot.png',
                  'e': 'bad_robot.png'}


root = tk.Tk()
root.title('PacMan')
make_menu(root)  # make window menu
ui = tk.Frame(root, bg='white')  # main UI
ui2 = tk.Frame(root, bg='white')

# define the user interaction widgets
canvas = tk.Canvas(root, width=cols * cell_size + 1, height=rows * cell_size + 1,
                   highlightthickness=0, bd=0, bg='white')

# load icons
canvas.icons = dict()
icons = dict()
for f in os.listdir('icons'):
    icon = Image.open(os.path.join('icons', f))
    icon = icon.resize((cell_size - 2, cell_size - 2), Image.ANTIALIAS)  # resize icon to fit cell
    icon = ImageTk.PhotoImage(icon)
    icons[f] = icon

# create buttons
start_button = tk.Button(ui, text='START', width=10, command=start_moving)
reset_button = tk.Button(ui, text='RELOAD', width=10, command=reload)
stat_report = tk.Label(root, text='      ', bg='white', justify=tk.LEFT, relief=tk.GROOVE,
                       font=tkFont.Font(weight='bold'))

# add buttons to UI
start_button.grid(row=0, column=0, padx=10, pady=10)
reset_button.grid(row=2, column=0, padx=10, pady=10)

# put everything on the screen
display_board()
root.bind('<Key>', key)  # bind keyboard event to function key
ui.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
canvas.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
ui2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, anchor=tk.W)
stat_report.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.NONE)

# load default board
load_board('boards/board.brd')
root.mainloop()

