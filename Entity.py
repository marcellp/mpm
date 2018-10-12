class Entity:

    def __init__(self,actions={},stats={},inventory=[]):

        self.inventory = []
        self.actions = actions
        if stats == {}:
            self.stats  ={"level":0,"strength":0,"perception":0,"endurance":0,
                          "charisma":0,"intelligence":0,"agility":0,"luck":0}
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



