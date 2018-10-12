import Item
from math import floor

class Entity(object):

    MAX_SPECIAL_POINTS = 40

    def __init__(self,stats,level=1):
        self.attributes = {}
        self.level = level
        self.inventory = []
        self.actions = {}
        self.at = None
        self.stats = stats
        self.update_attributes()


    def update_attributes(self):
        health = 90 + (self.stats["endurence"] * 20) + (self.level * 10)
        stamina = 5 + floor(self.stats["agility"] / 2)

        self.attributes["health"],self.attributes["stamina"] = health,stamina

    def add_item(self,item):

        if isinstance(item,Item):
            self.inventory.append(item)
        else:
            print("that wasnt an item")

    def drop_item(self,item_name):
        """returns the item if the player has it
        else returns none"""

        for item in self.inventory:
            if item.name == item_name:
                return item

        return None

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


