from Item import *
from math import floor, ceil
from IOStream import io

class Entity(object):
	MAX_SPECIAL_POINTS = 40
	DEFAULT_BODY_PARTS = ("head", "torso","left leg", "right leg", "right hand","left hand")
	DEFAULT_SKILLS = {  "barter": "charisma", "lockpick": "perception", "medicine": "intelligence",
						"meelee": "strength", "sneak": "agility", "speech": "charisma", "unarmed": "endurance"}

	def __init__(self, level = 1, local_player = False, body_parts = None, name = None):
		self.alive = True

		self.level = level
		self.xp = 0

		self.inventory = []
		self.actions = {}

		self.at = None
		
		self.local_player = local_player

		if name:
			self.name = name
		else:
			self.name = "living being"

		if body_parts:
			self.body_parts = body_parts
		else:
			self.body_parts = Entity.DEFAULT_BODY_PARTS

		self.equipped = {x:None for x in self.body_parts}
		self.crippled = {x:False for x in self.body_parts}

		#self.use_context = {Item_type.food:self.eat,Item_type.wearable:self.equip}

	def add_item(self, item, amount = 1):
		"""adds the item to the players inventory if it is an item"""

		if not isinstance(item,Item):
			return False

		amount_updated = False

		for i, slot in enumerate(self.inventory):
			slot_item = slot[0]
			slot_amount = slot[1]

			if item != slot_item:
				continue

			self.inventory[i][1] += amount

			amount_updated = True
			break

		if not amount_updated:
			self.inventory.append([item, amount])

		return True

	def remove_item(self, index):
		"""returns the item if the player has it
		else returns none"""

		try:
			item = self.inventory[index]
		except IndexError:
			return None

		item_obj = item[0]
		amount = item[1]

		if amount == 1:
			del self.inventory[index]
			return item_obj
		else:
			self.inventory[index][1] -= 1
			return copy.deepcopy(item_obj)

	def get_hp(self):
		raise NameError('HP not implemented for this class.')

	def get_stat(self, key):
		try:
			return self.stats.get(key)
		except KeyError:
			return None

	def set_stat(self, key, amount):
		try:
			self.stats[key] = amount
			return True
		except KeyError:
			return None

	def get_skill(self, skill):
		skill = skill.lower()

		if skill not in Entity.DEFAULT_SKILLS:
			raise ValueError('invalid skill specified')

		base_attr = self.get_stat(Entity.DEFAULT_SKILLS[skill])
		base_value = 2 + (base_attr * 2) + ceil(self.get_stat("luck") / 2)

		return base_value + self.skills[skill]

	def set_skill(self, skill, value):
		skill = skill.lower()

		if skill not in Entity.DEFAULT_SKILLS:
			raise ValueError('invalid skill specified')

		self.skills[skill] = value
		return True

	def add_xp(self, increase = 0):
		self.xp += increase
		while self.xp >= self.xp_to_level_up():
			self.xp -= self.xp_to_level_up()
			self.level_up()

	def level_up(self):
		self.level += 1

		if self.local_player:
			io.out("You are now level {}!".format(self.level))

	def xp_to_level_up(self):
		return 50+150*self.level

	def __str__(self):
		return self.name

	#def change hp/kill stuff

	#boilerplate
	def print_stats(self):
		"""print the state of the entity"""
		print(self.stats)

	def save(self):
		"""save the the current state of the object to file as json"""
		pass

	def load(self,file_name=""):
		"""load the object from json"""
		pass

class Human(Entity):
	def __init__(self, name, sex, local_player = False, stats = None,skills=None):

		if not stats:
			self.stats  =   {"level":1,"strength":5,"perception":5,"endurance":5,
							"charisma":5,"intelligence":5,"agility":5,"luck":5}
		else:
			self.stats = stats


		if not skills:
			self.skills = {x:0 for x in Entity.DEFAULT_SKILLS.keys()}
		else:
			self.skills = skills

		Entity.__init__(self, local_player = local_player)

		self.name = name
		self.sex = sex

	def get_hp(self):
		return 90 + (self.get_stat("endurance") * 20) + (self.level * 10)

	def get_ap(self):
		return 5 + floor(self.get_stat("agility") / 2)

	def show_inventory(self):
		if not self.local_player:
			return

		io.out('')
		io.out('YOU ARE CARRYING...')
		io.out('Use `inspect inventory [id]` to inspect an item in your inventory.')
		io.out('Use `use [id]` to use an item in your inventory.')

		if not self.inventory:
			io.out('You do not seem to be carrying anything.')

		for i, item in enumerate(self.inventory):
			if item:
				item_obj = item[0]
				item_amount = item[1]

				io.out('[{}]\t{}\t\tAMT: {}\t\tWGH: {}'.format(i, item_obj, item_amount, item_obj.weight))

		io.out('')
		io.out('YOU ARE WEARING...')
		for bodypart, item in self.equipped.items():
			if not item:
				item = "Nothing"

			io.out('{:<16}{}'.format(bodypart.upper(), item))
		io.out('')

	def move_to(self, room):
		curr_room = self.at

		try:
			curr_room.entities.remove(self)
		except:
			pass

		self.at = room
		room.entities.append(self)

	def show_pep(self):
		io.out('')
		io.out('PEP-BOY Mk. 8 Copyright 2018 mpm, inc. All rights reserved.')
		io.out('')

		io.out('Name:\t{}\t\tSex:\t{}'.format(self.name, self.sex))
		io.out('')

		io.out('STATISTICS')
		io.out('LVL:\t{}\tHP:\t{}\tAP:\t{}'.format(self.level, self.get_hp(), self.get_ap()))
		io.out('STR:\t{}\tPER:\t{}\tEND:\t{}'.format(self.get_stat("strength"), self.get_stat("perception"), self.get_stat("endurance")))
		io.out('CHA:\t{}\tINT:\t{}\tAGL:\t{}'.format(self.get_stat("charisma"), self.get_stat("intelligence"), self.get_stat("agility")))
		io.out('LCK:\t{}'.format(self.get_stat("luck")))
		io.out('')

		io.out('SKILLS')
		for skill in self.skills.keys():
			io.out('{:<16}{}'.format(skill.capitalize(), self.get_skill(skill)))
		io.out('')

		io.out('BODY STATE')
		for bodypart, crippled in self.crippled.items():

			if crippled:
				crippled = "CRIPPLED"
			else:
				crippled = "INTACT"

			io.out('{:<16}{}'.format(bodypart.capitalize(), crippled))
		io.out('')


class Creature(Entity):
	def __init__(self, hp, ap, name = None):
		Entity.__init__(self, name = name)
		self.hp = hp
		self.ap = ap
		pass

	def get_hp(self):
		return self.hp

	def get_ap(self):
		return self.ap