import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import lvl_manager
import pygame.surfarray
import numpy as np
import pygame
import collections


x = int(lvl_manager.x / 2)
y = int(lvl_manager.y / 2)

class pseudo_3D_polygon:
    def __init__(self, x, y, color, normal_map):
        self.x = x,
        self.y = y
        self.color = color
        self.normal_map = normal_map

    def get_color(self):
        return self.color
    def get_polygons(self):
        pass

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

def load_sprites():
    # Load the sprite sheet and convert for fast blitting
    sprite_sheet = pygame.image.load("assets/asset.png").convert()

    # Get full size
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // 3  # since there are 3 images
    frame_height = sheet_height

    # Create a list for individual frames
    frames = []

    for i in range(3):
        # Create a new surface with the same size as one frame, and with alpha support
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

        # Blit the corresponding part of the sprite sheet onto the new surface
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))

        # Replace black pixels with transparent
        frame.set_colorkey((0, 0, 0))  # Removes black

        frames.append(frame)
    
    return frames

def rounded_color(color, precision=16):
    """Round RGB color to the nearest multiple of `precision`"""
    return tuple((c // precision) * precision for c in color)


def flood_fill(texture, visited, x, y, target_color):
    queue = collections.deque()
    queue.append((x, y))
    region = []

    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) in visited:
            continue
        if not (0 <= cx < texture.get_width() and 0 <= cy < texture.get_height()):
            continue

        current_color = texture.get_at((cx, cy))[:3]
        if rounded_color(current_color) != target_color:
            continue

        visited.add((cx, cy))
        region.append((cx, cy))

        # Add 4-connected neighbors
        queue.extend([
            (cx + 1, cy),
            (cx - 1, cy),
            (cx, cy + 1),
            (cx, cy - 1)
        ])

    return region

def generate_shape(texture):
    # Load the sprite sheet and convert for fast blitting
    sprite_sheet = pygame.image.load("assets/asset.png").convert()

    # Get full size
    sheet_width, sheet_height = texture.get_size()
    frame_width = sheet_width
    frame_height = sheet_height

    # Step 1: build rounded color set
    colors = set()
    color_map = {}  # map rounded color -> list of positions

    for x in range(sheet_width):
        for y in range(sheet_height):
            pixel = texture.get_at((x, y))[:3]
            if pixel == (0, 0, 0):
                continue
            rc = rounded_color(pixel, precision=16)
            colors.add(rc)
            color_map.setdefault(rc, []).append((x, y))

    # Step 2: draw outlines on the texture copy
    highlight_surface = texture.copy()
    for color_key, positions in color_map.items():
        for (x, y) in positions:
            pygame.draw.rect(highlight_surface, (255, 0, 0), (x, y, 1, 1), 1)  # red outline

    # Step 3: blit to screen (in your draw loop)
    

    return(highlight_surface)
    

    print(colors)
        # # Create a new surface with the same size as one frame, and with alpha support
        # frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

        # # Blit the corresponding part of the sprite sheet onto the new surface
        # frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))



def pickColor(mouse_x, mouse_y):
    if 10 <= mouse_x < 275 and 10 <= mouse_y < 275:
        pass#cube.set_color(texture.get_at((mouse_x, mouse_y))[:3])




sprites = load_sprites() 
generate_shape(sprites[2])      
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

    lvl_manager.screen.blit(sprites[2], (int(x * 2) + 145, y))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    

    


    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pickColor(mouse_x, mouse_y)
            

    text_surface = my_font.render('Change asset color', False, (0, 0, 0))

    pygame.draw.rect(lvl_manager.screen, (184, 207, 206), (10, 10, 275, 60))
    lvl_manager.screen.blit(text_surface, (16, 20))

    #cube.move(dx, dy)

    visited = set() 
    highlight_surface = texture.copy()

    sheet_width, sheet_height = texture.get_size()
    frame_width = sheet_width
    frame_height = sheet_height

    for x in range(sheet_width):
        for y in range(sheet_height):
            if (x, y) in visited:
                continue
            pixel = texture.get_at((x, y))[:3]
            if pixel == (0, 0, 0):  # skip transparent
                continue
            rcolor = rounded_color(pixel)
            region = flood_fill(sprites[2], visited, x, y, rcolor)

            if not region:
                continue

            # Draw region outline
            mask = pygame.Mask((sheet_width, sheet_height))
            for px, py in region:
                mask.set_at((px, py), 1)

            outline = mask.outline()
            pygame.draw.polygon(highlight_surface, (255, 255, 255), outline)  # fill white
            pygame.draw.polygon(highlight_surface, (255, 0, 0), outline, 1)   # outline red

    #print(f"Mouse position: {mouse_x}, {mouse_y}")
    

    # top_side = tuple(max(0, min(160, int((100 - mouse_y + cube.y) / 3) + 100)) for _ in (0, 1, 2))
    # top_side = tuple(min(cube.get_color()[i], top_side[i]) for i in range(3))

    # left_side = tuple(max(0, min(160, int((100 - mouse_x + cube.x) / 3) + 100)) for _ in (0, 1, 2))
    # left_side = tuple(min(cube.get_color()[i], left_side[i]) for i in range(3))

    # right_side = tuple(max(0, min(160, int((100 + mouse_x - cube.x) / 3) + 100)) for _ in (0, 1, 2))
    # right_side = tuple(min(cube.get_color()[i], right_side[i]) for i in range(3))



    # pygame.draw.polygon(lvl_manager.screen, top_side, cube.get_polygons()[0], 0)
    # pygame.draw.polygon(lvl_manager.screen, left_side, cube.get_polygons()[1], 0)
    # pygame.draw.polygon(lvl_manager.screen, right_side, cube.get_polygons()[2], 0)



lvl_manager.LevelManagerObject.OnTick = tick
lvl_manager.run()

print('hello')