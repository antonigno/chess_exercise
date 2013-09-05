chess_exercise
==============

A coding task I realized as exercise


Chess Problem
The problem is to find all unique configurations of a set of normal chess pieces
on a chess board with dimensions M×N where none of the pieces is in a position
to take any of the others. Assume the colour of the piece does not matter, and
that there are no pawns among the pieces.
Write a program which takes as input:
• The dimensions of the board: M, N.
• The number of pieces of each type (King, Queen, Bishop, Rook and Knight)
   to try and place on the board.
As output, the program should list all the unique configurations to the console for
which all of the pieces can be placed on the board without threatening each
other.

Usage:
python ./setPieces.py, specifying the board dimensions with options -x and -y, the pieces count with -K (--kings), 
-Q (--queens), -B (--bishops), -R (--rooks), -N (--knights)
if not passed, the piece count is defaulted to 0

example:

python ./setPieces.py -x 6 -y 9 -K 2 -Q 1 -B 1 -R 1 -N 1
