from IOStream import IOStream
from Room import Room
import pickle

class Game(object):

	def __init__(self):
		self.rooms = self.load_rooms()
		pass

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
		self.rooms = [Room("Dark room")]
		self.save_rooms()

	def run(self):
		io = IOStream()

		io.out("mpm version 1 loaded")

		while True:
			self.rooms[0].describe()
			io.send_in()


g = Game()
g.run()