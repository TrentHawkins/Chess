from dataclasses import dataclass


@dataclass
class Piece:
    color: str

    def valid_steps(self):
        raise NotImplementedError

    @property
    def is_black(self):
        return self.color == "black"


@dataclass
class Pawn(Piece):
    value: int = 1

    def __repr__(self):
        return "♟" if self.is_black else "♙"


@dataclass
class Bishop(Piece):
    value: int = 3

    def __repr__(self):
        return "♝" if self.is_black else "♗"


@dataclass
class Knight(Piece):
    value: int = 3

    def __repr__(self):
        return "♞" if self.is_black else "♘"


@dataclass
class Rook(Piece):
    value: int = 5

    def __repr__(self):
        return "♜" if self.is_black else "♖"


@dataclass
class Queen(Piece):
    value: int = 9

    def __repr__(self):
        return "♛" if self.is_black else "♕"


@dataclass
class King(Piece):

    def __repr__(self):
        return "♚" if self.is_black else "♔"
