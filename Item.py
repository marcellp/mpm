from enum import Enum

class Item(object):

    def __init__(self,name,desc,weight,effect,item_code=None,inventory=None):
        self.name = name
        self.desc = desc
        self.weight = weight
        self.effect = effect
        self.item_code = item_code
        self.inventory = inventory

    ### add types that effect what item does

    def __str__(self):
    	return self.name

class Item_type(Enum):
    food_hp = 1
    food_ap = 2
    wearable= \
        3
