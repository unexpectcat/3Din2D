import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import lvl_manager
import pygame.surfarray
import numpy as np
import pygame

x_center = int(lvl_manager.x / 2)
y_center = int(lvl_manager.y / 2)

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

# Generate gradient texture
width, height = 255, 255
texture = pygame.Surface((width, height))
arr = pygame.surfarray.pixels3d(texture)
for x in range(width):
    for y in range(height):
        r = x
        g = 255 - y
        b = y
        arr[x, y] = [r, g, b]
del arr

# Create 4 cubes
cubes = [
    Cube(x_center - 150, y_center - 150, (160, 0, 30)),
    Cube(x_center + 150, y_center - 150, (30, 160, 0)),
    Cube(x_center - 250, y_center + 150, (0, 30, 160)),
    Cube(x_center + 250, y_center + 150, (160, 160, 0)),
]

def pickColor(mouse_x, mouse_y):
    if 10 <= mouse_x < 275 and 10 <= mouse_y < 275:
        color = texture.get_at((mouse_x - 20, mouse_y - 20))[:3]
        for cube in cubes:
            cube.set_color(color)  # All cubes pick the same color — or customize by proximity

def tick():
    keys = pygame.key.get_pressed()
    dx = dy = 0
    speed = 5
    if keys[pygame.K_w]: dy -= speed
    if keys[pygame.K_s]: dy += speed
    if keys[pygame.K_a]: dx -= speed
    if keys[pygame.K_d]: dx += speed

    pygame.draw.rect(lvl_manager.screen, (127, 140, 170), (0, 0, 295, lvl_manager.y))
    pygame.draw.rect(lvl_manager.screen, (234, 239, 239), (10, 10, 275, 275))
    lvl_manager.screen.blit(texture, (20, 20))  # Draw the texture

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pickColor(mouse_x, mouse_y)

    for cube in cubes:
        cube.move(dx, dy)

        # Compute color shading for each side
        top_side = tuple(max(0, min(160, int((100 - mouse_y + cube.y) / 3) + 100)) for _ in (0, 1, 2))
        top_side = tuple(min(cube.get_color()[i], top_side[i]) for i in range(3))

        left_side = tuple(max(0, min(160, int((100 - mouse_x + cube.x) / 3) + 100)) for _ in (0, 1, 2))
        left_side = tuple(min(cube.get_color()[i], left_side[i]) for i in range(3))

        right_side = tuple(max(0, min(160, int((100 + mouse_x - cube.x) / 3) + 100)) for _ in (0, 1, 2))
        right_side = tuple(min(cube.get_color()[i], right_side[i]) for i in range(3))

        # Draw cube
        pygame.draw.polygon(lvl_manager.screen, top_side, cube.get_polygons()[0], 0)
        pygame.draw.polygon(lvl_manager.screen, left_side, cube.get_polygons()[1], 0)
        pygame.draw.polygon(lvl_manager.screen, right_side, cube.get_polygons()[2], 0)

lvl_manager.LevelManagerObject.OnTick = tick
lvl_manager.run()
