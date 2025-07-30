import pygame
from Data.lvl1 import Level1

pygame.init()





class Game:
    def __init__(self):
        pygame.init()
        infoObject = pygame.display.Info()
        app_window_relative_size = (1, 1)

        x = int(infoObject.current_w * app_window_relative_size[0])
        y = int(infoObject.current_h * app_window_relative_size[1])
        self.screen = pygame.display.set_mode((x, y))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = Level1(self)

    def run(self):
        while self.running:

            if not self.current_level.ran:
                self.current_level.start()
                self.current_level.ran = True
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_level.handle_events(events)
            self.current_level.update()
            self.current_level.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
