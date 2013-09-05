import unittest
import pieces
import board


class TestFactory(unittest.TestCase):

    def setUp(self):
        self.factory = pieces.PieceFactory()
        self.king = self.factory.newPiece('king', 1)[0]
        self.queen = self.factory.newPiece('queen', 1)[0]
        self.bishop = self.factory.newPiece('bishop', 1)[0]
        self.knight = self.factory.newPiece('knight', 1)[0]
        self.rook = self.factory.newPiece('rook', 1)[0]
        self.board = board.Board(8, 8)
        self.board1 = board.Board(6, 9)

    def test_name(self):
        self.assertEqual(self.king.name, 'king')
        self.assertEqual(self.queen.name, 'queen')
        self.assertEqual(self.bishop.name, 'bishop')
        self.assertEqual(self.knight.name, 'knight')
        self.assertEqual(self.rook.name, 'rook')

    def test_factory(self):
        self.assertRaises(pieces.InvalidPiece,
                          self.factory.newPiece, 'unknown', 1)

    def test_moves(self):
        king_moveset = ((-1, 0), (1, 0), (0, -1),
                        (0, 1), (-1, -1),
                        (-1, 1), (1, -1), (1, 1))
        self.assertEquals(self.king.getMoveSet(), king_moveset)
        rook_moveset = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self.assertEquals(self.rook.getMoveSet(), rook_moveset)

    def test_steps(self):
        self.assertEquals(self.king.getSteps(), 1)
        self.assertEquals(self.queen.getSteps(), 'infinite')

    def test_max_length(self):
        self.assertEquals(self.board.getMaxLength(), 8)
        self.assertEquals(self.board1.getMaxLength(), 9)

    def test_board(self):
        self.assertRaises(board.InvalidAxis, board.Board, 8, 'impossible')
        self.assertRaises(board.InvalidAxis, board.Board, 8, -1)
        self.assertEquals(self.board1.getMaxLength(), 9)
        self.board1.forbidPosition((1, 3))
        self.assertTrue(self.board1.isForbidden(((1, 3), )))
        self.assertFalse(self.board1.isForbidden(((5, 6), )))
        self.board1.unforbidPosition((1, 3))
        self.assertFalse(self.board1.isForbidden(((1, 3), )))
        self.board1.forbidPosition((1, 2))
        position_list = self.board1.getAvailablePositions(self.king)
        self.assertTrue((0, 0) in position_list)
        self.assertFalse((1, 2) in position_list)
        self.board1.forbidPosition((1, 1))
        position_list = self.board1.getAvailablePositions(self.king)
        self.assertFalse((1, 1) in position_list)

    def test_legalMoves(self):
        moves = self.board1.legalMoves(self.rook, (0, 0))
        self.assertEquals(moves, [(0, 0), (1, 0), (0, 1), (2, 0),
                                  (0, 2), (3, 0), (0, 3), (4, 0),
                                  (0, 4), (5, 0), (0, 5), (0, 6),
                                  (0, 7), (0, 8)])
        moves = self.board1.legalMoves(self.rook, (1, 1))
        self.assertEquals(moves, [(1, 1), (0, 1), (2, 1), (1, 0),
                                  (1, 2), (3, 1), (1, 3), (4, 1),
                                  (1, 4), (5, 1), (1, 5), (1, 6),
                                  (1, 7), (1, 8)])
        moves = self.board1.legalMoves(self.queen, (1, 1))
        self.assertEquals(moves, [(1, 1), (0, 1), (2, 1), (1, 0),
                                  (1, 2), (0, 0), (0, 2), (2, 0),
                                  (2, 2), (3, 1), (1, 3), (3, 3),
                                  (4, 1), (1, 4), (4, 4), (5, 1),
                                  (1, 5), (5, 5), (1, 6), (1, 7), (1, 8)])
        moves = self.board1.legalMoves(self.king, (0, 0))
        self.assertEquals(moves, [(0, 0), (1, 0), (0, 1), (1, 1)])
        moves = self.board1.legalMoves(self.king, (5, 8))
        self.assertEquals(moves, [(5, 8), (4, 8), (5, 7), (4, 7)])
        moves = self.board1.legalMoves(self.bishop, (5, 8))
        self.assertEquals(moves, [(5, 8), (4, 7), (3, 6),
                                  (2, 5), (1, 4), (0, 3)])

    def test_set_remove_PiecePosition(self):
        self.board.setPiecePosition(self.king, (0, 0))
        self.assertEquals(self.board.getPiecePosition((0, 0)).short_name,
                          self.king.short_name)
        self.assertEquals(self.board.getPosition((0, 0)), 1)
        self.assertEquals(self.board.getPosition((0, 1)), 1)
        self.assertEquals(self.board.getPosition((1, 1)), 1)
        self.assertEquals(self.board.getPosition((1, 0)), 1)
        self.assertEquals(self.board.getPosition((2, 0)), 0)
        self.board.removePiece((0, 0))
        self.assertEquals(self.board.getPiecePosition((0, 0)), None)
        self.assertEquals(self.board.getPosition((0, 0)), 0)
        self.assertEquals(self.board.getPosition((0, 1)), 0)
        self.assertEquals(self.board.getPosition((1, 1)), 0)
        self.assertEquals(self.board.getPosition((1, 0)), 0)
        # TODO write more extensive tests


if __name__ == '__main__':
    unittest.main()
