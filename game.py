import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ---------------- LOAD ASSETS ----------------
def load_image(path, size=None):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    return None

background = load_image("assets/background.png", (WIDTH, HEIGHT))
player_img = load_image("assets/player.png", (60, 50))
enemy_img = load_image("assets/enemy.png", (40, 40))
bullet_img = load_image("assets/bullet.png", (10, 20))

# Sounds
shoot_sound = pygame.mixer.Sound("assets/shoot.wav") if os.path.exists("assets/shoot.wav") else None
hit_sound = pygame.mixer.Sound("assets/hit.wav") if os.path.exists("assets/hit.wav") else None

# ---------------- GAME STATE ----------------
START, PLAYING, GAME_OVER = "start", "playing", "game_over"
game_state = START

# ---------------- RESET ----------------
def reset_game():
    global player, bullets, enemies, score, level, enemy_speed
    player = pygame.Rect(WIDTH//2 - 30, HEIGHT - 70, 60, 50)
    bullets = []
    enemies = []
    score = 0
    level = 1
    enemy_speed = 4

reset_game()

player_speed = 7
bullet_speed = 9
enemy_timer = 0

# ---------------- BUTTON ----------------
def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, RED, (x, y, w, h), border_radius=8)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, (x + w//2 - txt.get_width()//2, y + h//2 - txt.get_height()//2))

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START and event.type == pygame.MOUSEBUTTONDOWN:
            if 300 <= event.pos[0] <= 500 and 300 <= event.pos[1] <= 360:
                reset_game()
                game_state = PLAYING

        if game_state == PLAYING and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.centerx - 5, player.top, 10, 20))
                if shoot_sound:
                    shoot_sound.play()

        if game_state == GAME_OVER and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_state = START

    # ---------------- START SCREEN ----------------
    if game_state == START:
        screen.fill(BLACK)
        screen.blit(big_font.render("SPACE SHOOTER", True, WHITE), (200, 180))
        draw_button("START GAME", 300, 300, 200, 60)

    # ---------------- PLAYING ----------------
    elif game_state == PLAYING:
        screen.fill(BLACK)
        if background:
            screen.blit(background, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        enemy_timer += 1
        if enemy_timer > max(20, 60 - level * 5):
            enemies.append(pygame.Rect(random.randint(0, WIDTH-40), 0, 40, 40))
            enemy_timer = 0

        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.y += enemy_speed

            for bullet in bullets[:]:
             if enemy.colliderect(bullet):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    if hit_sound:
                        hit_sound.play()
                    if score % 5 == 0:
                        level += 1
                        enemy_speed += 1
                    break

            if enemy.colliderect(player):
                game_state = GAME_OVER

        # Draw player
        if player_img:
            screen.blit(player_img, player)
        else:
            pygame.draw.rect(screen, WHITE, player)

        # Draw bullets
        for bullet in bullets:
            if bullet_img:
                screen.blit(bullet_img, bullet)
            else:
                pygame.draw.rect(screen, RED, bullet)

        # Draw enemies
        for enemy in enemies:
            if enemy_img:
                screen.blit(enemy_img, enemy)
            else:
                pygame.draw.rect(screen, WHITE, enemy)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 40))

    # ---------------- GAME OVER ----------------
    elif game_state == GAME_OVER:
        screen.fill(BLACK)
        screen.blit(big_font.render("GAME OVER", True, RED), (260, 220))
        screen.blit(font.render("Press R to Restart", True, WHITE), (290, 300))

    pygame.display.update()

pygame.quit()
sys.exit()
