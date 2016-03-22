from __future__ import print_function


class Board:
    """
    Klasa koja implementira strukturu table.
    """

    def __init__(self, rows=8, cols=8):
        self.rows = rows  # broj redova
        self.cols = cols  # broj kolona
        # ---------------
        # . = empty
        # w = wall
        # r = robot
        # g = robot's goal
        # ----------------
        self.elems = ['.',
                      'w',
                      '1',
                      '2',
                      '3',
                      '4',
                      '5',
                      '6',
                      'a',
                      'b',
                      'c',
                      'd',
                      'e',
                      'f']
        self.data = [['.'] * cols for _ in range(rows)]
        self.text = [[''] * cols for _ in range(rows)]
        self.colors = [[''] * cols for _ in range(rows)]

    def load_from_file(self, file_path):
        """
        Ucitavanje table iz fajla.
        :param file_path: putanja fajla.
        """
        board_f = open(file_path, 'r')
        row = board_f.readline().strip('\n')
        self.data = []
        while row != '':
            self.data.append(list(row))
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
    
    def fill_field(self, row, col, color):
        """
        Dodeljuje polju sa indeksom row,col prosledjenu boju
        """
        self.colors[row][col] = color;

    def switch_cell(self, row, col):
        """
        Izmena sadrzaja celije table.
        :param row: red celije.
        :param col: kolona celije.
        """
        if row < len(self.data) and col < len(self.data[0]):
            idx = self.elems.index(self.data[row][col])
            idx += 1
            idx %= len(self.elems)
            self.data[row][col] = self.elems[idx]

    def clear(self):
        """
        Ciscenje sadrzaja cele table.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] = '.'
                self.text[row][col] = ''

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


