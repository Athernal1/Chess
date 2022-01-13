def show(chessboard):
    """Shows the chessboard in the console.
    DOES NOT WORK UNTIL ALL CLASES: Pawn, Knight, Queen, King, Rook, Bishop ARE CREATED!!!
    """
    WHITE = {
        Pawn: chr(9817),
        Knight: chr(9816),
        Queen: chr(9813),
        King: chr(9812),
        Rook: chr(9814),
        Bishop: chr(9815),
    }
    BLACK = {
        Pawn: chr(9823),
        Knight: chr(9818),
        Queen: chr(9819),
        King: chr(9812),
        Rook: chr(9820),
        Bishop: chr(9821),
    }
    for y in range(7, -1, -1):
        print(y, end='\t')
        for x in range(8):
            if chessboard.board[x][y] is not None:
                if chessboard.board[x][y].color == 'white':
                    print(WHITE[type(chessboard.board[x][y])], end='\t')
            if chessboard.board[y][x] is not None:
                if chessboard.board[y][x].color == 'white':
                    print(WHITE[type(chessboard.board[y][x])], end='\t')
                else:
                    print(BLACK[type(chessboard.board[x][y])], end='\t')
                    print(BLACK[type(chessboard.board[y][x])], end='\t')
            else:
                print('\t', end='')
        print('\n')


class Chessboard:
    pass

    def __init__(self):
        self.color = "white"
        self.board = [[None] * 8 for _ in range(8)]

    def setup(self):
        self.board[1] = [Pawn("white", x, 1) for x in range(8)]
        self.board[6] = [Pawn("black", x, 6) for x in range(8)]
        for row in [0, 7]:
            if row == 0:
                color = "white"
            if row == 7:
                color = "black"
            self.board[row][0], self.board[row][7] = Rook(color, 0, row), Rook(color, 7, row)
            self.board[row][1], self.board[row][6] = Knight(color, 1, row), Knight(color, 6, row)
            self.board[row][2], self.board[row][5] = Bishop(color, 2, row), Bishop(color, 5, row)
            self.board[row][3], self.board[row][4] = Queen(color, 3, row), King(color, 4, row)

    def print_board(self):
        for row in self.board:
            print(row)

    def list_allowed_moves(self, x, y):
        figure = self.board[y][x]
        if figure and figure.color == self.color:
            return figure.list_allowed_moves(self)
        else:
            return None

    def move(self, from_x, from_y, to_x, to_y):
        figure = self.board[from_y][from_x]
        if figure and figure.color == self.color:
            if (to_x, to_y) in self.list_allowed_moves(figure.x, figure.y):
                if type(self.board[to_y][to_x]) == King:
                    if self.color == "white":
                        return "WHITE WON"
                    return "BLACK WON"
                figure.move(to_x, to_y)
                self.board[to_y][to_x], self.board[from_y][from_x] = self.board[from_y][from_x], None
                if self.color == "white":
                    self.color = "black"
                else:
                    self.color = "white"
            else:
                raise ValueError("Invalid move")
        else:
            raise ValueError("There is no figure in this place")


class Figure:

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.if_moved = False

    def move(self, x, y):
        self.x = x
        self.y = y
        self.if_moved = True

    def _is_on_board(self, x, y):
        if x < 0 or y < 0:
            return False
        if x > 7 or y > 7:
            return False
        return True

    def _ally(self, chessboard, color, x, y):
        if chessboard.board[y][x]:
            if color == chessboard.board[y][x].color:
                return True
            return False
        return None

    def _x_border(self, chessboard, moves):
        left = 0
        right = 8
        for i in range(len(moves)):
            place = chessboard.board[moves[i][1]][moves[i][0]]
            if place:
                if self._ally(chessboard, self.color, place.x, place.y):
                    if place.x > self.x:
                        right = i
                        break
                    left = i + 1
                else:
                    if place.x > self.x:
                        right = i + 1
                        break
                    left = i
        return moves[left:right]

    def _y_border(self, chessboard, moves):
        left = 0
        right = 8
        for i in range(len(moves)):
            place = chessboard.board[moves[i][1]][moves[i][0]]
            if place:
                if self._ally(chessboard, self.color, place.x, place.y):
                    if place.y > self.y:
                        right = i
                        break
                    left = i + 1
                else:
                    if place.y > self.y:
                        right = i + 1
                        break
                    left = i
        return moves[left:right]

    def _get_diagonal_moves(self, chessboard, bishop):
        return bishop.list_allowed_moves(chessboard)

    def _get_horizontal_and_vertical_moves(self, chessboard, rook):
        return rook.list_allowed_moves(chessboard)


