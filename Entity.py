from Item import *
from math import floor, ceil
from IOStream import io

class Entity(object):
    MAX_SPECIAL_POINTS = 40
    DEFAULT_BODY_PARTS = ("head", "chest", "legs", "shoes")
    DEFAULT_SKILLS = {  "barter": "charisma", "lockpick": "perception", "medicine": "intelligence",
                        "meelee": "strength", "sneak": "agility", "speech": "charisma", "unarmed": "endurance"}

    def __init__(self, stats = None, level = 1, local_player = False, body_parts = None):
        self.alive = True

        self.attributes = {}

        if stats:
            self.stats = stats
        else:
            self.stats  =   {"level":1,"strength":0,"perception":0,"endurance":0,
                            "charisma":0,"intelligence":0,"agility":0,"luck":0}

        self.skills = {x : 0 for x in Entity.DEFAULT_SKILLS.keys()}

        self.level = level
        self.xp = 0

        self.inventory = []
        self.actions = {}

        self.at = None
        
        self.local_player = local_player

        if body_parts:
            self.body_parts = body_parts
        else:
            self.body_parts = Entity.DEFAULT_BODY_PARTS

        self.clothes = {x:None for x in self.body_parts}

        #self.use_context = {Item_type.food:self.eat,Item_type.wearable:self.equip}

    def use_item(self,index):
        item = self.inventory.pop(index)

    def get_hp(self):
        return 90 + (self.get_stat("endurance") * 20) + (self.level * 10)

    def get_stamina(self):
        return 5 + floor(self.get_stat("agility") / 2)

    def add_item(self,item):
        """adds the item to the players inventory if it is an item"""

        if isinstance(item,Item):
            self.inventory.append(item)
            return True
        else:
            return False

    def remove_item(self, index):
        """returns the item if the player has it
        else returns none"""

        try:
            item = self.inventory[itemid]
        except IndexError:
            return None

        self.inventory[itemid] = None
        return item

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
    def __init__(self, name, sex, local_player = False, stats = None):

        if not stats:
            self.stats  =   {"level":1,"strength":5,"perception":5,"endurance":5,
                            "charisma":5,"intelligence":5,"agility":5,"luck":5}
        else:
            self.stats = stats

        Entity.__init__(self, stats = self.stats, local_player = local_player)

        self.name = name
        self.sex = sex

    def show_inventory(self):
        if not self.local_player:
            return

        io.out('')
        io.out('YOUR INVENTORY')

        if not self.inventory:
            io.out('You do not seem to be carrying anything.')

        for (i, item) in zip(range(1, len(self.inventory) + 1), self.inventory):
            if item:
                io.out('[{}]\t{}\t\tWGH: {}'.format(i, item, item.weight))

        io.out('')

    def show_pep(self):
        io.out('')
        io.out('PEP-BOY 2000. Copyright 2018 mpm, inc. All rights reserved.')
        io.out('')

        io.out('Name:\t{}\t\tSex:\t{}'.format(self.name, self.sex))
        io.out('')

        io.out('STATISTICS')
        io.out('LVL:\t{}\tHP:\t{}\tSTA:\t{}'.format(self.level, self.get_hp(), self.get_stamina()))
        io.out('STR:\t{}\tPER:\t{}\tEND:\t{}'.format(self.get_stat("strength"), self.get_stat("perception"), self.get_stat("endurance")))
        io.out('CHA:\t{}\tINT:\t{}\tAGL:\t{}'.format(self.get_stat("charisma"), self.get_stat("intelligence"), self.get_stat("agility")))
        io.out('LCK:\t{}'.format(self.get_stat("luck")))
        io.out('')

        io.out('SKILLS')
        for skill in self.skills.keys():
            io.out('{:<16}{}'.format(skill.upper(), self.get_skill(skill)))


##continue test on player, coalesce with entity
#test = Player({"endurence":0,"agility":0},"thing")
#test.add_xp(1000)