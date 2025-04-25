import pygame
import os

# Initialize pygame
pygame.init()

# Create the assets/images directory if it doesn't exist
if not os.path.exists("assets/images"):
    os.makedirs("assets/images")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Create player sprite
def create_player_sprite():
    # Create a transparent surface for the player ship
    surface = pygame.Surface((50, 40), pygame.SRCALPHA)
    
    # Draw the ship body (triangle)
    pygame.draw.polygon(surface, BLUE, [(25, 0), (0, 40), (50, 40)])
    
    # Draw the cockpit
    pygame.draw.rect(surface, YELLOW, (18, 25, 14, 10))
    
    # Draw engine flames
    pygame.draw.polygon(surface, RED, [(15, 40), (20, 50), (30, 50), (35, 40)])
    
    # Save the image
    pygame.image.save(surface, "assets/images/player.png")
    
    # Create a mini version for lives display
    mini = pygame.Surface((25, 20), pygame.SRCALPHA)
    pygame.draw.polygon(mini, BLUE, [(12, 0), (0, 20), (25, 20)])
    pygame.draw.rect(mini, YELLOW, (9, 12, 7, 5))
    pygame.image.save(mini, "assets/images/player_mini.png")
    
    return surface

# Create enemy sprites (3 different types)
def create_enemy_sprites():
    enemies = []
    
    # Enemy Type 1: Basic saucer
    enemy1 = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(enemy1, RED, (0, 5, 30, 20))
    pygame.draw.ellipse(enemy1, YELLOW, (5, 0, 20, 30))
    pygame.image.save(enemy1, "assets/images/enemy1.png")
    enemies.append(enemy1)
    
    # Enemy Type 2: Octagon
    enemy2 = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.polygon(enemy2, PURPLE, [
        (15, 0), (25, 5), (30, 15), 
        (25, 25), (15, 30), (5, 25),
        (0, 15), (5, 5)
    ])
    pygame.draw.circle(enemy2, RED, (15, 15), 5)
    pygame.image.save(enemy2, "assets/images/enemy2.png")
    enemies.append(enemy2)
    
    # Enemy Type 3: Square with details
    enemy3 = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.rect(enemy3, GREEN, (0, 0, 30, 30))
    pygame.draw.rect(enemy3, BLACK, (5, 5, 20, 20))
    pygame.draw.rect(enemy3, WHITE, (10, 10, 10, 10))
    pygame.image.save(enemy3, "assets/images/enemy3.png")
    enemies.append(enemy3)
    
    return enemies

# Create bullet sprite
def create_bullet_sprite():
    bullet = pygame.Surface((5, 10), pygame.SRCALPHA)
    pygame.draw.rect(bullet, YELLOW, (0, 0, 5, 10))
    pygame.draw.rect(bullet, WHITE, (1, 1, 3, 3))
    pygame.image.save(bullet, "assets/images/bullet.png")
    return bullet

# Create power-up sprites
def create_powerup_sprites():
    powerups = {}
    
    # Shield power-up
    shield = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(shield, BLUE, (10, 10), 10)
    pygame.draw.circle(shield, WHITE, (10, 10), 6, 2)
    pygame.image.save(shield, "assets/images/powerup_shield.png")
    powerups['shield'] = shield
    
    # Power power-up
    power = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(power, YELLOW, (10, 10), 10)
    pygame.draw.polygon(power, RED, [(10, 2), (18, 10), (10, 18), (2, 10)])
    pygame.image.save(power, "assets/images/powerup_power.png")
    powerups['power'] = power
    
    return powerups

# Create explosion frames
def create_explosion_sprites():
    sizes = [20, 30, 40, 50, 60]
    for i, size in enumerate(sizes):
        explosion = pygame.Surface((size, size), pygame.SRCALPHA)
        radius = size // 2
        center = (radius, radius)
        
        # Create a gradient color explosion
        color = (255, 255 - (i * 40), 0)
        for r in range(radius, 0, -4):
            intensity = max(0, min(255, 255 - (radius - r) * 8))
            explosion_color = (color[0], intensity, 0)
            pygame.draw.circle(explosion, explosion_color, center, r)
        
        pygame.image.save(explosion, f"assets/images/explosion{i+1}.png")

# Create all sprites
print("Creating sprites...")
create_player_sprite()
create_enemy_sprites()
create_bullet_sprite()
create_powerup_sprites()
create_explosion_sprites()
print("All sprites created successfully in assets/images/")

pygame.quit()