class Pawn(Figure):

    def list_allowed_moves(self, chessboard):
        allowed_moves = []
        if self.color == "white":
            if not self.if_moved and not chessboard.board[self.y + 1][self.x]:
                allowed_moves.append((self.x, self.y + 2))
            allowed_moves.append((self.x, self.y + 1))

            elif self.color == "black":
            if not self.if_moved and not chessboard.board[self.y - 1][self.x]:
                allowed_moves.append((self.x, self.y - 2))
            allowed_moves.append((self.x, self.y - 1))

        return [move for move in allowed_moves if self._is_on_board(*move)
                and not chessboard.board[move[1]][move[0]]] + self.beat(chessboard)

    def beat(self, chessboard):
        allowed_beat = []
        if self.color == "white":
            allowed_beat.extend([(self.x + 1, self.y + 1), (self.x - 1, self.y + 1)])
        elif self.color == "black":
            allowed_beat.extend([(self.x + 1, self.y - 1), (self.x - 1, self.y - 1)])
        return [move for move in allowed_beat if self._is_on_board(*move)
                and self._ally(chessboard, self.color, *move) == False]


class Knight(Figure):

    def list_allowed_moves(self, chessboard):
        allowed_moves = []
        allowed_moves.extend([
            (self.x + 1, self.y + 2),
            (self.x + 2, self.y + 1),
            (self.x - 1, self.y + 2),
            (self.x - 2, self.y + 1),
            (self.x + 1, self.y - 2),
            (self.x + 2, self.y - 1),
            (self.x - 1, self.y - 2),
            (self.x - 2, self.y - 1)
        ])
        return [move for move in allowed_moves if self._is_on_board(*move)
                and not self._ally(chessboard, self.color, *move)]


class Rook(Figure):

    def list_allowed_moves(self, chessboard):
        horizontal = []
        up = []
        for x in range(8):
            if x != self.x:
                horizontal.append((x, self.y))

        for y in range(8):
            if y != self.y:
                up.append((self.x, y))

        return self._x_border(chessboard, horizontal) + self._y_border(chessboard, up)


class King(Figure):

    def list_allowed_moves(self, chessboard):
        allowed_moves = []
        allowed_moves.extend([
            (self.x - 1, self.y),
            (self.x - 1, self.y + 1),
            (self.x, self.y + 1),
            (self.x + 1, self.y + 1),
            (self.x + 1, self.y),
            (self.x + 1, self.y - 1),
            (self.x, self.y - 1),
            (self.x - 1, self.y - 1)
        ])
        return [move for move in allowed_moves if self._is_on_board(*move)
                and not self._ally(chessboard, self.color, *move)]


class Bishop(Figure):

    def list_allowed_moves(self, chessboard):
        left = []
        right = []
        new_y = 0
        for position in range(self.x - self.y, self.x - self.y + 8):
            if (position, new_y) != (self.x, self.y):
                left.append((position, new_y))
            new_y += 1
        left = [move for move in left if self._is_on_board(*move)]
        new_y = 0

        for position in range(self.x - (7 - self.y), self.x - (7 - self.y) + 8):
            if (position, 7 - new_y) != (self.x, self.y):
                right.append((position, 7 - new_y))
                new_y += 1
            right = [move for move in right if self._is_on_board(*move)]
            right = right[::-1]

            return self._x_border(chessboard, left) + self._y_border(chessboard, right)


class Queen(Figure):

    def list_allowed_moves(self, chessboard):
        allowed_moves = []
        allowed_moves.extend(self._get_diagonal_moves(chessboard, Bishop(self.color, self.x, self.y)))
        allowed_moves.extend(self._get_horizontal_and_vertical_moves(chessboard, Rook(self.color, self.x, self.y)))
        return allowed_moves