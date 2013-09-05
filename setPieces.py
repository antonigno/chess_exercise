from libs.board import Board
from libs.pieces import PieceFactory
from copy import deepcopy, copy
import optparse


class BoardConfigurations( object ):

    def __init__(self, board, piece_list):
        self.output_boards = {}
        self.board = board
        self.analysed_configurations = {}
        self.skipped_analysis = 0
        self.analysed_configuration_count = 0

    def getOutputBoardList(self):
        return self.output_boards

    def printBoardConfiguration(self, config):
        '''
        prints the board on console
        '''
        for c in config.split():
            v, k = c.split(":")
            print "%s: %s" %(k, v)
#        print config.split()
        
    def setPieceList(self, piece_list, board):
        '''
        recursively parse board configurations for the piece list.
        returns a list of all unique configurations found, expressed as board objecs
        '''
    
        # the following commented code is an attempt to skip already analysed configuration
        # commented out because on big boards the overload introduced wasn't worth the time spared
        # TODO find a more convenient way to reduce elaboration time
    
        # check if this configuration has been analysed already
        #configuration_repr = board.toString()+"".join([piece.short_name for piece in piece_list])
        #if configuration_repr in self.analysed_configurations:
#       #     print "already analysed configuration "+configuration_repr
        #    self.skipped_analysis += 1
        #    return
        #else:
            #print configuration_repr
        #    self.analysed_configurations[configuration_repr] = 1
        #    print "configuration analized: %d, skipped analysis: %d" % (len(self.analysed_configurations.keys() ), self.skipped_analysis) 
        # check if piece_list is empty
        if self.analysed_configuration_count % 100000 == 0:
            print "Analysed configurations: %d, continuing..." % self.analysed_configuration_count
        self.analysed_configuration_count += 1
        if len(piece_list) == 0:
#            print "no more pieces remaining"
            return
        piece = piece_list[0]
        available_positions = board.getAvailablePositions(piece)
        #print "available position for %s:" % piece.name
        #print available_positions
        if len(available_positions) == 0:
            #print "no available position"
            # no available positions
            return
        for position in available_positions:
            #print "Placing piece %s at position (%d, %d)" %(piece.name, position[0], position[1]) 
            board.setPiecePosition(piece, position)
            # recursion
            self.setPieceList(piece_list[1:], board)
            if len(piece_list) == 1:
                # append a copy of the current board configuration to the output_boards
                #if not board.isEmpty():
                self.output_boards[board.toString()] = 1 #deepcopy(board)
            board.removePiece(position)


if __name__ == '__main__':
    parser = optparse.OptionParser("usage: %prog [options] pieces list")
    parser.add_option("-x", "-x", dest="x",
                      default=8,   type="int",
                      help="number of places on x-asis of the board")
    parser.add_option("-y", "-y", dest="y",
                      default=8,   type="int",
                      help="number of places on y-asis of the board")
    parser.add_option("-K", "--kings", dest="kings",
                      default=0,   type="int",
                      help="number of kings on the board")
    parser.add_option("-Q", "--queens", dest="queens",
                      default=0,   type="int",
                      help="number of queens on the board")
    parser.add_option("-B", "--bishop", dest="bishops",
                      default=0,   type="int",
                      help="number of bishops on the board")
    parser.add_option("-R", "--rooks", dest="rooks",
                      default=0,   type="int",
                      help="number of rooks on the board")
    parser.add_option("-N", "--knights", dest="knights",
                      default=0,   type="int",
                      help="number of knights on the board")
   
    (options, args) = parser.parse_args()
    
    kings = options.kings
    queens = options.queens
    bishops = options.bishops
    rooks = options.rooks
    knights = options.knights
    x = options.x
    y = options.y
    print "Using board %dx%d" %(x, y)
    print "Placing kings: %d, queens: %s, bishops: %d, rooks: %s, knights: %d" %(kings, queens, bishops, rooks, knights)
    factory = PieceFactory()
    piece_list = []
    if kings > 0:
        piece_list += factory.newPiece('king', kings)
    if queens > 0:
        piece_list += factory.newPiece('queen', queens)
    if bishops > 0:
        piece_list += factory.newPiece('bishop', bishops)
    if rooks > 0:
        piece_list += factory.newPiece('rook', rooks)
    if knights > 0:
        piece_list += factory.newPiece('knight', knights)

    if x <= 0:
        print "please insert an x axis > 0"
    if y <= 0:
        print "please insert an y axis > 0"
    
    board = Board(x, y)
    configurations = BoardConfigurations(board, piece_list)
    configurations.setPieceList(piece_list, board)
    output_boards = configurations.getOutputBoardList()
    if len(output_boards) == 0:
        print "No board configuration found."
    for b in output_boards:
        print "board:"
        configurations.printBoardConfiguration(b)

    
    

#     board = Board(3, 3)
#     factory = PieceFactory()
#     piece_list = factory.newPiece('king', 2) + factory.newPiece('rook',1) 
#     configurations = BoardConfigurations(board, piece_list)
#     configurations.setPieceList(piece_list, board)
#     output_boards = configurations.getOutputBoardList()
#     for b in output_boards:
#         print "board:"
#         print b
# #        print output_boards[b].toString()


#     board = Board(4, 4)
#     factory = PieceFactory()
#     piece_list = factory.newPiece('rook', 2) + factory.newPiece('knight',4) 
#     configurations = BoardConfigurations(board, piece_list)
#     configurations.setPieceList(piece_list, board)
#     output_boards = configurations.getOutputBoardList()
#     for b in output_boards:
#         print "board:"
#         print b
#         #print output_boards[b].toString()


#     board = Board(6, 9)
#     factory = PieceFactory()
#     piece_list = factory.newPiece('king', 2) + factory.newPiece('queen', 1) + factory.newPiece('bishop', 1) \
#         + factory.newPiece('rook', 1) + factory.newPiece('knight', 1) 
#     configurations = BoardConfigurations(board, piece_list)
#     configurations.setPieceList(piece_list, board)
#     output_boards = configurations.getOutputBoardList()
#     for b in output_boards:
#         print "board:"
#         #print output_boards[b].toString()
#         print b
    
#     print "Found %d unique configurations." % len(output_boards)
    


    #for output_board in output_board_list:
    #    print "---------------------"
    #    print output_board.printPlacedPieces()
    # board = Board(6, 6)
    # factory = PieceFactory()
    # piece_list = [factory.newPiece('rook'), factory.newPiece('rook'), factory.newPiece('knight'), 
    #               factory.newPiece('knight'), factory.newPiece('knight'), factory.newPiece('knight')]
    # setPieceList(piece_list, board) 
