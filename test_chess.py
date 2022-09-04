"""Unit tests for the Chess project."""

from collections.abc import Generator
from pytest import fixture


initial_board_state = """
▐\033[7m  A B C D E F G H  \033[0m▌
▐\033[7m8\033[27m\033[4m▌♜│♞│♝│♛│♚│♝│♞│♜▐\033[24m\033[7m8\033[0m▌
▐\033[7m7\033[27m\033[4m▌♟│♟│♟│♟│♟│♟│♟│♟▐\033[24m\033[7m7\033[0m▌
▐\033[7m6\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m6\033[0m▌
▐\033[7m5\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m5\033[0m▌
▐\033[7m4\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m4\033[0m▌
▐\033[7m3\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m3\033[0m▌
▐\033[7m2\033[27m\033[4m▌♙│♙│♙│♙│♙│♙│♙│♙▐\033[24m\033[7m2\033[0m▌
▐\033[7m1\033[27m\033[4m▌♖│♘│♗│♕│♔│♗│♘│♖▐\033[24m\033[7m1\033[0m▌
▐\033[7m  A B C D E F G H  \033[0m▌

"""


class MockInput:
    """Mocks the input_ stream to the chess game."""

    def __init__(self, xs: list[str]) -> None:
        """Initialize MockInput with a list of selections."""
        self._xs = [None, *xs]
        self._g = self._make_generator()
        next(self._g)

    def _make_generator(self) -> Generator[str, None, str]:
        for x in self._xs:
            _ = yield x

    def __call__(self, text: str) -> str:
        """Make MockInput a callable that returns the items in the list."""
        return self._g.send(text)


class TestBoard:
    """Unit tests for the board."""

    def test_board(self):
        """Test initial state of the board."""
        from src.board import Board

        assert repr(Board()) == initial_board_state

    def test_square_of(self):
        """Test piece referencing on the board."""
        from src.board import Board

        board = Board()

        for rank in board._board:
            for piece in rank:
                assert board[board.square_of(piece)] is piece


class TestSquare:
    """Unit tests exclusive to the squares."""

    def test_square_operations(self):
        """Test that squares can safely be operated on and that operations can be stacked."""
        from src.square import Square, Vector

        assert Square("e4") + Vector(-1, 0) == Square("e5")
        assert Square("e4") + Vector(0, -1) == Square("d4")
        assert Square("e4") + Vector(+1, 0) == Square("e3")
        assert Square("e4") + Vector(0, +1) == Square("f4")


