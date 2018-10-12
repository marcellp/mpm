from IOStream import io

class Room(object):
	def __init__(self, name, interior = True):
		self.name = name
		self.interior = interior

		self.paths = {"up": None, "down": None, "left": None, "right": None}
		self.description = "You see an empty room"
		self.items = []
		self.entities = []
		self.locked = False

	def describe(self):
		io.out(self.name.upper())
		io.out(self.description)
		io.out("")

		directions = [direction for (direction, room) in self.paths.items() if room]

		if not directions:
			io.out('It appears there is no way out of this room.')

		io.out("You can go {}.".format(', '.join(directions)))