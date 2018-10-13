from IOStream import io
from Item import *
from copy import copy

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

	def get_entities(self, who_for, initial = False):
		"""
		If verbose is true, we will print information for non-existent stuff.
		Should be set only for detailed looking.
		"""

		entities_except_current = self.entities[:].remove(who_for)

		if not entities_except_current:
			if not initial:
				io.out('There is no one else in the room.')

			return False
		else:
			output = ["There is a(n)"]
			for i,thing in enumerate(entities_except_current):
				output.append(str(thing)+"("+str(i)+")")
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
			output = ["You can see"]
			for i, thing in enumerate(self.items):
				thing_object = thing[0]
				thing_amount = thing[1]

				output.append(str(thing_amount) + " " + thing_object.name+"("+str(i)+")")

			output.append("in this room.")

			io.out(", ".join(output))

		io.out('Use inspect room [id] to inspect an item in this room.')

		return True

	def describe(self, who_for, initial = True):
		if initial:
			io.out(self.name.upper())

		io.out(self.description)
		io.out("")
		self.get_entities(initial = initial, who_for = who_for)
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

	def add_item(self, item, amount = 1):
		"""adds the item to the players inventory if it is an item"""

		if not isinstance(item,Item):
			return False

		amount_updated = False

		for i, slot in enumerate(self.items):
			slot_item = slot[0]
			slot_amount = slot[1]

			if item != slot_item:
				continue

			slot_amount += amount

			amount_updated = True
			break

		if not amount_updated:
			self.items.append([item, amount])

		return True

	def remove_item(self, index):
		"""returns the item if the player has it
		else returns none"""

		try:
			item, amount = self.items[index]
		except IndexError:
			return None

		if amount == 1:
			del self.items[index]
			return item
		else:
			self.items[index][1] -= 1
			return copy.deepcopy(item)
		
