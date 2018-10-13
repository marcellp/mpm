from Item import *
from math import floor
from IOStream import io

class Entity(object):
    MAX_SPECIAL_POINTS = 40
    DEFAULT_BODY_PARTS = ("head", "chest", "legs", "shoes")

    def __init__(self, stats, level = 1, local_player = False, body_parts = None):
        self.alive = True

        self.attributes = {}
        self.stats = stats

        self.level = level
        self.xp = 0

        self.inventory = []
        self.actions = {}

        self.at = None
        
        self.local_player = local_player

        self.update_attributes()

        if body_parts:
            self.body_parts = body_parts
        else:
            self.body_parts = Entity.DEFAULT_BODY_PARTS

        self.clothes = {x:None for x in self.body_parts}

        #self.use_context = {Item_type.food:self.eat,Item_type.wearable:self.equip}

    def use_item(self,index):
        item = self.inventory.pop(index)

    def update_attributes(self):
        health = 90 + (self.stats["endurance"] * 20) + (self.level * 10)
        stamina = 5 + floor(self.stats["agility"] / 2)

        self.attributes["health"],self.attributes["stamina"] = health,stamina

    def add_item(self,item):
        """adds the item to the players inventory if it is an item"""

        if isinstance(item,Item):
            self.inventory.append(item)
        else:
            print("that wasnt an item")

    def get_stats(self,key):
        try:
            return self.attributes.get(key)
        except KeyError:
            return None

    def drop_item(self,item_name):
        """returns the item if the player has it
        else returns none"""

        for i,item in enumerate(self.inventory):
            if item.name == item_name:
                return self.inventory.pop(i)

        return None

    def change_attributes(self,key,amount):
        """cahnge attributes of an alive entity, invalid operation otherwise"""

        if self.attributes["health"] <= 0:
            print("invalid operation in change attributes")
            return None
        else:
            try:
                self.attributes[key] += amount
            except KeyError:
                print("couldnt change attributes")

    def add_xp(self, increase = 0):
        self.xp += increase
        while self.xp >= self.xp_to_level_up():
            self.xp -= self.xp_to_level_up()
            self.level_up()

    def level_up(self):
        self.level += 1
        self.update_attributes()

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
            self.stats  =   {"level":0,"strength":0,"perception":0,"endurance":0,
                            "charisma":0,"intelligence":0,"agility":0,"luck":0}
        else:
            self.stats = stats

        Entity.__init__(self, stats = self.stats, local_player = local_player)

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

##continue test on player, coalesce with entity
#test = Player({"endurence":0,"agility":0},"thing")
#test.add_xp(1000)