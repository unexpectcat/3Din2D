import pygame
import math

class LitObject:
    def __init__(self, position, texture, shadow_map):
        self.position = position
        self.texture = texture
        self.shadow_map = shadow_map

    def get_polygons(self):
        return self.shadow_map


    def set_light_position(self, new_light_source):
        self.light_source = new_light_source

    def get_surface(self):
        def shade(dx, dy, base=200, limit=160, offset=100):
            return max(0, min(limit, int((dx + dy) / 2) + base))
        
        width, height = self.texture.get_size()

        asset_surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        asset_surface.blit(self.texture, (0, 0))

        limit_light_lvl_inner = 170
        limit_light_lvl_outer = 160
        base_light_lvl_inner = 200
        base_light_lvl_outer = 120

        

        for light_source in self.light_source:
            lx, ly, r, g, b, light_lenth = light_source
            light_lenth *= -1
            
            left_horisontal_light=lx - self.position[0] - width
            right_horisontal_light=-lx + self.position[0]
            top_vertical_light=ly - self.position[1] - height
            bottom_vertical_light=-ly + self.position[1]
            
            

            if left_horisontal_light < light_lenth - width:
                left_horisontal_light=-lx + self.position[0] - width + light_lenth 
            else:
                left_horisontal_light=lx - self.position[0] - width
            
            
            if right_horisontal_light < light_lenth - width:
                right_horisontal_light= lx - self.position[0] - width * 2 + light_lenth
            else:
                right_horisontal_light=-lx + self.position[0]

            
            if top_vertical_light < light_lenth:
                top_vertical_light = -ly + self.position[1] - height + light_lenth
            else:
                top_vertical_light=ly - self.position[1] - height
            
            
            if bottom_vertical_light < light_lenth - height:
                bottom_vertical_light = ly - self.position[1] - height * 2 + light_lenth
            else:
                bottom_vertical_light=-ly + self.position[1]
            
            shadow_colors = [
                # --- Outer side bevels ---
                (10, 10, 10, shade(top_vertical_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),        # Top
                (10, 10, 10, shade(left_horisontal_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),     # Left
                (10, 10, 10, shade(bottom_vertical_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),     # Bottom
                (10, 10, 10, shade(right_horisontal_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),    # Right

                # --- Outer corner bevels ---
                (10, 10, 10, shade(top_vertical_light / 2, left_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),   # Top-left
                (10, 10, 10, shade(top_vertical_light / 2, right_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),  # Top-right
                (10, 10, 10, shade(bottom_vertical_light / 2, left_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),# Bottom-left
                (10, 10, 10, shade(bottom_vertical_light / 2, right_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),# Bottom-right


                # --- Inner side bevels ---
                (10, 10, 10, shade(top_vertical_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),   # Inner top
                (10, 10, 10, shade(left_horisontal_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Inner left
                (10, 10, 10, shade(bottom_vertical_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Inner bottom
                (10, 10, 10, shade(right_horisontal_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Inner right

                # --- Inner corner bevels ---
                (10, 10, 10, shade(top_vertical_light / 2, left_horisontal_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),  # Bevel top-left (duplicate ok)
                (10, 10, 10, shade(top_vertical_light / 2, right_horisontal_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),  # Bevel top-right
                (10, 10, 10, shade(left_horisontal_light / 2,bottom_vertical_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Bevel bottom-left
                (10, 10, 10, shade(right_horisontal_light / 2, bottom_vertical_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner))# Bevel bottom-righ
            ]

            shadow_layer = pygame.Surface((width, height), flags=pygame.SRCALPHA)

            polygons = self.get_polygons()
            for i in range(min(16, len(polygons))):
                for layer in polygons[i]:
                    pygame.draw.polygon(shadow_layer, shadow_colors[i], layer, 0)

            asset_surface.blit(shadow_layer, (0, 0))

            left_horisontal_light = -lx + self.position[0]  # swapped with original right
            right_horisontal_light = lx - self.position[0] - width  # swapped with original left
            top_vertical_light = -ly + self.position[1]  # swapped with original bottom
            bottom_vertical_light = ly - self.position[1] - height  # swapped with original top

            if left_horisontal_light < light_lenth - width:
                left_horisontal_light = lx - self.position[0] - width + light_lenth
            else:
                left_horisontal_light = -lx + self.position[0]

            if right_horisontal_light < light_lenth - width:
                right_horisontal_light = -lx + self.position[0] - width * 2 + light_lenth
            else:
                right_horisontal_light = lx - self.position[0] - width

            if top_vertical_light < light_lenth:
                top_vertical_light = ly - self.position[1] - height + light_lenth
            else:
                top_vertical_light = -ly + self.position[1]

            if bottom_vertical_light < light_lenth - height:
                bottom_vertical_light = -ly + self.position[1] - height * 2 + light_lenth
            else:
                bottom_vertical_light = ly - self.position[1] - height

            shadow_colors = [
                # --- Outer side bevels ---
                (r, g, b, shade(top_vertical_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),        # Top
                (r, g, b, shade(left_horisontal_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),     # Left
                (r, g, b, shade(bottom_vertical_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),     # Bottom
                (r, g, b, shade(right_horisontal_light, 0, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),    # Right

                # --- Outer corner bevels ---
                (r, g, b, shade(top_vertical_light / 2, left_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),   # Top-left
                (r, g, b, shade(top_vertical_light / 2, right_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),  # Top-right
                (r, g, b, shade(bottom_vertical_light / 2, left_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),# Bottom-left
                (r, g, b, shade(bottom_vertical_light / 2, right_horisontal_light / 2, base=base_light_lvl_outer, limit=limit_light_lvl_outer)),# Bottom-right


                # --- Inner side bevels ---
                (r, g, b, shade(top_vertical_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),   # Inner top
                (r, g, b, shade(left_horisontal_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Inner left
                (r, g, b, shade(bottom_vertical_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Inner bottom
                (r, g, b, shade(right_horisontal_light, 0, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Inner right

                # --- Inner corner bevels ---
                (r, g, b, shade(top_vertical_light / 2, left_horisontal_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),  # Bevel top-left (duplicate ok)
                (r, g, b, shade(top_vertical_light / 2, right_horisontal_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),  # Bevel top-right
                (r, g, b, shade(left_horisontal_light / 2,bottom_vertical_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner)),# Bevel bottom-left
                (r, g, b, shade(right_horisontal_light / 2, bottom_vertical_light / 2, base=base_light_lvl_inner, limit=limit_light_lvl_inner))# Bevel bottom-righ
            ]

            shadow_layer = pygame.Surface((width, height), flags=pygame.SRCALPHA)

            polygons = self.get_polygons()
            # for i in range(min(16, len(polygons))):
            #     pygame.draw.polygon(shadow_layer, shadow_colors[i], polygons[i], 0)
            for i in range(min(16, len(polygons))):
                for layer in polygons[i]:
                    pygame.draw.polygon(shadow_layer, shadow_colors[i], layer, 0)

            asset_surface.blit(shadow_layer, (0, 0))

        return asset_surface