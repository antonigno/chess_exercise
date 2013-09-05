class InvalidMovement(Exception):
    pass  # TODO


class InvalidSteps(Exception):
    pass  # TODO


class InvalidPiece(Exception):
    pass  # TODO


class PieceFactory(object):
    def newPiece(self, name, quantity):
        piece_list = []
        for i in range(quantity):
            if name in ('king', 'K'):
                piece_list.append(King())
            elif name in ('queen', 'Q'):
                piece_list.append(Queen())
            elif name in('bishop', 'B'):
                piece_list.append(Bishop())
            elif name in ('knight', 'N'):
                piece_list.append(Knight())
            elif name in ('rook', 'R'):
                piece_list.append(Rook())
            else:
                raise InvalidPiece
        return piece_list


class Piece(object):
    def __init__(self, name, movements, steps='infinite'):
        self.name = name
        self.horizontal = False
        self.vertical = False
        self.diagonal = False
        self.L = False
        for movement in movements:
            if movement == 'horizontal':
                self.horizontal = True
            elif movement == 'vertical':
                self.vertical = True
            elif movement == 'diagonal':
                self.diagonal = True
            elif movement == 'L':
                self.L = True
            else:
                raise InvalidMovement
        if steps in (1, 'infinite'):
            self.steps = steps
        else:
            raise InvalidSteps

    def getMoveSet(self):
        moves = ()
        if self.horizontal:
            moves += ((-1, 0), (1, 0))
        if self.vertical:
            moves += ((0, -1), (0, 1))
        if self.diagonal:
            moves += ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.L:
            moves += ((-2, -1), (-2, 1), (-1, -2),
                      (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        return moves

    def getSteps(self):
        return self.steps

    def __str__(self):
        return self.name


class King(Piece):
    def __init__(self):
        self.short_name = "K"
        super(King, self).__init__('king', ('horizontal',
                                            'vertical',
                                            'diagonal'), 1)


class Queen(Piece):
    def __init__(self):
        self.short_name = "Q"
        super(Queen, self).__init__('queen', ('horizontal',
                                              'vertical',
                                              'diagonal'), 'infinite')


class Bishop(Piece):
    def __init__(self):
        self.short_name = "B"
        super(Bishop, self).__init__('bishop', ('diagonal',), 'infinite')


class Knight(Piece):
    def __init__(self):
        self.short_name = "N"
        super(Knight, self).__init__('knight', ('L',), 1)


class Rook(Piece):
    def __init__(self):
        self.short_name = "R"
        super(Rook, self).__init__('rook', ('horizontal',
                                            'vertical'), 'infinite')
