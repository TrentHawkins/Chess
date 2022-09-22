"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from dataclasses import dataclass
from types import MethodType

from .board import Board
from .piece import Orientation, Piece
from .square import Square


@dataclass(init=False, repr=False)
class Player:
    """A player.

    Attributes:
        board: The board this player is playing on.
        orientation: The allegiance of the player, defining the correspponding orientation of the board.
        pieces: A collection of the player's pieces on the board.
        captured: A collection of captured pieces hashed by piece type.
            NOTE: All captured pieces are expected to have `square == None` making them distinct only by type.
    """

    def __init__(self, board: Board, color: str):
        """Create collections for player.

        Args:
            board: The board this player is playing on.
            orientation: The allegiance of the player, defining the correspponding orientation of the board.
        """
        self.board: Board = board  # The board this player is playing on.
        self.orientation: Orientation = Orientation[color]  # The allegiance of the player.

    #   Assign pieces to player agnostically, so that custom position can also be loaded.
        self.pieces = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured = Counter()  # In custom positions, captured material is immaterial.

    @property
    def moves(self):
        """Generate moves for all pieces of player on the board.

        Return:
            A dictionary containing all possible moves for each square player has a piece on.

        NOTE: Ideally the piece would be used as key but it is unhashable.
        """
        _moves = {}

    #   Check only pieces of player:
        for piece in self.pieces:
            def deployable(source_piece: Piece, target: Square):
                Piece.deployable.__doc__
                target_piece = self.board[target]

                return Piece.deployable(source_piece, target) and target_piece is None

            def capturable(source_piece: Piece, target: Square):
                Piece.capturable.__doc__
                target_piece = self.board[target]

            #   If there is a piece on the target, check their allegiance.
                if target_piece is not None:
                    return Piece.capturable(source_piece, target) and source_piece.orientation != target_piece.orientation

                return False

            piece.deployable = MethodType(deployable, piece)
            piece.capturable = MethodType(capturable, piece)

            _moves[piece] = piece.moves

        return _moves

    def move(self, piece: Piece, target: Square | str):
        """Move whatever is in source square to target square if move is valid.

        Args:
            source: The square in notation the piece is on
            target: The square in notation the piece wants to go to.
        """
        target = Square(target)

        source = piece.square

        if source is not None and piece in self.moves:
            if target in self.moves[piece]:
                self.board[source], self.board[target] = None, piece

                piece.has_moved = True
