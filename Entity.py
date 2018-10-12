class Entity:

    MAX_SPECIAL_POINTS = 40

    def __init__(self, sex, stats = None):
        self.inventory = []
        self.actions = {}
        self.sex = None
        self.at = None

        if stats:
            self.stats  ={"level":1,"strength":5,"perception":5,"endurance":5,
                          "charisma":5,"intelligence":5,"agility":5,"luck":5}
        else:
            self.stats = {}

    def print_stats(self):
        """print the state of the entity"""
        print(self.stats)

    def save(self):
        """save the the current state of the object to file as json"""
        pass

    def load(self,file_name=""):
        """load the object from json"""
        pass



