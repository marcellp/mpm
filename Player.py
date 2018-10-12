from Entity import Entity
class Player(Entity):

    def __init__(self,stats,sex):
        Entity.__init__(self,stats)
        self.sex = sex
        self.xp = 0

    def add_xp(self,increase=0):
        self.xp += increase
        while self.xp >= self.xp_to_level_up():
            self.xp -= self.xp_to_level_up()
            self.level_up()


    def level_up(self):
        self.level += 1
        self.update_attributes()
        print("You have are now level ",self.level,
              "\nHealth: ",self.health," Stamina:", self.stamina)

    def xp_to_level_up(self):
        return 50+150*self.level

    ##continue test on player, coalesce with entity
test = Player({"endurence":0,"agility":0},"thing")
test.add_xp(1000)









