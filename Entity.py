class Entity:

    def __init__(self,actions={},stats={},inventory=[]):

        self.inventory = []
        self.actions = actions
        if stats == {}:
            self.stats  ={"Level":0,"Strength":0,"Perception":0,"Endurance":0,
                          "Charisma":0,"Intelligence":0,"Agility":0,"Luck":0}
        else:
            self.stats = stats

        if actions == {}:
            self.actions = {}


    def print_stats(self):
        """print the state of the entity"""
        print(self.stats)

    def save(self):
        """save the the current state of the object to file as json"""
        pass

    def load(self,file_name=""):
        """load the object from json"""
        pass



