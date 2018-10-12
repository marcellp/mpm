from enum import Enum

class Item(object):

    def __init__(self,name,desc,weight,effect):
        self.name = name
        self.desc = desc
        self.weight = weight
        self.effect = effect

    ### add types that effect what item does


class type(Enum):
    food = 1


