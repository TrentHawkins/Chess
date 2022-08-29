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


Move = tuple[int, int]


def horizontal(move:Move) -> int:
    return move[0]


def vertical(move:Move) -> int:
    return move[1]


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

    def check_movement(self, move:Move, captured:"Piece") -> bool:
        raise NotImplemented("Each subtype of Piece has its own valid movements.")

    def unit_move(self, move:Move) -> Move:
        raise NotImplemented("Each subtype of Piece has its own valid movements.")


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
    
    def check_movement(self, move:Move, captured:Piece | None) -> bool:
        """Checks whether the Pawn is allowed to execute the move given.
        
        Args:
            move: the move to execute
            captured: whether a Piece is captured as a result of the move.
        Returns:
            a truth value indicating whether the move is valid.
        """
        x, y = move
        return y == 0 and ((not self.is_black and x == -1) or (self.is_black and x == 1))

    def unit_move(self, move: Move) -> Move:
        return move


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

    def check_movement(self, move:Move, piece:Piece | None):
        return (horizontal(move) != 0) ^ (vertical(move) != 0)

    def unit_move(self, move:Move) -> Move:
        if horizontal(move) > 0 and vertical(move) == 0:
            return (1, 0)
        if horizontal(move) < 0 and vertical(move) == 0:
            return (-1, 0)
        if horizontal(move) == 0 and vertical(move) > 0:
            return (0, 1)
        if horizontal(move) == 0 and vertical(move) < 0:
            return (0, -1)
        raise ValueError("Rook cannot move diagonally!")
        

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
