from IOStream import io
from Item import *

class Room(object):

	def __init__(self, name, description = None):
		self.name = name
		self.interior = True
		self.paths = {}

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
			output = ["There is a(n)"]
			for i,thing in enumerate(self.entities):
				output.append(thing+"("+str(i)+")")
			output.append("in this room")

			io.out(" ".join(output))

		return True

	def get_items(self, initial):
		if initial:
			return True

		if not self.items:
			io.out('There are no items in the room.')
			return False
		else:
			print(self.items)
			output = ["There is a(n)"]
			for i,thing in enumerate(self.items):
				output.append(thing+"("+str(i)+")")

			output.append("in this room.")

			io.out(", ".join(output))

		return True

	def describe(self, initial = True):
		if initial:
			io.out(self.name.upper())

		io.out(self.description)
		io.out("")
		self.get_entities(initial)
		self.get_items(initial)
		self.get_directions()

	def get_room_at(self, direction):
		direction = direction.lower()

		return self.paths[direction]

	def remove_item(self, itemid):
		try:
			item = self.items[itemid]
		except IndexError:
			return None

		del self.items[itemid]
		return item

	def __str__(self):
		return self.name

	def add_item(self, item):

		if isinstance(item,Item):
			self.items.append(item)
			return True
		else:
			return False