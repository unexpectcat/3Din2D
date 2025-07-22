from Data.Level import Level

class Level1(Level):
    def update(self):
        # Example condition to switch to level 2
        if self.game.player_reached_exit:
            from Data.lvl2 import Level2
            self.game.current_level = Level2(self.game)