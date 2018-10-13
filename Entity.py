import Item
from math import floor

class Entity(object):

    MAX_SPECIAL_POINTS = 40
    DEFAULT_BODY_PARTS = ("head", "chest", "legs", "shoes")

    def __init__(self, stats, level=1, body_parts = None):
        self.alive = True
        self.attributes = {}
        self.level = level
        self.inventory = []
        self.actions = {}
        self.at = None
        self.stats = stats
        self.update_attributes()

        if body_parts:
            self.body_parts = body_parts
        else:
            self.body_parts = Entity.DEFAULT_BODY_PARTS

        self.clothes = {x:None for x in self.body_parts}

        #self.use_context = {type.food}

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
            print("key was not found for attributes")
            return None

    def drop_item(self,item_name):
        """returns the item if the player has it
        else returns none"""

        for item in self.inventory:
            if item.name == item_name:
                return item

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