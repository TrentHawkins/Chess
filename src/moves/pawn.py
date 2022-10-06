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
"""

from dataclasses import dataclass, field
from re import Pattern, compile
from typing import ClassVar, Type

from ..move import Capture, Move
from ..piece import Piece
from ..pieces.pawn import Pawn
from ..square import Square


@dataclass(repr=False)
class Jump(Move):
    """This class actually emulates the ghost generation happening by pawn leaping at start.

    This gives credance to enpassant shall an opposing pawn is lurking near the skipped square.
    This move has a normal move representation.

    Attributes:
        piece: The pawn to make jump. It is a jump so square is known.
    """

#   Jumping is a starting pawn's property.
    piece: Pawn = field()

#   Keep track of the ghost's square.
    middle: Square = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.middle = self.square + (self.square - self.piece.square) // -2

    @classmethod
    def read(cls, notation: str, pieces: set[Piece]):
        f"""{super(Jump, cls).read.__doc__}"""
        move = super(Jump, cls).read(notation, pieces)

        if move is not None and not move.piece.has_moved:
            return move


@dataclass(repr=False)
class Promotion(Capture, Move):
    """A promotion move, that required the extra info of which piece to replace the pawn with.

    Attributes:
        piece: Override original attribute with one that is `Pawn` specifically.
        promotionPiece: The type of piece the pawn is promoted to.
    """

#   Reading of promotions:
    move_range: ClassVar[str] = f"({Move.move_range}|{Capture.move_range})=([{Pawn.piece_range}])"
    notation: ClassVar[Pattern] = compile(move_range)

    piece: Pawn = field()
    promotionPiece: Type = field()

    def __post_init__(self):
        super().__post_init__()

    def __repr__(self):
        """Each move of a piece is indicated by the piece's uppercase letter, plus the coordinate of the destination square.

        Pawn promotion
            When a pawn promotes, the piece promoted to is indicated at the end of the move notation,
            for example: e8Q (promoting to queen). In standard FIDE notation, no punctuation is used;
            in Portable Game Notation (PGN) and many publications, pawn promotion is indicated by the equals sign (e8=Q).
        """
        return super().__repr__() + ("⊜" if self.draw else "🏳" if self.resign else repr(self.promotionPiece))

    @classmethod
    def read(cls, notation: str, pieces: set[Piece]):
        f"""{super(Promotion, cls).read.__doc__}"""
        read = cls.notation.match(notation)

    #   Try to see if input matches a promotion:
        if read:
            for piece in pieces:
                promotionPiece = cls.typePiece[read.group(-1)]  # The piece type to promote to is captured last,

                offset = 3  # Regex group capturing offset due to the presence of "or" in the pattern.

                source = Square(read.group(2)) or Square(read.group(offset + 2))  # The square the piece to move is on.
                target = Square(read.group(3)) or Square(read.group(offset + 3))  # The square the piece shall move to.

            #   NOTE: OK, who would offer a draw or resign right after promoting a pawn?
            #   Only generate a move object if the right pawn is caught:
                if type(piece) is Pawn and piece.square == source:
                    move = cls(piece, target, promotionPiece, draw="=" in notation, resign="#" in notation)

                #   Only return this move if it is legal too or else we get overlaps:
                    if move:
                        return move

    def __bool__(self):
        """Check if pawn can promote either by moving or by capturing.

        Returns:
            Whether pawn can promote either by moving or by capturing.
        """
        return self.square in self.piece.squares() and self.piece.can_promote(self.square)
