from IOStream import io
from Room import Room

class Parser(object):

	def __init__(self, game):
		self.game = game

	def parse_move(self, words):
		if words[0] != 'go' and words[0] != 'move':
			return None

		if len(words) != 2:
			io.out('USAGE: [move/go] [direction]')
			return False

		direction = words[1].lower()

		if direction not in Room.ALLOWED_PATHS:
			io.out('That is not a valid direction to move to.')
			return False

		next_room = self.game.p.at.get_room_at(direction)

		if not next_room:
			io.out('There is nothing in that direction.')
			return False

		if next_room.locked:
			io.out('The room is locked and you cannot go in.')
			return False

		self.game.p.at = next_room
		next_room.describe()
		return True

	def parse_inventory(self, words):
		if len(words) != 1 or (words[0] != 'inventory' and words[0] != 'inv'):
			return None

		self.game.p.show_inventory()
		return True

	def parse_observe_room(self, words):
		if len(words) != 1 or (words[0] != 'look' and words[0] != 'inspect'):
			return None

		self.game.p.at.describe(initial = False)
		return True

	def parse_pep(self, words):
		if len(words) != 1 or (words[0] != 'pep' and words[0] != 'stats' and words[0] != 'skills'):
			return None

		self.game.p.show_pep()
		return True

	def parse(self, str):
		words = str.strip().split()

		if not words:
			return

		not self.parse_move(words) and not self.parse_inventory(words) and not self.parse_observe_room(words) and not self.parse_pep(words)
