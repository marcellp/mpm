from Item import *
from math import floor, ceil
import random
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

		self.hp = None

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
		self.part_damage = {x:0 for x in self.body_parts}

		#self.use_context = {Item_type.food:self.eat,Item_type.wearable:self.equip}

	def get_equipped_weapon(self):
		left_hand = self.equipped["left hand"]
		right_hand = self.equipped["right hand"]

		if not isinstance(left_hand,Weapon):
			left_hand = None
		if not isinstance(right_hand,Weapon):
			right_hand = None

		return right_hand,left_hand

	def attack_send(self, victim):
		pass

	def attack_receive(self, attacker, body_part, damage):
		if self.hp <= 0:
			return

		if self.local_player:
			io.out('')
			io.out('{} has dealt {} damage to you on your {}.'.format(attacker, damage, body_part))

		clothes = self.equipped[body_part]

		# Reduce damage by DR percentage.
		if isinstance(clothes, Clothing):
			damage = ceil(damage * (100 - clothes.attributes["dr"]) * 0.01)
			if self.local_player:
				io.out('Thanks to your {}, this has been reduced to {}.'.format(damage))

		self.part_damage[body_part] += damage

		if damage > self.get_hp() and (body_part == 'left hand' or body_part == 'right hand'):
			self.equipped[body_part] = None

			if self.local_player:
				io.out('Your hand is crippled. Anything that you held in there has been unequipped.')

		self.hp -= damage
		self.hp = max(self.hp, 0)

		if self.hp == 0 and self.local_player:
			io.out('You have died.')
			return

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

		for bodypart, equipped in self.equipped.items():
			if equipped == item_obj:
				self.equipped[bodypart] = None
				break

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
			stat = self.stats.get(key)
		except KeyError:
			return None

		if key == "perception" and self.part_damage["head"] > self.get_hp():
			return max(stat - 4, 1)

		if key == "endurance" and self.part_damage["torso"] > 100:
			return max(stat - 4, 1)

		return stat

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
		if self.hp == None:
			self.hp = 90 + (self.get_stat("endurance") * 20) + (self.level * 10)

		return self.hp

	def get_ap(self):
		return 65 + (2 * self.get_stat("agility"))

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

		io.out('BODY PART DAMAGE')
		for bodypart, part_damage in self.part_damage.items():
			io.out('{:<16}{:<8}'.format(bodypart.capitalize(), part_damage))
		io.out('')

	def attack_send(self, victim):
		if not self.local_player:
			return

		if victim.get_hp() <= 0:
			io.out("You can't fight {}, they are dead.".format(victim))
			return False

		curr_ap = self.get_ap()
		io.out("YOU ARE NOW FIGHTING {}".format(str(victim).upper()))

		while True:

			if self.get_hp() <= 0:
				return

			io.out('')
			io.out('ROUND')
			io.out('Opponent has {} HP. You have {} HP. You have {} action points to use in total.'.format(victim.get_hp(), self.get_hp(), curr_ap))

			weapons = self.get_equipped_weapon()
			unarmed_damage = damage = ceil(self.get_skill("unarmed")/20 + 0.5)
			damage = None

			for i, weapon in enumerate(weapons):
				if not weapon:
					continue

				io.out("[{}] {} (DPA: {}, CRIT damage: {}, AP cost: {}".format(i, weapon, weapon.attributes["dpa"], weapon.attributes["crit_damage"], weapon.attributes["ap_cost"]))

			io.out('Choose a weapon to attack with or type in u to attack unarmed.')

			while True:
				attack_weapon = io.send_in('! ')

				if attack_weapon == "u":
					damage = unarmed_damage
					io.out("Fair enough, use your fists. You will be dealing {} damage.".format(damage))
					break

				try:
					attack_weapon = weapons[int(attack_weapon)]
				except:
					io.out('Invalid weapon. Try again.')
					continue

				if attack_weapon.attributes["ap_cost"] > curr_ap:
					io.out('You do not have enough action points for this action.')
					continue

				curr_ap -= attack_weapon.attributes["ap_cost"]
				damage = attack_weapon.attributes["dpa"]		
				io.out('You are attacking with {}, base damage of {} dealt.'.format(attack_weapon, damage))

				crit_chance = ((self.get_stat("luck") * 0.01) * attack_weapon.attributes["crit_chance"]) + 0.15

				if random.random() < crit_chance:
					damage += attack_weapon.attributes["crit_damage"]
					io.out("This is a critical hit! You are now dishing out {} damage points.".format(damage))

				break

			body_part = random.choice(victim.body_parts)
			io.out('You have struck the {} of the {}.'.format(body_part, victim))

			victim.attack_receive(self, body_part, damage)

			if victim.get_hp() <= 0:
				io.out('You killed {}.'.format(victim))
				return

			victim.attack_send(self)


class Creature(Entity):
	def __init__(self, hp, meelee, level = 1, body_parts = None, name = None):
		Entity.__init__(self, level = level, body_parts = body_parts, name = name)
		self.hp = hp
		self.meelee = meelee
		pass

	def get_hp(self):
		return self.hp

	def get_ap(self):
		return self.ap	

	def attack_send(self, victim):
		damage = self.meelee
		max_dpa = 0

		for weapon in self.equipped:
			if not isinstance(weapon, Weapon):
				continue

			if weapon.attributes["dpa"] > max_dpa:
				max_dpa = weapon.attributes["dpa"]

		damage += max_dpa

		body_part = random.choice(victim.body_parts)
		victim.attack_receive(self, body_part, damage)