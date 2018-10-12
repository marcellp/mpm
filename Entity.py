class Entity:

    def __init__(self,actions={},state={}):

        self.actions = actions
        self.state = state

    def print_stats(self):
        """print the state of the entity"""
        print(self.state)

    def save(self):
        """save the the current state of the object to file as json"""
        pass

    def load(self,file_name=""):
        """load the object from json"""
        pass



