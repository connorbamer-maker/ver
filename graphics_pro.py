import pygame
import math
from base_classes import Vector2, WHITE, GRAY, CYAN, BLUE, RED, PURPLE

class TextureEngine:
    def __init__(self):
        self.ship_cache = {}
        self.asteroid_cache = {}

    def get_ship_texture(self, radius, color):
        """Creates a high-fidelity ship texture with shading and lights."""
        tag = (radius, color)
        if tag in self.ship_cache: return self.ship_cache[tag]

        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        center = radius
        
        # 1. Outer Glow/Atmosphere
        for r in range(radius, radius - 4, -1):
            pygame.draw.circle(surf, (*color, 100), (center, center), r)

        # 2. Main Hull (Gradient effect)
        pygame.draw.circle(surf, color, (center, center), radius - 2)
        
        # 3. Cockpit/Glass
        glass_color = (200, 230, 255, 200)
        pygame.draw.ellipse(surf, glass_color, (center - 5, center - 8, 10, 12))
        
        # 4. Specular Highlight (Shiny spot)
        pygame.draw.circle(surf, WHITE, (center - 4, center - 4), radius // 4)

        self.ship_cache[tag] = surf
        return surf

    def draw_thruster(self, screen, ship):
        """Adds an animated blue/orange engine flame."""
        # Calculate back of ship based on velocity
        if ship.vel.length() > 10:
            back_dir = ship.vel.normalize() * -1
            flame_pos = ship.pos + (back_dir * ship.radius)
            
            # Draw flicker flame
            flame_size = int(random.uniform(5, 12))
            pygame.draw.circle(screen, (255, 200, 50), (int(flame_pos.x), int(flame_pos.y)), flame_size)
            pygame.draw.circle(screen, WHITE, (int(flame_pos.x), int(flame_pos.y)), flame_size // 2)

    def draw_neon_bullet(self, screen, bullet):
        """Draws glowing tracer rounds instead of dots."""
        # Tracer line
        start = bullet.pos
        end = bullet.pos - (bullet.vel * 0.04)
        pygame.draw.line(screen, bullet.color, start, end, 5)
        pygame.draw.line(screen, WHITE, start, end, 2)

def init(api):
    engine = TextureEngine()

    def on_draw(screen, game):
        # 1. Draw Player with new textures
        ship_tex = engine.get_ship_texture(game.player.radius, game.player.color)
        engine.draw_thruster(screen, game.player)
        screen.blit(ship_tex, (game.player.pos.x - game.player.radius, game.player.pos.y - game.player.radius))

        # 2. Draw Enemies with new textures
        for enemy in game.enemies:
            if hasattr(enemy, 'radius'):
                e_tex = engine.get_ship_texture(enemy.radius, enemy.color)
                screen.blit(e_tex, (enemy.pos.x - enemy.radius, enemy.pos.y - enemy.radius))

        # 3. Draw Neon Bullets
        for bullet in game.bullets:
            engine.draw_neon_bullet(screen, bullet)

    api.on_event('on_draw', on_draw)
    print("🚀 Texture Revamp Mod Loaded: Procedural Sprites Active.")

import random # Required for thruster flicker