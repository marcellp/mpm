from IOStream import io
from Room import Room
from Entity import Entity, Human
from Item import Item,Weapon,Clothing
from Parser import Parser
import json
import pickle
import copy

class Game(object):
	def __init__(self):
		self.parser = Parser(self)
		#self.assets #filled in load assets
		self.load_assets()
		self.load_rooms()

	def load_rooms(self):
		r1 = Room("Dark Room", "This is a very dark room.")
		r2 = Room("Dim Room", "This is a slightly brighter room.")
		
		f = self.get_item("Baseball bat")
		r1.add_item(f)

		r1.paths["down"] = r2
		r2.paths["up"] = r1

		self.rooms = (r1, r2)

	def save_rooms(self):
		if not self.rooms:
			raise Exception("rooms not loaded boi")

		with open("rooms.bin", "wb") as rooms:
			pickle.dump(self.rooms, rooms)

	def load_assets(self):
		"""read from json file parse to tuples as types, copy into rooms from here"""
		with open("weapons.json") as f:
			raw_file_data = json.load(f)
		weapons = tuple(Weapon(x) for x in raw_file_data)

		with open("clothing.json") as f:
			raw_file_data = json.load(f)
		clothing = tuple(Clothing(x) for x in raw_file_data)

		#tuple of all assets
		self.assets = clothing + weapons


	def create_character(self):
		while True:
			name = io.send_in('By what name should I call you? > ').strip()
			if name:
				break

		while True:
			sex = io.send_in("Okay, " + name + ", what is your sex? (male, female) > ").strip()

			if sex == "male" or sex == "female":
				break

		p = Human(name, sex, local_player = True)
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

	def get_item(self,searchStr):
		"""looks in assets for the specified search key
			returns none if not found"""
		for item in self.assets:
			if searchStr == item.name:
				return copy.deepcopy(item)

	def show_intro(self):
		with open("title.txt") as f:
			for line in f:
				print(line,end="")

			print("\n")

		with open("intro.txt") as f:
			for line in f:
				print(line,end="")
			print("\n")

	def run(self):
		self.show_intro()
		self.p = self.create_character()
		c = self.get_item("Kevlar vest")
		self.p.add_item(c)

		io.out('')

		# Game loop
		self.p.at.describe()
		
		while True:
			words = io.send_in()
			self.parser.parse(words)

g = Game()
g.run()