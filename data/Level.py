class Level:
    def __init__(self, game, ran=False):
        self.game = game
        self.ran = ran

    def start(self):
        pass
    
    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass