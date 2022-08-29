"""Implements the chess pieces that are placed in a chessboard.

Chess has 6 types of pieces with predifined rules of movement and worth in-game:
    Pawn: Moves one step forward, unless first move, where it may move two squares forward.
        Captures diagonally. Can en-pasant. Can be promoted to a higher value piece at the end of a player's board. Worth 1.
    Bishop: Moves along diagonals. Worth 3. WOrth 3+ when in pairs of two or in an open game.
    Knights: Moves 2 squares in one directions and 1 in a vertical to that direction).
        Can jump over other pieces. Worth 3. Worth 3+ in closed games.
    Rook: Moves along ranks and files. Worth 5.
    Queen: Moves both like a rook and bishop. Worth 9.
    King: Moves one square in any direction. Worth N/A (you loose the king it's game over).
"""

from dataclasses import dataclass

from .square import Vector, Square


@dataclass
class Piece:
    """A generic chess piece."""

    color: str

    def valid_steps(self):
        """Give a list of the valid steps for the piece.

        Raises:
            NotImplementedError: Needs implementation.
        """
        raise NotImplementedError

    @property
    def is_black(self) -> bool:
        """Return whether the piece is a black piece or not.

        Returns:
            Whether the piece is a black piece or not.
        """
        return self.color == "black"


@dataclass
class Pawn(Piece):
    """A pawn."""

    value: int = 1

    def __repr__(self) -> str:
        """Represent the pawn.

        Returns:
            The representation of a pawn.
        """
        return "♟" if self.is_black else "♙"


@dataclass
class Bishop(Piece):
    """A bishop."""

    value: int = 3

    def __repr__(self) -> str:
        """Represent the bishop.

        Returns:
            The representation of a bishop.
        """
        return "♝" if self.is_black else "♗"


@dataclass
class Knight(Piece):
    """A knight."""

    value: int = 3

    def __repr__(self) -> str:
        """Represent the knight.

        Returns:
            The representation of a knight.
        """
        return "♞" if self.is_black else "♘"


@dataclass
class Rook(Piece):
    """A rook."""

    value: int = 5

    def __repr__(self) -> str:
        """Represent the rook.

        Returns:
            The representation of a rook.
        """
        return "♜" if self.is_black else "♖"


@dataclass
class Queen(Piece):
    """A queen."""

    value: int = 9

    def __repr__(self) -> str:
        """Represent the queen.

        Returns:
            The representation of a queen.
        """
        return "♛" if self.is_black else "♕"


@dataclass
class King(Piece):
    """A king."""

    def __repr__(self) -> str:
        """Represent the king.

        Returns:
            The representation of a king.
        """
        return "♚" if self.is_black else "♔"
