from IOStream import io
from Room import Room

class Parser(object):

	def __init__(self, game):
		self.game = game

	def parse_move(self, words):
		if words[0] != 'go' and words[0] != 'move':
			return None

		if len(words) < 2:
			io.out('USAGE: [move/go] [direction]')
			return False

		direction = " ".join(words[1:]).lower()

		try:
			next_room = self.game.p.at.get_room_at(direction)
		except KeyError:
			io.out('That is not a valid direction.')
			return False

		if not next_room:
			io.out('There is nothing in that direction.')
			return False

		if next_room.locked:
			io.out('The room is locked and you cannot go in.')
			return False

		self.game.p.move_to(next_room)
		next_room.describe(self.game.p)
		return True

	def parse_inventory(self, words):
		if len(words) != 1 or (words[0] != 'inventory' and words[0] != 'inv'):
			return None

		self.game.p.show_inventory()
		return True

	def parse_observe_room(self, words):
		if len(words) != 1 or (words[0] != 'look' and words[0] != 'inspect'):
			return None

		self.game.p.at.describe(who_for = self.game.p, initial = False)
		return True

	def parse_observe_item(self, words):
		if len(words) != 3 or (words[0] != 'look' and words[0] != 'inspect') or (words[1] != "room" and words[1] != "inventory"):
			return None

		try:
			index = int(words[2])
		except:
			io.out('USAGE: [look/inspect] [room/inventory] [index]')
			return False

		target = words[1]

		if target == "room":
			try:
				item = self.game.p.at.items[index]
			except IndexError:
				io.out('That item does not exist.')
				return None

			item.describe()
		elif target == "inventory":
			try:
				item = self.game.p.inventory[index]
			except IndexError:
				io.out('That item does not exist.')
				return None

			item.describe()
		else:
			return False

		return True

	def parse_pep(self, words):
		if len(words) != 1 or (words[0] != 'pep' and words[0] != 'stats' and words[0] != 'skills'):
			return None

		self.game.p.show_pep()
		return True

	def parse_player_room_item_interaction(self, words):
		"""
		false: pickup
		true: drop
		none: invalid
		"""

		action = None
		player = self.game.p
		room = self.game.p.at

		if words[0] == "pickup":
			action = False
		elif words[0] == "drop":
			action = True
		else:
			return False

		if len(words) != 2:
			io.out('USAGE: [pickup/drop] [item id]. Get item id from `look`.')
			return False

		try:
			index = int(words[1])
		except:
			io.out('Invalid index specified.')
			return False

		if action:
			item = player.remove_item(index)

			print("we are removing", item)

			if not item:
				io.out('That is not a valid item.')
				return False

			room.add_item(item)

			io.out('You have successfully dropped {} in {}.'.format(item, room))

		if not action:
			item = room.remove_item(index)

			if not item:
				io.out('That is not a valid item.')
				return False

			player.add_item(item)
			io.out('You have successfully picked up {} from {}.'.format(item, room))

		return True

	def parse_use_item(self, words):
		if len(words) == 0 or words[0] != 'use':
			return None

		if len(words) == 1:
			io.out('USAGE: use [item id]. Get item id from `look`.')
			return False

		try:
			index = int(words[1])
		except:
			io.out('Invalid index specified.')
			return False

		try:
			item = self.game.p.inventory[index]
		except IndexError:
			io.out('This is not a valid item.')
			return False

		item[0].use(self.game.p)
		return True

	def parse(self, str):
		words = str.strip().split()

		if not words:
			return

		not self.parse_move(words) and not self.parse_inventory(words) and not self.parse_observe_room(words) and not self.parse_observe_item(words) and not self.parse_pep(words) and not self.parse_player_room_item_interaction(words) and not self.parse_use_item(words)
