import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import lvl_manager
import pygame.surfarray
import numpy as np
import pygame

x = int(lvl_manager.x / 2)
y = int(lvl_manager.y / 2)




class Cube:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_color(self):
        return self.color
    
    def set_color(self, color):
        self.color = color

    def get_polygons(self):
        x, y = self.x, self.y
        return [
            [(x, y - 25), (x - 50, y), (x, y + 25), (x + 50, y), (x, y - 25)],
            [(x, y + 25), (x - 50, y), (x - 50, y + 50), (x, y + 75)],
            [(x + 50, y), (x, y + 25), (x, y + 75), (x + 50, y + 50)]
        ]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

width = 255
height = 255
texture = pygame.Surface((width, height))
arr = pygame.surfarray.pixels3d(texture)
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Arial Black', 24)    


for x in range(width):
    for y in range(height):
        r = x
        g = 255 - y
        b = y
        arr[x, y] = [r, g, b]  # RGB
del arr 



cube = Cube(lvl_manager.x / 2, lvl_manager.y / 2, (160, 0, 30))
def pickColor(mouse_x, mouse_y):
    if 10 <= mouse_x < 275 and 10 <= mouse_y < 275:
        cube.set_color(texture.get_at((mouse_x, mouse_y))[:3])

def to_lvl_2(mouse_x, mouse_y):
    if 10 <= mouse_x < 285 and 355 <= mouse_y < 415:
        os.system("python lvl2/main.py")        
def tick():

    keys = pygame.key.get_pressed()
    dx = dy = 0
    speed = 5
    if keys[pygame.K_w]:
        dy -= speed
    if keys[pygame.K_s]:
        dy += speed
    if keys[pygame.K_a]:
        dx -= speed
    if keys[pygame.K_d]:
        dx += speed

    pygame.draw.rect(lvl_manager.screen, (127, 140, 170), (0, 0, 295, lvl_manager.y))
    pygame.draw.rect(lvl_manager.screen, (234, 239, 239), (10, 70, 275, 275))
    lvl_manager.screen.blit(texture, (20, 80))  # Draw the texture at top-left

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pickColor(mouse_x, mouse_y)
            to_lvl_2(mouse_x, mouse_y)

    text_surface = my_font.render('Change cube color', False, (0, 0, 0))

    pygame.draw.rect(lvl_manager.screen, (184, 207, 206), (10, 10, 275, 60))
    lvl_manager.screen.blit(text_surface, (16, 20))

    
    text_surface = my_font.render('Cubes Stress-Test', False, (0, 0, 0))
    pygame.draw.rect(lvl_manager.screen, (184, 207, 206), (10, 355, 275, 60))
    lvl_manager.screen.blit(text_surface, (16, 365))
    cube.move(dx, dy)


    print(f"Mouse position: {mouse_x}, {mouse_y}")
    

    top_side = tuple(max(0, min(160, int((100 - mouse_y + cube.y) / 3) + 100)) for _ in (0, 1, 2))
    top_side = tuple(min(cube.get_color()[i], top_side[i]) for i in range(3))

    left_side = tuple(max(0, min(160, int((100 - mouse_x + cube.x) / 3) + 100)) for _ in (0, 1, 2))
    left_side = tuple(min(cube.get_color()[i], left_side[i]) for i in range(3))

    right_side = tuple(max(0, min(160, int((100 + mouse_x - cube.x) / 3) + 100)) for _ in (0, 1, 2))
    right_side = tuple(min(cube.get_color()[i], right_side[i]) for i in range(3))



    pygame.draw.polygon(lvl_manager.screen, top_side, cube.get_polygons()[0], 0)
    pygame.draw.polygon(lvl_manager.screen, left_side, cube.get_polygons()[1], 0)
    pygame.draw.polygon(lvl_manager.screen, right_side, cube.get_polygons()[2], 0)



lvl_manager.LevelManagerObject.OnTick = tick
lvl_manager.run()

print('hello')