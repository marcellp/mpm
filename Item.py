from enum import Enum

class Item(object):

    def __init__(self,name,desc,weight,effect,inventory=None):
        self.name = name
        self.desc = desc
        self.weight = weight
        self.effect = effect
        self.item_code = item_code
        self.inventory = inventory

    ### add types that effect what item does


class Item_type(Enum):
    food_hp = 1
    food_ap = 2
    wearable= \
        3


