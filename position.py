import sys


class Position:
    def __init__(self):
        self.board = []
        self.macroboard = []

    def parse_field(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        self.board = [int(f) for f in flist]

    def parse_macroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [int(f) for f in mblist]

    def is_legal(self, x, y):
        mbx, mby = x//3, y//3
        return self.macroboard[3*mby+mbx] == -1 and self.board[9*y+x] == 0

    def legal_moves(self):
        return [(x, y) for x in range(9) for y in range(9) if self.is_legal(x, y)]

    def make_move(self, x, y, pid):
        mbx, mby = x//3, y//3
        if self.is_winner(x, y, pid):
            self.macroboard[3*mby+mbx] = pid
        if self.is_cats_game(x, y, pid):
            self.macroboard[3*mby+mbx] = 3
        self.board[9*y+x] = pid

    def get_board(self):
        return ''.join(self.board, ',')

    def get_macroboard(self):
        return ''.join(self.macroboard, ',')

    def get_microboard(self, x, y):
        mini_squares = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        for mini in mini_squares:
            if x in mini:
                xs = mini
                x_index = mini.index(x)
            if y in mini:
                ys = mini
                y_index = mini.index(y)
        microboard = []
        for xx in xs:
            microboard.append([(xx, yy) for yy in ys])
        return microboard, (x_index, y_index)

    def is_cats_game(self, x, y, pid):
        if not self.is_winner(x, y, pid):
            microboard, index = self.get_microboard(x, y)
            values = [self.board[9*y+x] for x, y in flatten(microboard)]
            if all(value > 0 for value in values):
                return True
        return False

    def is_winner(self, x, y,  pid):
        microboard, index = self.get_microboard(x, y)
        opts = list(self.row_col_diag(index, microboard))
        opts = [[self.board[9*y+x] for x, y in opt] for opt in opts]
        for opt in opts:
            if all(v == id for v in opt):
                return True
        return False

    def row_col_diag(self, index, microboard):
        indices = [0, 1, 2]
        row = [(x, index[1]) for x in indices if x != index[0]]
        col = [(index[0], y) for y in indices if y != index[1]]
        diag1 = [(x, x) for x in indices]
        diag2 = [(2-x, x) for x in indices]

        opts = [row, col]
        if index in diag1:
            opts.append([i for i in diag1 if i != index])
        if index in diag2:
            opts.append([i for i in diag2 if i != index])
        for opt in opts:
            yield [microboard[x][y] for x, y in opt]


def flatten(l):
    return [item for sublist in l for item in sublist]
