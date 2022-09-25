"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from dataclasses import dataclass
from types import MethodType

from .board import Board
from .piece import Orientation, Piece
from .pieces.meleed import King
from .square import Square


@dataclass(init=False, repr=False)
class Player:
    """A player.

    Attributes:
        name: The player's name.
        board: The board this player is playing on.
        orientation: The allegiance of the player, defining the correspponding orientation of the board.
        pieces: A collection of the player's pieces on the board.
        captured: A collection of captured pieces hashed by piece type.
            NOTE: All captured pieces are expected to have `square == None` making them distinct only by type.
    """

    def __init__(self, name: str, color: str, board: Board):
        """Create collections for player.

        Args:
            name: The player's name.
            color: The color of the player's pieces.
            board: The board this player is playing on.

        Also defines player-context-sensitive rules for evaluating piece legal moves.
        King safety is not relevant nor can be resolve here.
        The piece legal moves shall be agnostically updated here though,
        because the squares the player checks are legit, since king safety is irrelevant when it is not their turn!
        In elaboration, if an opponent walks their king in danger, it does not matter if your king will be in danger after;
        their king will die first.
        """
        self.name: str = name
        self.orientation: Orientation = Orientation[color]  # The allegiance of the player.
        self.board: Board = board  # The board this player is playing on.

    #   Assign pieces to player agnostically, so that custom position can also be loaded.
        self.pieces: set[Piece] = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured: Counter = Counter()  # In custom positions, captured material is immaterial.

        def piece_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

            return source_piece.__class__.deployable(source_piece, target) \
                and target_piece is None

        def piece_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            if target_piece is not None:
                return source_piece.__class__.capturable(source_piece, target) \
                    and source_piece.orientation != target_piece.orientation

            return False

        for piece in self.pieces:
            piece.deployable = MethodType(piece_deployable, piece)
            piece.capturable = MethodType(piece_capturable, piece)

    #   Keep the player's king registered, as it is a special piece.
        for piece in self.pieces:
            if isinstance(piece, King):
                self.king: King = piece

    def __repr__(self):
        """Represent a player by name and captured pieces.

        NOTE: Timer is not implemented yet.

        Returns:
            Players name followed by a color window and captured pieces
        """
        ...

    @property
    def squares_checked(self) -> set[Square]:
        """Get all squares checked by player.

        Returns:
            A flattened union of all squares the player has access to.
        """
        return set().union(*(piece.squares for piece in self.pieces))

    def move(self, piece: Piece, target: Square | str):
        """Move whatever is in source square to target square if move is valid.

        Args:
            piece: The piece to move.
            target: The square in notation the piece wants to go to.

        NOTE: A `Move` class will be made to encapsulate moves, this will be moved there.
        """
        target = Square(target)
        source = piece.square

        if source is not None:  # If piece is on the board,
            if target in piece.squares:  # If the target square is legal for the piece,
                self.board[target], self.board[source] = piece, None  # Move the piece to the target square.

                piece.has_moved = True  # The pawns at theirstart and kings and rooks for castling use this flag.
