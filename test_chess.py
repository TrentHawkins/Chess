"""Unit tests for the Chess project."""

initial_board_state = """
▐\x1b[7m  A B C D E F G H  \x1b[0m▌
▐\x1b[7m8\x1b[27m\x1b[4m▌♜│♞│♝│♛│♚│♝│♞│♜▐\x1b[24m\x1b[7m8\x1b[0m▌
▐\x1b[7m7\x1b[27m\x1b[4m▌♟│♟│♟│♟│♟│♟│♟│♟▐\x1b[24m\x1b[7m7\x1b[0m▌
▐\x1b[7m6\x1b[27m\x1b[4m▌ │ │ │ │ │ │ │ ▐\x1b[24m\x1b[7m6\x1b[0m▌
▐\x1b[7m5\x1b[27m\x1b[4m▌ │ │ │ │ │ │ │ ▐\x1b[24m\x1b[7m5\x1b[0m▌
▐\x1b[7m4\x1b[27m\x1b[4m▌ │ │ │ │ │ │ │ ▐\x1b[24m\x1b[7m4\x1b[0m▌
▐\x1b[7m3\x1b[27m\x1b[4m▌ │ │ │ │ │ │ │ ▐\x1b[24m\x1b[7m3\x1b[0m▌
▐\x1b[7m2\x1b[27m\x1b[4m▌♙│♙│♙│♙│♙│♙│♙│♙▐\x1b[24m\x1b[7m2\x1b[0m▌
▐\x1b[7m1\x1b[27m\x1b[4m▌♖│♘│♗│♕│♔│♗│♘│♖▐\x1b[24m\x1b[7m1\x1b[0m▌
▐\x1b[7m  A B C D E F G H  \x1b[0m▌

"""


class TestBoard:
    """Unit tests for the board."""

    def test_board(self):
        """Test initial state of the board."""
        from src.board import Board
        assert str(Board()) == initial_board_state
