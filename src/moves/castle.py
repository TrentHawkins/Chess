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

from ..move import dataclass
from ..pieces.melee import King
from ..pieces.ranged import Rook


@dataclass(init=False, repr=False)
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
    """

    def __init__(self, king: King, rook: Rook):
        """Set up castling pair.

        Args:
            king: A reference to a king piece.
            rook: A reference to a rook piece (of same color and on the same board).
        """
        self.king: King = king  # reference to a king piece
        self.rook: Rook = rook  # reference to a rook piece (of same color)

        self.connection = self.king.square - self.rook.square  # type: ignore
        step = self.connection // len(self.connection)  # Take the unit step in the direction from king to rook.

        self.flying = self.king.square + step      # The in-passing square of the king on its way to castling.
        self.target = self.king.square + step * 2  # The destination square the king lands upon castling.

    def __repr__(self):
        """Notation for castle moves."""
        return "O-O-O" if len(self.connection) > 3 else "O-O"

    def __hash__(self):
        """Hashing for castle moves."""
        return hash((self.king.orientation, self.connection))

    def legal(self) -> bool:
        """Check if castling with the two pieces is still possible.

        Returns:
            Whether castling with the two pieces is still possible.
        """
        return not (self.king.has_moved or self.rook.has_moved or self.rook.square is None) \
            and self.king.deployable(self.flying) \
            and self.king.deployable(self.target) \
            and self.rook.deployable(self.flying)  # If rook can reach the last square, it can reach them all in-between.
