
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
        self.macroboard[3*mby+mbx] = -1
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
