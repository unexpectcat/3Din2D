import pygame
from Data.lvl1 import Level1

pygame.init()





class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = Level1(self)

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_level.handle_events(events)
            self.current_level.update()
            self.current_level.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
