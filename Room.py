class Room(object):
	def __init__(self, name):
		self.name = name
		self.paths = {"up": None, "down": None, "left": None, "right": None}
		self.description = "You see an empty room"
		self.items = []
		self.entities = []

	def describe(self):
		print(self.name.upper())
		print(self.description)
