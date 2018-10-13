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

	def get_directions(self):
		directions = [direction for (direction, room) in self.paths.items() if room]

		if self.path_text:
			io.out(self.path_text)
		elif not self.paths:
			io.out('It appears there is no way out of this room.')
		else:
			io.out("You can go {}.".format(', '.join(directions)))

	def get_entities(self, initial = False):
		"""
		If verbose is true, we will print information for non-existent stuff.
		Should be set only for detailed looking.
		"""

		if not self.entities:
			if not initial:
				io.out('There is no one else in the room.')

			return False
		else:
			for entity in self.entities:
				io.out('There is a(n) {} in this room.'.format(", a(n)".join(self.entities)))

		return True

	def get_items(self, initial):
		if initial:
			return True

		if not self.items:
			io.out('There are no items in the room.')
			return False
		else:
			for entity in self.entities:
				io.out('There is a(n) {} in this room.'.format(", a(n)".join(self.entities)))

		return True

	def describe(self, initial = True):
		if initial:
			io.out(self.name.upper())

		io.out(self.description)
		io.out("")
		self.get_entities(initial)
		self.get_items(initial)

	def get_room_at(self, direction):
		direction = direction.lower()

		if direction not in Room.ALLOWED_PATHS:
			return False

		return self.paths[direction]
