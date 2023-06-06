
import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Load images
spaceship_img = pygame.image.load("spaceship.png")
bullet_img = pygame.image.load("bullet.png")
enemy_img = pygame.image.load("enemy.png")
asteroid_img = pygame.image.load("asteroid.png")
coin_img = pygame.image.load("coin.png")
background_img = pygame.image.load("background.png")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define game objects
class GameObject:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Spaceship(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 5
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 64:
            self.x += self.speed

    def shoot(self):
        bullet = Bullet(self.x + 24, self.y, bullet_img)
        bullets.append(bullet)

class Bullet(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 10

    def update(self):
        self.y -= self.speed

class EnemyBullet(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 8

    def update(self):
        self.y += self.speed


class Enemy(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = random.randint(1, 3)
        self.shoot_delay = random.randint(1000, 3000)  # Delay between shots in milliseconds
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        self.y += self.speed
        self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            enemy_bullet = EnemyBullet(self.x + 24, self.y + 64, bullet_img)
            enemy_bullets.append(enemy_bullet)
            self.last_shot_time = current_time


class Asteroid(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = random.randint(1, 3)

    def update(self):
        self.y += self.speed

class Coin(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = random.randint(1, 3)

    def update(self):
        self.y += self.speed

# Create game objects
spaceship = Spaceship(WIDTH // 2 - 32, HEIGHT - 64, spaceship_img)
enemies = []
asteroids = []
coins = []
bullets = []
enemy_bullets = []
# Game variables
score = 0
clock = pygame.time.Clock()

# Load background music
pygame.mixer.music.load("background_music.mp3")
# Set background music volume
pygame.mixer.music.set_volume(0.5)
# Play background music in a loop
pygame.mixer.music.play(-1)

# Game loop
running = True
game_over = False
while running:
    clock.tick(60)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spaceship.shoot()

    if not game_over:
        # Update spaceship
        spaceship.update()

        # Update bullets
        for bullet in bullets:
            bullet.update()
            if bullet.y < -32:
                bullets.remove(bullet)
            for enemy in enemies:
                if bullet.x < enemy.x + 64 and bullet.x + 32 > enemy.x and bullet.y < enemy.y + 64 and bullet.y + 32 > enemy.y:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    break
            for asteroid in asteroids:
                if bullet.x < asteroid.x + 64 and bullet.x + 32 > asteroid.x and bullet.y < asteroid.y + 64 and bullet.y + 32 > asteroid.y:
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    score += 5
                    break

        # Update enemy bullets
        for enemy_bullet in enemy_bullets:
            enemy_bullet.update()
            if enemy_bullet.y > HEIGHT:
                enemy_bullets.remove(enemy_bullet)
            if enemy_bullet.x < spaceship.x + 64 and enemy_bullet.x + 32 > spaceship.x and enemy_bullet.y < spaceship.y + 64 and enemy_bullet.y + 32 > spaceship.y:
                spaceship.health -= 10
                enemy_bullets.remove(enemy_bullet)

        # Update enemies
        for enemy in enemies:
            enemy.update()
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            if enemy.x < spaceship.x + 64 and enemy.x + 64 > spaceship.x and enemy.y + 64 > spaceship.y and enemy.y < spaceship.y + 64:
                spaceship.health -= 10
                enemies.remove(enemy)

        # Update asteroids
        for asteroid in asteroids:
            asteroid.update()
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
            if asteroid.x < spaceship.x + 64 and asteroid.x + 64 > spaceship.x and asteroid.y + 64 > spaceship.y and asteroid.y < spaceship.y + 64:
                spaceship.health -= 5
                asteroids.remove(asteroid)

        # Update coins
        for coin in coins:
            coin.update()
            if coin.y > HEIGHT:
                coins.remove(coin)
            if coin.x < spaceship.x + 64 and coin.x + 64 > spaceship.x and coin.y + 64 > spaceship.y and coin.y < spaceship.y + 64:
                score += 5
                coins.remove(coin)

        # Generate enemies, asteroids, and coins
        if random.random() < 0.01:
            enemy = Enemy(random.randint(0, WIDTH - 64), -64, enemy_img)
            enemies.append(enemy)
        if random.random() < 0.005:
            asteroid = Asteroid(random.randint(0, WIDTH - 64), -64, asteroid_img)
            asteroids.append(asteroid)
        if random.random() < 0.01:
            coin = Coin(random.randint(0, WIDTH - 64), -64, coin_img)
            coins.append(coin)

    # Clear the screen
    screen.blit(background_img, (0, 0))

    # Draw game objects
    spaceship.draw()
    for bullet in bullets:
        bullet.draw()
    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw()
    for enemy in enemies:
        enemy.draw()
    for asteroid in asteroids:
        asteroid.draw()
    for coin in coins:
        coin.draw()

    # Draw score and health
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    health_text = score_font.render("Health: " + str(spaceship.health), True, WHITE)
    screen.blit(health_text, (10, 50))

    # Check game over condition
    if spaceship.health <= 0:
        game_over = True
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        retry_text = score_font.render("Press R to Retry", True, WHITE)
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))
        quit_text = score_font.render("Press Q to Quit", True, WHITE)
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))
        pygame.mixer.music.stop()

    # Update the display
    pygame.display.flip()

    # Retry or quit game
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    score = 0
                    spaceship.health = 100
                    enemies.clear()
                    asteroids.clear()
                    coins.clear()
                    bullets.clear()
                    enemy_bullets.clear()
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_q:
                    running = False

# Quit the game
pygame.quit()







