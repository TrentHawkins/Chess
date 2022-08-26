import numpy

class Piece(object):
	def __init__(self, color: str):
		self.color = color # clear color representation in string form
		self.black = True if self.color=="black" else False
		self.direction = -1 if self.black else +1 # black moves up the board ( - 1) and black down the board ( + 1)

	def __repr__(self):
		return f"{self.__class__.__name__}({self.color})"

	def valid_steps(self):
		raise NotImplementedError

class Pawn(Piece):
	def __init__(self, color: bool):
		super(Pawn, self).__init__(color)
		self.value = 1

	def __repr__(self):
		return "♟" if self.black else "♙"

class Bishop(Piece):
	def __init__(self, color: bool):
		super(Bishop, self).__init__(color)
		self.value = 3

	def __repr__(self):
		return "♝" if self.black else "♗"

class Knight(Piece):
	def __init__(self, color: bool):
		super(Knight, self).__init__(color)
		self.value = 3

	def __repr__(self):
		return "♞" if self.black else "♘"

class Rook(Piece):
	def __init__(self, color: bool):
		super(Rook, self).__init__(color)
		self.value = 5

	def __repr__(self):
		return "♜" if self.black else "♖"

class Queen(Piece):
	def __init__(self, color: bool):
		super(Queen, self).__init__(color)
		self.value = 9

	def __repr__(self):
		return "♛" if self.black else "♕"

class King(Piece):
	def __init__(self, color: bool):
		super(King, self).__init__(color)
		self.value = None

	def __repr__(self):
		return "♚" if self.black else "♔"
