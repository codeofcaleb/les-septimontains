import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1800, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Journey of Les Septimontains")

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

FLOOR = pygame.Rect(0, 3 * HEIGHT//4, WIDTH, 5)

JULIETTE_WIDTH, JULIETTE_HEIGHT = 15, 60

WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
JUMP_HEIGHT = 30
Y_VEL = JUMP_HEIGHT
X_VEL = 10
GRAVITY = 2
BULLET_VEL = 20

MAX_BULLETS = 3

JULIETTE_HIT = pygame.USEREVENT + 1

def handle_juliette_movement(keys_pressed, juliette):
    global Y_VEL
    if keys_pressed[pygame.K_a] and juliette.x - X_VEL > 0: # LEFT
        juliette.x -= X_VEL
    if keys_pressed[pygame.K_d] and juliette.x + X_VEL < WIDTH - JULIETTE_WIDTH: # RIGHT
        juliette.x += X_VEL

def handle_enemy_movement(enemies):
    for enemy in enemies:
        enemy.x -= random.randint(0, 4)

def handle_bullets(bullets, enemies, boss_mode):
    for bullet in bullets:
        bullet.x += BULLET_VEL
        if not boss_mode:
            for enemy in enemies:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
        if bullet.x > WIDTH:
                bullets.remove(bullet)

def draw_window(juliette, enemies, bullets):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, FLOOR)
    pygame.draw.rect(WIN, GREEN, juliette)
    for enemy in enemies:
        pygame.draw.rect(WIN, RED, enemy)
    for bullet in bullets: 
        pygame.draw.rect(WIN, ORANGE, bullet)
    pygame.display.update()

def draw_winner():
    draw_text = WINNER_FONT.render("You Defeated All of the Enemies!", 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    global Y_VEL
    jumping = False

    juliette = pygame.Rect(WIDTH//2, 3 * HEIGHT//4 - JULIETTE_HEIGHT, JULIETTE_WIDTH, JULIETTE_HEIGHT)

    enemy_count = 0
    stage = 0 
    boss_mode = False
    boss_health = 10
    level_over = False

    enemies = []
    bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        # EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # HIT CHECK
            if event.type == JULIETTE_HIT:
                juliette_health -= 1
            # BULLETS -          -                     -
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(juliette.x + juliette.width, juliette.y + juliette.height//2 - 2, 10, 5)
                    bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

        # ENEMY GENERATION
        if len(enemies) <= 0:
            stage += 1
            enemy1 = pygame.Rect(WIDTH - 100, 3 * HEIGHT//4 - JULIETTE_HEIGHT, JULIETTE_WIDTH, JULIETTE_HEIGHT)
            enemy2 = pygame.Rect(WIDTH - 140, 3 * HEIGHT//4 - JULIETTE_HEIGHT, JULIETTE_WIDTH, JULIETTE_HEIGHT)
            enemy3 = pygame.Rect(WIDTH - 180, 3 * HEIGHT//4 - JULIETTE_HEIGHT, JULIETTE_WIDTH, JULIETTE_HEIGHT)
            enemy4 = pygame.Rect(WIDTH - 220, 3 * HEIGHT//4 - JULIETTE_HEIGHT, JULIETTE_WIDTH, JULIETTE_HEIGHT)
            enemy5 = pygame.Rect(WIDTH - 260, 3 * HEIGHT//4 - JULIETTE_HEIGHT, JULIETTE_WIDTH, JULIETTE_HEIGHT)
            if stage == 1:
                enemies.append(enemy1)
                enemies.append(enemy2)
                enemy_count = 2
            if stage == 2: 
                enemies.append(enemy1)
                enemies.append(enemy2)
                enemies.append(enemy3)
                enemy_count = 3
            if stage == 3:
                enemies.append(enemy1)
                enemies.append(enemy2)
                enemies.append(enemy3)
                enemies.append(enemy4)
                enemies.append(enemy5)
            if stage == 4:
                boss = pygame.Rect(WIDTH - 100, 3 * HEIGHT//4 - 4 * JULIETTE_HEIGHT, 4 * JULIETTE_WIDTH, 4 * JULIETTE_HEIGHT)
                enemies.append(boss)
                boss_mode = True

        # SPRITE HANDLERS
        keys_pressed = pygame.key.get_pressed()
        handle_juliette_movement(keys_pressed, juliette)
        handle_enemy_movement(enemies)
        handle_bullets(bullets, enemies, boss_mode)

        # =========== BOSS HANDLER ===========
        if boss_mode:
            for bullet in bullets:
                for enemy in enemies:
                    if enemy.colliderect(bullet):
                        boss_health -= 1
                        if boss_health <= 0:
                            enemies.remove(enemy)
                            draw_winner()
                            level_over = True
                        bullets.remove(bullet)

        # =========== JUMP HANDLER ===========
        if keys_pressed[pygame.K_w]:
            jumping = True
        if jumping:
            juliette.y -= Y_VEL
            Y_VEL -= GRAVITY
            if Y_VEL < -JUMP_HEIGHT:
                jumping = False
                Y_VEL = JUMP_HEIGHT
        # ====================================

        if level_over:
            break

        draw_window(juliette, enemies, bullets)

    pygame.quit()

if __name__ == "__main__":
    main()