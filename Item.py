from enum import Enum

class Item(object):

    def __init__(self, name, desc = None, value = 0, weight = 0, container = False):
        self.name = name

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