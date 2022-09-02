"""A game of chess."""
from .board import Board
from .pieces import Color, Piece
from .square import Square


Score = tuple[int, int]
Checkmate = bool


class Chess:
    """A chess game."""

    def __init__(self):
        """Start a chess game."""
        self._board = Board()

    def _take_turns(self, color: Color) -> tuple[Score, Checkmate]:
        """A player's turn, where he selects a piece to move and a target square to move to.

        Args:
            color: the color of the player.

        Returns:
            a tuple of the current score and whether the game has ended with checkmate.
        """
        piece = None
        selected_square = None
        print(self._board)
        # will loop until all a proper square is selected.
        while True:
            selected_square = Square(input("Choose a piece to move: "))
            piece = self._board[selected_square]
            if piece is not None and piece.color == color:
                break
            print("Invalid square selection.")
        move_selection = self._board.list_moves(selected_square)
        # if there are no selections, game is over.
        # TODO: fix this, it's should be true only for the King.
        # this needs work, since it should backtrack to a new selection.
        if len(move_selection) == 0:
            return (0, 0), True
        
        choice:int | None = None
        while choice is None:
            self._print_options(move_selection)
            choice = input("Choose target square from the above options: ")
            if Square(choice) not in move_selection:
                print("Invalid option.")
                choice = None

        target_square = Square(choice)
        other_piece = self._move(piece, selected_square, target_square)
        if other_piece is not None:
            return ((other_piece.value, 0), False) if color == Color.white else ((0, other_piece.value), False)
        return (0, 0), False

    def run(self) -> tuple[Score, Color]:
        """Start the game of chess, it finishes when a checkmate occurs.

        Returns:
            the final score of the game and the color of the winner.
        """
        game_over = False
        color = Color.white
        score = (0, 0)
        while not game_over:
            diff_score, checkmate = self._take_turns(color)
            score = self._update_score(score, diff_score)
            color = Color.white if color == Color.black else Color.black
            if checkmate:
                game_over = True
                winner = color
            
        return score, winner

    @staticmethod
    def _update_score(score: Score, diff_score: tuple[int, int]) -> Score:
        """Update the score after a move was made.

        Args:
            score: the previous score before the move.
            diff_score: how much the score changed.

        Returns:
            the new score.
        """
        score_white, score_black = score
        diff_white, diff_black = diff_score
        return score_white + diff_white, score_black + diff_black

    def _move(self, piece: Piece, start_square: Square, target_square: Square) -> Piece:
        """Move a piece on the board, returning any enemy piece captured.

        Args:
            piece: the piece to move
            start_square: the starting position of the piece.
            target_square: the position the piece will move to.

        Returns:
            any enemy piece that is captured because of the move.
        """
        other_piece = self._board[target_square]
        self._board[start_square], self._board[target_square] = None, piece

        return other_piece

    def _print_options(self, move_selection: set[Square]) -> None:
        """Print movement options to the screen.
        
        Args:
            move_selection: the moves to be printed.

        Returns:
            Nothing, only prints to screen.
        """
        for target_square in move_selection:
            other_piece = self._board[target_square]
            if other_piece is not None:
                print(f"- Option: {target_square} capturing {other_piece}.")
            else:
                print(f"- Option: {target_square}")


if __name__ == "__main__":
    game = Chess()
    score, winner = game.run()
    print(score, winner)
