"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces pawns are special:
    Pawn: Moves one step forward, unless first move, where it may move two squares forward.
        Captures diagonally. Can en-pasant. Can be promoted to a higher value piece at the end of a player's board. Worth 1.
"""

from dataclasses import dataclass
from typing import ClassVar, Type

from ..piece import Orientation, Piece
from ..square import Square, Vector
from .meleed import King, Knight
from .ranged import Bishop, Queen, Rook


@dataclass(init=False, repr=False, eq=False)
class Pawn(Piece):
    """A Pawn.

    Moves forward a square, unless its first move where it can move two and unless blocked by any piece.
    It captured forward-diagonally. I can capture en-passant:
        If an enemy pawn passes yours trying to escape capture, well... it cannot, not for this round.

    Upon reaching the end of the board, it is promoted to an officer:
        - Rook
        - Bishop
        - Knight
        - Queen

    Pawn steps:
        black:
            ↓ one step
            ↓ + ↓ two step
            ↓ + ← = ↙ capture west
            ↓ + → = ↘ capture east
        white:
            ↑ one step
            ↑ + ↑ two step
            ↑ + ← = ↖ capture west
            ↑ + → = ↗ capture east
    """

#   Pawn value:
    value: ClassVar[int] = 1

#   Pawn moves:
    step: ClassVar[Vector] = Vector(+1, 0)  # One step.
    captures: ClassVar[set[Vector]] = {
        Vector(+1, -1),  # Capturing to the west.
        Vector(+1, +1),  # Capturing to the east.
    }

#   Eligible ranks for promotion:
    promotions: ClassVar[Type] = {
        Bishop,
        Knight,
        Rook,
        Queen,
    }

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": f"\033[37;1m♟\033[0m",
            "black": f"\033[30;1m♟\033[0m",
        }[self.orientation.name]

    @property
    def squares(self) -> set[Square]:
        f"""{super().squares.__doc__}"""
        squares = super().squares

        if self.square is not None:  # If pawn is on a board,
            for step in self.captures:  # For all target squares (diagonally with respect to pawn),
                square = self.square + step * self.orientation  # Get target,

                if self.capturable(square):  # If said target is inside board limits,
                    squares.add(square)  # Add said target to pawn.

            square = self.square + self.step * self.orientation  # Get forward square,

            if self.deployable(square):  # If said square is inside board limits,
                squares.add(square)  # Add said square to possible moves,

                if not self.has_moved:  # If the pawn is in its starting position,
                    square += self.step * self.orientation  # Get next forward square,

                    if self.deployable(square):  # If said square is inside board limits,
                        squares.add(square)  # Add the next forward square to possible moves too.

        return squares

    def promote(self, Piece: Type):
        """Promote pawn to piece.

        Args:
            piece: The type of piece to promote pawn to.
        """
        if Piece in self.promotions:
            self.__class__ = Piece  # Promote pawn without changing any of its other attributes.


@dataclass(init=False, repr=False)
class Castle:
    """ A pair of king and rook for facilitating castling.

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

    Castles belong to player and are a piece wrapper for such special moves.
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
        """Distinctify by length of castling."""
        return hash((self.king.orientation, self.connection))

    def deployable(self) -> bool:
        """Check if castling with the two pieces is still possible.

        Returns:
            Whether castling with the two pieces is still possible.
        """
        return not (self.king.has_moved or self.rook.has_moved or self.rook.square is None) \
            and self.king.deployable(self.flying) \
            and self.king.deployable(self.target) \
            and self.rook.deployable(self.flying)  # If rook can reach the last square, it can reach them all in-between.
