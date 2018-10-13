from IOStream import io

class Room(object):

	ALLOWED_PATHS = ('up', 'down', 'left', 'right', 'north', 'south', 'east', 'west')

	def __init__(self, name, description = None):
		self.name = name
		self.interior = True
		self.paths = {direction : None for direction in Room.ALLOWED_PATHS}

		if not description:
			self.description = "You see an empty room"
		else:
			self.description = description

		self.path_text = ""
		self.items = []
		self.entities = []
		self.locked = False

	def describe(self):
		io.out(self.name.upper())
		io.out(self.description)
		io.out("")

		directions = [direction for (direction, room) in self.paths.items() if room]

		if self.path_text:
			io.out(self.path_text)
		elif not self.paths:
			io.out('It appears there is no way out of this room.')
		else:
			io.out("You can go {}.".format(', '.join(directions)))

	def get_room_at(self, direction):
		direction = direction.lower()

		if direction not in Room.ALLOWED_PATHS:
			return False

		return self.paths[direction]
