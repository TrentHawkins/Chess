"""Implements pawn promotion and en passant.

En passant captures are indicated by specifying:
-   the capturing pawn's file of departure,
-   the "×", and
-   the destination square (not the square of the captured pawn)

NOTE: En Passant is a capturing move, and so long we provide a trailing ghost target, no need for special implementation.
Notation is precisely the same too.

Pawn promotion
    When a pawn promotes, the piece promoted to is indicated at the end of the move notation,
    for example: e8Q (promoting to queen). In standard FIDE notation, no punctuation is used;
    in Portable Game Notation (PGN) and many publications, pawn promotion is indicated by the equals sign (e8=Q).

NOTE: Promotions can be either moves or captures so, either we inherit from both `Move` and `Capture` or,
we modify the representations of the two latter to accomodate for promotions.

"""

from dataclasses import dataclass
from typing import Type

from ..move import Capture, Move
from ..pieces.pawn import Officer, Pawn


@dataclass(repr=False)
class Promotion(Capture, Move):
    """A promotion move, that required the extra info of which piece to replace the pawn with.

    Attributes:
        Piece: The type of piece the pawn is promoted to.
    """

    Piece: Type

    def __repr__(self):
        """Each move of a piece is indicated by the piece's uppercase letter, plus the coordinate of the destination square.

        Pawn promotion
            When a pawn promotes, the piece promoted to is indicated at the end of the move notation,
            for example: e8Q (promoting to queen). In standard FIDE notation, no punctuation is used;
            in Portable Game Notation (PGN) and many publications, pawn promotion is indicated by the equals sign (e8=Q).

        HACK: A mock new piece is createdto get its representation
        """
        return Move.__repr__(self) + "=" + self.Piece._repr

    def is_legal(self):
        """Check if move is legal based on piece and square context."""
        return (Move.is_legal(self) or Capture.is_legal(self)) and type(self.piece) is Pawn and self.Piece in Officer.__args__
