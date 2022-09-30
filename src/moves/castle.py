"""Implements castling.

For each game, two such pairs are created per player, a king-side and a queen-side castle.
This implementation attempts at abstracting the castling logic to its fundamental rules:
1.  The king must not have moved.
    This is cleared here with the king's `has_moved` flag.
2.  The corresponding rook to castle must not have moved.
    This is cleared here with the rook's `has_moved` flag.
3.  The king must not be in check.
    This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
4.  The squares the king skips with castling must not be threatened.
    This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
    The king's `capturable` method is not needed, as the king can never capture a piece in the process of castling.
5.  There must not be any obstructing pieces (of any color) between the king and the rook.
    This requires a context at `board` level redefintion of the `deployable` function.
"""

from dataclasses import dataclass
from re import Pattern, compile
from typing import ClassVar

from ..piece import Piece
from ..pieces.melee import King
from ..pieces.ranged import Rook
from ..square import Square


@dataclass(repr=False)
class Castle:
    """A pair of king and rook for facilitating castling.

    For each game, two such pairs are created per player, a king-side and a queen-side castle.
    This class attempts at abstracting the castling logic to its fundamental rules:
    1.  The king must not have moved.
        This is cleared here with the king's `has_moved` flag.
    2.  The corresponding rook to castle must not have moved.
        This is cleared here with the rook's `has_moved` flag.
    3.  The king must not be in check.
        This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
    4.  The squares the king skips with castling must not be threatened.
        This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
        The king's `capturable` method is not needed, as the king can never capture a piece in the process of castling.
    5.  There must not be any obstructing pieces (of any color) between the king and the rook.
        This requires a context at `board` level redefintion of the `deployable` function.

    Attributes:
        king: A reference to a king piece.
        rook: A reference to a rook piece (of same color and on the same board).
        squares: The squares the king will access in this castling.

    Castling is indicated by the special notations 0-0 (for kingside castling) and 0-0-0 (queenside castling).
    While the FIDE standard [6] is to use the digit zero (0-0 and 0-0-0), PGN uses the uppercase letter O (O-O and O-O-O).

    NOTE: This class is made to look like a `Move` class, but aside from common names it practically overrides everything,
    so inheriting from `Move` has little to no use at all. It does a type-hinting headeach but makes for readable code too.
    """

#   Ask for any ot the piece letters to appear once or nonce (for pawns).
    move_range: ClassVar[str] = "O-O|O-O-O"
    notation: ClassVar[Pattern] = compile(move_range)

    piece: King  # reference to a king piece
    other: Rook  # reference to a rook piece (of same color)

    def __post_init__(self):
        """Set up the castling relevant squares.

        Args:
            king: A reference to a king piece.
            rook: A reference to a rook piece (of same color and on the same board).
        """
        self.connection = (self.piece.square - self.other.square)  # type: ignore
        step = self.connection // len(self.connection)  # Take the unit step in the direction from king to rook.

        self.middle = self.piece.square + step  # The in-passing square of the king on its way to castling.
        self.square = self.middle + step  # The destination square the king lands upon castling.

    def __repr__(self):
        """Notation for castle moves."""
        return {
            3: "O-O",
            4: "O-O-O",
        }[self.connection]

    def __hash__(self):
        """Hashing for castle moves."""
        return hash((self.piece.orientation, self.connection))

    def is_legal(self) -> bool:
        """Check if castling with the two pieces is still possible.

        Returns:
            Whether castling with the two pieces is still possible.
        """
        return self.piece.castleable(self.square)