class TestPiece:
    """Unit tests for pieces."""

    def test_legal_moves(self):
        """Test whether the pieces generate proper legal moves. One example for each piece."""
        from src.piece import Bishop, Color, King, Knight, Pawn, Queen, Rook
        from src.square import Square

        def condition(sq: Square) -> tuple[bool, None]:
            return sq.is_in_board(), None

        assert Pawn(Color.white).legal_moves(Square("h2"), condition) == {
            Square("h3"),
            Square("h4"),
        }
        assert King(Color.white).legal_moves(Square("e1"), condition) == {
            Square("e2"),  # TODO: No piece blocking yet
            Square("d2"),  # TODO: No piece blocking yet
            Square("d1"),  # TODO: No piece blocking yet
            Square("f1"),  # TODO: No piece blocking yet
            Square("f2"),  # TODO: No piece blocking yet
            Square("e2"),  # TODO: No piece blocking yet
        }
        assert Knight(Color.white).legal_moves(Square("g1"), condition) == {
            Square("h3"),
            Square("f3"),
            Square("e2"),  # TODO: No piece blocking yet
        }
        assert Rook(Color.white).legal_moves(Square("h1"), condition) == {
            Square("h2"),  # TODO: No piece blocking yet
            Square("h3"),  # TODO: No piece blocking yet
            Square("h4"),  # TODO: No piece blocking yet
            Square("h5"),  # TODO: No piece blocking yet
            Square("h6"),  # TODO: No piece blocking yet
            Square("h7"),  # TODO: No piece blocking yet
            Square("h8"),  # TODO: No piece blocking yet
            Square("g1"),  # TODO: No piece blocking yet
            Square("f1"),  # TODO: No piece blocking yet
            Square("e1"),  # TODO: No piece blocking yet
            Square("d1"),  # TODO: No piece blocking yet
            Square("c1"),  # TODO: No piece blocking yet
            Square("b1"),  # TODO: No piece blocking yet
            Square("a1"),  # TODO: No piece blocking yet
        }
        assert Bishop(Color.white).legal_moves(Square("f1"), condition) == {
            Square("e2"),  # TODO: No piece blocking yet
            Square("d3"),  # TODO: No piece blocking yet
            Square("c4"),  # TODO: No piece blocking yet
            Square("b5"),  # TODO: No piece blocking yet
            Square("a6"),  # TODO: No piece blocking yet
            Square("g2"),  # TODO: No piece blocking yet
            Square("h3"),  # TODO: No piece blocking yet
        }
        assert Queen(Color.white).legal_moves(Square("d1"), condition) == {
            Square("d2"),  # TODO: No piece blocking yet
            Square("d3"),  # TODO: No piece blocking yet
            Square("d4"),  # TODO: No piece blocking yet
            Square("d5"),  # TODO: No piece blocking yet
            Square("d6"),  # TODO: No piece blocking yet
            Square("d7"),  # TODO: No piece blocking yet
            Square("d8"),  # TODO: No piece blocking yet
            Square("c2"),  # TODO: No piece blocking yet
            Square("b3"),  # TODO: No piece blocking yet
            Square("a4"),  # TODO: No piece blocking yet
            Square("c1"),  # TODO: No piece blocking yet
            Square("b1"),  # TODO: No piece blocking yet
            Square("a1"),  # TODO: No piece blocking yet
            Square("e1"),  # TODO: No piece blocking yet
            Square("f1"),  # TODO: No piece blocking yet
            Square("g1"),  # TODO: No piece blocking yet
            Square("h1"),  # TODO: No piece blocking yet
            Square("e2"),  # TODO: No piece blocking yet
            Square("f3"),  # TODO: No piece blocking yet
            Square("g4"),  # TODO: No piece blocking yet
            Square("h5"),  # TODO: No piece blocking yet
        }


class TestChessGame:
    """Test a chess game object."""

    def test_one_turn(self):
        """Take one turn, just the white player."""
        from src.chess import Chess
        from src.board import Board

        game_sequence = MockInput(["d2", "d3"])

        board_after_step = Board()
        board_after_step["d2"], board_after_step["d3"] = None, board_after_step["d2"]

        def ending(board: Board, color) -> bool:
            return board_after_step == board

        game = Chess(input_=game_sequence, ending_condition=ending)
        game.run()
        assert game._board == board_after_step

    def test_two_turns(self, game_sequence_two_turns):
        """Play two turns, one white one black."""
        from src.chess import Chess
        from src.board import Board
        from src.piece import Color

        game_sequence = MockInput(["d2", "d3", "e7", "e5"])

        board_after_steps = Board()
        board_after_steps["d2"], board_after_steps["d3"] = None, board_after_steps["d2"]
        board_after_steps["e7"], board_after_steps["e5"] = None, board_after_steps["e7"]

        def ending(board: Board, color: Color) -> bool:
            return board_after_steps == board

        game = Chess(input_=game_sequence, ending_condition=ending)
        game.run()
        assert game._board == board_after_steps

    def test_fools_mate(self):
        """Finish game by fool's mate."""
        from src.chess import Chess
        from src.piece import Color

        game_sequence = MockInput(["f2", "f3", "e7", "e5", "g2", "g4", "d8", "h4", "e1"])
        game = Chess(input_=game_sequence)
        _, color = game.run()
        assert color == Color.black
