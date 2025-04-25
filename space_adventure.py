import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Asset loading function
def load_image(name):
    image_path = os.path.join('assets', 'images', name)
    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Cannot load image: {image_path}")
        print(e)
        return pygame.Surface((30, 30))

# Game settings
FPS = 60

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Adventure - Debug Challenge")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Load game images
player_img = load_image('player.png')
player_mini_img = load_image('player_mini.png')
bullet_img = load_image('bullet.png')
enemy_imgs = [load_image(f'enemy{i}.png') for i in range(1, 4)]
powerup_imgs = {
    'shield': load_image('powerup_shield.png'),
    'power': load_image('powerup_power.png')
}
explosion_imgs = [load_image(f'explosion{i}.png') for i in range(1, 6)]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = 0
        self.power_level = 1
        self.power_timer = 0

    def update(self):
        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = SCREEN_WIDTH // 2
            self.rect.bottom = SCREEN_HEIGHT - 10

        # Power up timeout
        if self.power_level > 1 and pygame.time.get_ticks() - self.power_timer > 5000:
            self.power_level -= 1
            self.power_timer = pygame.time.get_ticks()

        # Movement
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = 8
        if keystate[pygame.K_RIGHT]:
            self.speed_x = -8

        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH + 20:
            self.rect.right = SCREEN_WIDTH + 20
        if self.rect.left < -20:
            self.rect.left = -20

    def shoot(self):
        if not self.hidden:
            if self.power_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.power_level >= 2:
                bullet1 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 200)

    def powerup(self):
        self.power_level += 1
        self.power_timer = pygame.time.get_ticks()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_imgs)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

        if self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 25:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 1

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Powerup class
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['shield', 'power'])
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Explosion animation class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.images = explosion_imgs
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= 5:
                self.kill()
            elif self.frame < 5:
                self.image = self.images[self.frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

# Function to draw text
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Function to draw shield bar
def draw_shield_bar(surface, x, y, percentage):
    if percentage < 0:
        percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

# Function to draw lives
def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)

# Game loop
def main_game():
    global all_sprites, bullets, enemies, powerups
    
    game_over = False
    running = True
    
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    # Create enemies
    for i in range(8):
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)
    
    # Score
    score = 0
    
    # Main game loop
    while running:
        # Keep loop running at the right speed
        clock.tick(FPS)
        
        # Process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        
        # Update
        all_sprites.update()
        
        # Check bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for hit in hits:
            score += 10
            # Create explosion
            explosion = Explosion(hit.rect.center, 30)
            all_sprites.add(explosion)
            # Spawn new enemy
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
            # Random chance for power-up
            if random.random() > 0.5:  # 50% chance
                powerup = Powerup()
                all_sprites.add(powerup)
                powerups.add(powerup)
        
        # Check player-enemy collisions
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.shield -= 20
            explosion = Explosion(hit.rect.center, 10)
            all_sprites.add(explosion)
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
            if player.shield <= 0:
                # player.lives -= 1
                player.shield = 100
                player.hide()
                if player.lives == 0:
                    game_over = True
        
        # Check player-powerup collisions
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += 20
                if player.shield > 100:
                    player.shield = 100
            if hit.type == 'power':
                player.powerup()
        
        if game_over:
            pass
            
        # Draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Draw UI
        draw_text(screen, str(score), 18, SCREEN_WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, SCREEN_WIDTH - 100, 5, player.lives, player_mini_img)
        
        # Flip the display
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main_game()
