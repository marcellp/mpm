from IOStream import io
from Room import Room
from Entity import Entity
from Player import Player
from Item import Item
from Parser import Parser
import pickle

class Game(object):

	def __init__(self):
		self.rooms = self.load_rooms()
		self.parser = Parser(self)

	def load_rooms(self):
		with open("rooms.bin", "rb") as rooms:
			rooms = pickle.load(rooms)

		return rooms

	def save_rooms(self):
		if not self.rooms:
			raise Exception("rooms not loaded boi")

		with open("rooms.bin", "wb") as rooms:
			pickle.dump(self.rooms, rooms)

	def debug(self):
		r = Room("Dark room")
		r.paths["up"] = True
		r.paths["down"] = True

		self.rooms = [r]
		self.save_rooms()

	def create_character(self):
		while True:
			name = io.send_in('By what name should I call you? > ').strip()
			if name:
				break

		while True:
			sex = io.send_in("Okay, " + name + ", what is your sex? (male, female) > ").strip()

			if sex == "male" or sex == "female":
				break

		p = Player(name, sex)
		io.out("Good job, {}. To create your character, assign some skills to your character.\n".format(name))
		
		"""
		Here be dragons.
		"""
		while True:
			assignable_points = Entity.MAX_SPECIAL_POINTS
			total_points = 0
			i = 1
			out_of = len(p.stats) - 1

			for stat in p.stats.keys():
				if stat == "level":
					continue

				while True:
					try:
						points = io.send_in("[{}/{}] Assign points for {} (default: 5, minimum: 1, maximum: 10 {}/{} assigned). > ".format(i, out_of, stat.upper(), total_points, assignable_points))
						points = int(points)
					except ValueError:
						io.out("I'll take that as 5.")
						points = 5

					if points < 1 or points > 10:
						io.out('Points must be between 1 and 10.')
						continue

					if total_points == assignable_points and i <= out_of:
						break

					if total_points + points > assignable_points:
						io.out('You cannot assign this many points.')
						continue

					p.stats[stat] = points
					total_points += points
					i += 1
					break

				if total_points == assignable_points and i <= out_of:
					io.out('You used up your points a bit too fast there. Let us try again....\n')
					break

			if i > out_of:
				break

		# Character stats created, let us put the character into the first available room.
		p.at = self.rooms[0]

		return p


	def run(self):
		io.out("mpm version 1 loaded\n")
		self.p = self.create_character()
		i = Item("Cola","Delicious diabetes-inducing beverage", 0.1, None)
		self.p.add_item(i)

		io.out('')

		# Game loop
		self.p.at.describe()
		
		while True:
			words = io.send_in()
			self.parser.parse(words)

def fuck_all_rooms():
	r1 = Room("Dark Room", "This is a very dark room.")
	r2 = Room("Dim Room", "This is a slightly brighter room.")
	r1.paths["down"] = r2
	r2.paths["up"] = r1

	roomlist = [r1, r2]

	with open("rooms.bin", "wb") as rooms:
		pickle.dump(roomlist, rooms)

fuck_all_rooms()
g = Game()
g.run()