from Data.Level import Level
from Data.Objects.lit_obj import LitObject

import pygame

background_color = ()

class Level1(Level):
    def update(self):
        # Example condition to switch to level 2

        
        if False:
            from Data.lvl2 import Level2
            self.game.current_level = Level2(self.game)

    diamond = None
    def start(self):
        print("innit start function")
        self.diamond = LitObject(
            [0, 0],
            pygame.image.load('assets/test_texture.png').convert_alpha(),
            [
                [(137, 0), (165, 70), (305, 70), (332, 0)],  # Top
                [(0, 137), (0, 332), (70, 305), (70, 165)],  # Left
                [(137, 472), (165, 400), (305, 400), (332, 472)],  # Bottom
                [(400, 165), (400, 305), (470, 332), (470, 137)],  # Right

                [(165, 70), (137, 0), (0, 137), (70, 165)],  # Top-left bevel
                [(305, 70), (332, 0), (470, 137), (400, 165)],  # Top-right bevel
                [(137, 472), (165, 400), (70, 305), (0, 332)],  # Bottom-left bevel
                [(305, 400), (332, 472), (470, 332), (400, 305)],  # Bottom-right bevel

                [(236, 236), (305, 70), (165, 70)],  # Inner top
                [(236, 236), (70, 165), (70, 305)],  # Inner left
                [(236, 236), (165, 400), (305, 400)],  # Inner bottom
                [(236, 236), (400, 165), (400, 305)],  # Inner right

                [(236, 236), (70, 165), (165, 70)],  # Bevel top-left
                [(236, 236), (305, 70), (400, 165)],  # Bevel top-right
                [(236, 236), (70, 305), (165, 400)],  # Bevel bottom-left
                [(236, 236), (305, 400), (400, 305)],  # Bevel bottom-right
            ])
        
        self.diamond.set_light_position([(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, 0)])

        return super().start()
    
    def draw(self, screen):
        print("Drawn frame")
        screen.fill((255, 255, 255), rect=None, special_flags=0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.diamond.position[1] -= 5
        if keys[pygame.K_s]:
            self.diamond.position[1] += 5
        if keys[pygame.K_a]:
            self.diamond.position[0] -= 5
        if keys[pygame.K_d]:
            self.diamond.position[0] += 5

        if self.diamond != None:
            print("drawn diamond")
            self.diamond.set_light_position([(0, 0, 222, 114, 52, 500),
                                             (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, 0, 500)])

            screen.blit(self.diamond.get_surface(), (self.diamond.position))