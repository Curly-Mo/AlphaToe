import sys
import operator
import copy


class Bot:
    def get_move(self, pos, tleft):
        legal_moves = pos.legal_moves()
        if not legal_moves:
            return ''
        scores = {}
        for move in legal_moves:
            scores[move] = 0
        for move in legal_moves:
            microboard, index = pos.get_microboard(move[0], move[1])
            legal_microboard = [m for m in legal_moves if m in flatten(microboard)]
            # Block opponent
            if self.is_winner(move, pos, self.oppid):
                if not any(self.is_winner(m, pos, self.oppid) for m in legal_microboard if m != move):
                    scores[move] += 3
            # Win microboard
            if self.is_winner(move, pos, self.myid):
                scores[move] += 10
            # Win Game
            if self.is_macro_winner(move, pos, self.myid):
                scores[move] += 100000000000
            # Corner
            if self.is_center(index):
                scores[move] += 0.5
            # Edge
            if self.is_edge(index):
                scores[move] -= 0.5
            # Setup potential win
            opts = list(self.row_col_diag(index, microboard))
            opts = [[pos.board[9*y+x] for x, y in opt] for opt in opts]
            for opt in opts:
                if self.myid in opt and self.oppid not in opt:
                    scores[move] += 1.1

            next_pos = copy.deepcopy(pos)
            next_pos.make_move(move[0], move[1], self.myid)
            next_legal_moves = self.next_legal(index, next_pos)
            can_block = False
            for next_move in next_legal_moves:
                # Lose next microboard
                if self.is_winner(next_move, next_pos, self.oppid):
                    scores[move] -= 10
                # Allow opp to block me
                if self.is_winner(next_move, next_pos, self.myid) and not can_block:
                    can_block = True
                    scores[move] -= 2
                # Lose Game
                if self.is_macro_winner(next_move, next_pos, self.oppid):
                    scores[move] -= 10000
                # Allow opp to block my winning move
                if self.is_macro_winner(next_move, next_pos, self.myid):
                    scores[move] -= 12

        sys.stderr.write('scores:\n')
        for score in scores.items():
            sys.stderr.write('{}\n'.format(score))
        sys.stderr.write('\n')
        best_scores = max_items(scores)

        # Find the best option when multiple good moves are equal
        if len(best_scores) > 1:
            best_scores = self.tiebreaker(best_scores, pos)
            sys.stderr.write('Tiebreaker: {}\n'.format(best_scores))

        best_move = max(best_scores.items(), key=operator.itemgetter(1))[0]
        return best_move

    def tiebreaker(self, scores, pos):
        for move in scores.keys():
            index = (move[0]/3, move[1]/3)
            macroboard = zip(*[pos.macroboard[0:3], pos.macroboard[3:6], pos.macroboard[6:9]])
            # Setup potential macro win
            opts = list(self.row_col_diag(index, macroboard))
            for opt in opts:
                if self.myid in opt and self.oppid not in opt:
                    scores[move] += 1
            # Corner
            if self.is_center(index):
                scores[move] += 0.1
            # Edge
            if self.is_edge(index):
                scores[move] -= 0.1
        return scores

    def is_winner(self, move, pos, id):
        microboard, index = pos.get_microboard(move[0], move[1])
        opts = list(self.row_col_diag(index, microboard))
        opts = [[pos.board[9*y+x] for x, y in opt] for opt in opts]
        for opt in opts:
            if all(v == id for v in opt):
                return True
        return False

    def is_macro_winner(self, move, pos, id):
        if self.is_winner(move, pos, id):
            index = (move[0]/3, move[1]/3)
            macroboard = zip(*[pos.macroboard[0:3], pos.macroboard[3:6], pos.macroboard[6:9]])
            # sys.stderr.write('MACROBOARD: {}\n'.format(macroboard))
            opts = list(self.row_col_diag(index, macroboard))
            # sys.stderr.write('{}\n'.format(opts))
            # sys.stderr.write('\n')
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

    def is_center(self, index):
        if index == (1, 1):
            return True
        return False

    def is_edge(self, index):
        if index in [(0, 1), (1, 0), (2, 1), (1, 2)]:
            return True
        return False

    def next_microboard(self, index, pos):
        microboard, _ = pos.get_microboard(index[0]*3, index[1]*3)
        return microboard

    def next_legal(self, index, pos):
        # Won board
        if pos.macroboard[3*index[1]+index[0]] > 0:
            moves = [(x, y) for x in range(9) for y in range(9)]
        # Cats game
        elif pos.is_cats_game(index[0], index[1]):
            moves = [(x, y) for x in range(9) for y in range(9)]
        else:
            microboard = self.next_microboard(index, pos)
            moves = flatten(microboard)
        legal_moves = [m for m in moves if pos.board[9*m[1] + m[0]] == 0 and pos.macroboard[3*(m[1]//3)+m[0]//3] < 1]
        return legal_moves


def flatten(l):
    return [item for sublist in l for item in sublist]


def max_items(d):
    max_val = max(d.values())
    return {k: v for k, v in d.items() if v == max_val}
