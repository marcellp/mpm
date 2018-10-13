from enum import Enum
from IOStream import io

class Item(object):

	def __init__(self, name, desc = None, value = 0, weight = 0, container = False):
		self.name = name
		self.attributes = None
		if desc:
			self.desc = desc
		else:
			self.desc = "Yep. Looks like an item to me."

		self.value = value
		self.weight = weight

		self.container = container

		if self.container:
			self.inventory = []
		else:
			self.inventory = None

	def __str__(self):
		return self.name

	def describe(self):
		print(self.name,
			  "\n\tDescription: ",self.desc,
			  "\n\tValue: ",self.value,
			  "\n\tWeight: ",self.weight,)

		if self.attributes:
			for attr in self.attributes:
				print("\t", attr, ": ", self.attributes[attr])

	def use(self):
		io.out('You marvel at the magnificence of this item.')
		return True

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

class Weapon(Item):
	#structure as in the json in main

	def __init__(self, weaponJson):
		#for inherited attributes
		Item.__init__(self,weaponJson["name"],weaponJson["desc"],
					  weaponJson["value"],weaponJson["weight"])
		#assign actual weapon properties in here
		self.attributes = weaponJson["attributes"]
	

class Clothing(Item):
	def __init__(self, clothingJson):

		#for inherited attributes
		Item.__init__(self,clothingJson["name"],clothingJson["desc"],
					  clothingJson["value"],clothingJson["weight"])
		#assign actual weapon properties in here
		self.attributes = clothingJson["attributes"]