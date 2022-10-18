"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces the following are units with range:
    Bishop: Moves along diagonals. Worth 3. WOrth 3+ when in pairs of two or in an open game.
    Rook: Moves along ranks and files. Worth 5.
    Queen: Moves both like a rook and bishop. Worth 9.
"""


from dataclasses import dataclass
from typing import ClassVar

from ..piece import Piece
from ..square import Square, Vector


@dataclass(init=False, repr=False, eq=False)
class Ranged(Piece):
    """A long range piece:
        - Rook
        - Bishop
        - Queen

    Testing.
    """

    def __repr__(self) -> str:
        f"""{super().__repr__.__doc__}"""
        return {
            "white": f"\033[37;1m{self.symbol}\033[0m",
            "black": f"\033[30;1m{self.symbol}\033[0m",
        }[self.orientation.name]

    def squares(self) -> set[Square]:
        f"""{super().squares.__doc__}"""
        squares = super().squares()

        if self.square is not None:  # If ranged piece is on a board,
            for step in self.steps:  # For all legal directions,
                square = self.square + step  # Get next square in direction,

                while self.deployable(square):  # If said square is unblocked,
                    if not self.king_saved(square):  # If said square leaves or puts king in danger,
                        square += step  # Advance to the next square in said direction.
                        continue  # Don't add said square, but continue looking ahead!

                    squares.add(square)  # Add said square to ranged piece.
                    square += step  # Advance to the next square in said direction.

                if self.capturable(square):  # If the square after last has a capturable piece,
                    squares.add(square)  # Do not forget to add said trailing square to targets.

        return squares


@dataclass(init=False, repr=False, eq=False)
class Rook(Ranged):
    """A rook.

    Moves anywhere along its rank xor its file, unless blocked by enemy (which captures) or same piece.

    Rook steps:
        ↑ north
        ← west
        ↓ south
        → east
    """

#   Rook value:
    value: ClassVar[int] = 5

#   Rook notation:
    letter: ClassVar[str] = "R"
    symbol: ClassVar[str] = "♜"

#   Straight lines:
    steps: ClassVar[set[Vector]] = Piece.straights
    other: Vector = Vector(0, +1)  # other castling rook unit direction

    def castleable(self, square: Square) -> bool:
        """Check if current rook is castlable.

        This method only takes care of whatever is needed by rook. Square is assumed properly invoked by `King.capturable`.
        For now, check that:
        -   The rook has not moved.
        -   The rook can move to the castling square (but only as a move, not a capture).
            This means that the only the other castling needs to be checked:
            -   In the short castling king checks both in-between squares for deployability so delagate check to king.
            -   In the other castling king checks the same squares, and there is only one square left to check for the rook.

        Args:
            square: The source square is `self.square` (not necessary).

        Returns:
            Whether piece is placeable on target square.
        """
        castle = square - self.square

    #   Mind that the rook moves the other way the king does.
        return not self.has_moved and self.square is not None \
            and self.deployable(self.square + self.other) if castle.file > 0 else True


@dataclass(init=False, repr=False, eq=False)
class Bishop(Ranged):
    """A bishop.

    Moves anywhere along a diagonal, unless blocked by enemy (which captures) or same piece.
    This means that a bishop never leaves the color of the square it is on.
    A player starts with two bishops:
        A black-square bishop.
        A white-square bishop.
    So both cover the squares of the whole board, and it is the reason the worth more when both on the board.

    Bishop steps:
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   Bishop value:
    value: ClassVar[int] = 3

#   Bishop notation:
    letter: ClassVar[str] = "B"
    symbol: ClassVar[str] = "♝"

#   Diagonal lines:
    steps: ClassVar[set[Vector]] = Piece.diagonals


@dataclass(init=False, repr=False, eq=False)
class Queen(Ranged):
    """A queen.

    Moves both like a rook and bishop, unless blocked by enemy (which captures) or same piece.
    Can access all squares.

    Inherits the steps of a King but the movement of Range.

    Queen steps:
        ↑ north
        ← west
        ↓ south
        → east
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   Queen value:
    value: ClassVar[int] = 9

#   Queen notation:
    letter: ClassVar[str] = "Q"
    symbol: ClassVar[str] = "♛"

#   Queen lines:
    steps: ClassVar[set[Vector]] = Piece.straights | Piece.diagonals
