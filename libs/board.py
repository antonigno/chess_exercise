class InvalidAxis(Exception):
    pass  # TODO


class Board(object):
    '''
    Simple chess board implemented as a matrix
    '''
    def __init__(self, x_length, y_length):
        self._x_length = x_length
        self._y_length = y_length
        # has memory of the placed pieces on the board
        # key is the position coordinates (x, y), value is the placed piece
        self.placed_pieces = {}
        # a two dimensional matrix containing the freely accessible positions
        # a free position is marked with a 0, an non free position with a 1
        self.board = []
        if not isinstance(x_length, int) or not isinstance(y_length, int):
            raise InvalidAxis
        if x_length < 0 or y_length < 0:
            raise InvalidAxis
        self.initialize_board()

    def initialize_board(self):
        self.board = [[0 for y in range(0, self._y_length)]
                      for x in range(0, self._x_length)]

    def getMaxLength(self):

        # returns the max value between x and y axix
        return max(self._x_length, self._y_length)

    def getPosition(self, (x, y)):
        #returns the value stored in board
        return self.board[x][y]

    def forbidPosition(self, (x, y)):
        # if a position is forbidden it is marked with a 1
        self.board[x][y] = 1

    def unforbidPosition(self, (x, y)):
        # if a position in not forbidden it is marked with a 0
        self.board[x][y] = 0

    def isForbidden(self, position_list):
        # returns True if at least one position is marked
        # as 1 on the board, False otherwise
        for (x, y) in position_list:
            if self.board[x][y]:
                return True
        return False

    def isFree(self, position_list):
        # returns False if at least one position is marked
        # as 1 on the board, True otherwise
        for (x, y) in position_list:
            if self.board[x][y]:
                return False
        return True

    def doesItCollide(self, position_list):
        # return True if at least one position in position_list
        # is already occupied by a piece
        for position in position_list:
            if position in self.placed_pieces:
                return True
        return False

    def getAvailablePositions(self, piece):
        # returns a list of positions available for the passed piece
        position_list = []
        for row in range(self._x_length):
            for column in range(self._y_length):
                if not self.isForbidden(((row, column),)):
                    position_list.append((row, column))
        position_list = filter(lambda position: not self.doesItCollide(
                self.legalMoves(piece, position)), position_list)
        return position_list

    def legalMoves(self, piece, (from_x, from_y)):
        # returns al list of positions the passed piece
        # can move to, starting from from_x,from_y
        moves = piece.getMoveSet()
        steps = piece.getSteps()
        legal_moves = [(from_x, from_y)]
        if steps == 'infinite':
            steps = self.getMaxLength()
        for step in range(1, steps + 1):
            for x, y in moves:
                dest = from_x + step * x, from_y + step * y
                legal_moves.append(dest)
        legal_moves = filter(self.isInBoard, legal_moves)
        return legal_moves

    def isInBoard(self, (x, y)):
        # returns True if the passed position is in board boundaries,
        # False otherwise
        if 0 <= x < self._x_length and 0 <= y < self._y_length:
            return True
        else:
            return False

    def setPiecePosition(self, piece, (x, y)):
        # sets the piece in the specified position,
        # meaning adding to placed_pieces and updating the board
        self.placed_pieces[(x, y)] = piece
        self.updateBoard()

    def getPiecePosition(self, position):
        return self.placed_pieces.get(position, None)

    def getFlattenBoard(self):
        return self.board.flatten()

    def removePiece(self, (x, y)):
        # removes the piece placed in (x,y)
        self.placed_pieces.pop((x, y), None)
        self.updateBoard()

    def updateBoard(self):
        # updates self.board values according with placed pieces
        self.initialize_board()
        for (from_x, from_y), piece in self.placed_pieces.items():
            for (x, y) in self.legalMoves(piece, (from_x, from_y)):
                self.board[x][y] = 1
            self.board[from_x][from_y] = 1

    def printPlacedPieces(self):
        if self.placed_pieces:
            for (x, y), piece in self.placed_pieces.iteritems():
                print "%s: (%s, %s)" % (piece.short_name, x, y)
        else:
            print "Empty"

    def isEmpty(self):
        return len(self.placed_pieces.keys())

    def toString(self):
        output = ""
        for (x, y) in sorted(self.placed_pieces.keys()):
            output += "%s:(%s,%s) " %\
                (self.placed_pieces[(x, y)].short_name, x, y)
        return output

    def toStringSimmetrical(self):
        output = []
        x_simmetric = {}
        y_simmetric = {}
        xy_simmetric = {}
        for (x, y) in sorted(self.placed_pieces.keys()):
            x_simmetric[((self._x_length - 1 - x), y)] \
                = self.placed_pieces[(x, y)]
            y_simmetric[(x, (self._y_length - 1 - y))]\
                = self.placed_pieces[(x, y)]
            xy_simmetric[((self._x_length - 1 - x),
                          (self._y_length - 1 - y))]\
                          = self.placed_pieces[(x, y)]
        x_output = ""
        for (x, y) in sorted(x_simmetric.keys()):
            x_output += "%s:(%s,%s) " % (x_simmetric[(x, y)].short_name, x, y)
        output.append(x_output)
        y_output = ""
        for (x, y) in sorted(y_simmetric.keys()):
            y_output += "%s:(%s,%s) " % (y_simmetric[(x, y)].short_name, x, y)
        output.append(y_output)
        xy_output = ""
        for (x, y) in sorted(xy_simmetric.keys()):
            xy_output += "%s:(%s,%s) "\
                % (xy_simmetric[(x, y)].short_name, x, y)
        output.append(xy_output)
        return output
