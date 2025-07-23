from Data.Level import Level

background_color = ()

class Level1(Level):
    def update(self):
        # Example condition to switch to level 2

        
        if True:
            from Data.lvl2 import Level2
            self.game.current_level = Level2(self.game)

    def draw(self, screen):

        screen.fill((255, 0, 0), rect=None, special_flags=0)