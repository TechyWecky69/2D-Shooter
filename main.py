import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooter")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
FPS = 60

player_size = 40
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
player_color = RED
lives = 3

player_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
pygame.draw.rect(player_surface, player_color, (0, 0, player_size, player_size))

enemy_size = 30
enemy_speed = 2
enemy_color = BLUE
enemy_spawn_interval = 500
last_enemy_spawn_time = pygame.time.get_ticks()

bullet_speed = 10
bullet_size = 10
bullet_color = YELLOW

score = 0

font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

enemies = []
bullets = []


def get_angle_to_mouse(player_pos, mouse_pos):
    dx, dy = mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]
    return math.degrees(math.atan2(-dy, dx))


def calculate_bullet_direction(angle):
    radians = math.radians(angle)
    return math.cos(radians), -math.sin(radians)


def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x, y = random.randint(0, WIDTH), 0
    elif side == "bottom":
        x, y = random.randint(0, WIDTH), HEIGHT
    elif side == "left":
        x, y = 0, random.randint(0, HEIGHT)
    else:  # "right"
        x, y = WIDTH, random.randint(0, HEIGHT)

    return {"pos": [x, y], "surface": pygame.Surface((enemy_size, enemy_size), pygame.SRCALPHA)}


def render_ui():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 120, 10))


# Game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not game_over:  # Right-click
            angle = get_angle_to_mouse(player_pos, pygame.mouse.get_pos())
            direction = calculate_bullet_direction(angle)
            bullets.append({"pos": [player_pos[0], player_pos[1]], "dir": direction})

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed

        mouse_pos = pygame.mouse.get_pos()

        angle = get_angle_to_mouse(player_pos, mouse_pos)

        rotated_player = pygame.transform.rotate(player_surface, angle)

        rotated_rect = rotated_player.get_rect(center=(player_pos[0], player_pos[1]))

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > enemy_spawn_interval:
            enemy = spawn_enemy()
            enemies.append(enemy)
            last_enemy_spawn_time = current_time

        for enemy in enemies[:]:
            enemy_pos = enemy["pos"]
            dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                enemy_pos[0] += enemy_speed * (dx / distance)
                enemy_pos[1] += enemy_speed * (dy / distance)

            player_rect = pygame.Rect(player_pos[0] - player_size // 2,
                                      player_pos[1] - player_size // 2,
                                      player_size, player_size)
            enemy_rect = pygame.Rect(enemy_pos[0] - enemy_size // 2,
                                     enemy_pos[1] - enemy_size // 2,
                                     enemy_size, enemy_size)
            if player_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                lives -= 1
                if lives <= 0:
                    game_over = True

        for bullet in bullets[:]:
            bullet["pos"][0] += bullet_speed * bullet["dir"][0]
            bullet["pos"][1] += bullet_speed * bullet["dir"][1]

            if not (0 <= bullet["pos"][0] <= WIDTH and 0 <= bullet["pos"][1] <= HEIGHT):
                bullets.remove(bullet)
                continue

            bullet_rect = pygame.Rect(bullet["pos"][0] - bullet_size // 2,
                                      bullet["pos"][1] - bullet_size // 2,
                                      bullet_size, bullet_size)
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy["pos"][0] - enemy_size // 2,
                                         enemy["pos"][1] - enemy_size // 2,
                                         enemy_size, enemy_size)
                if bullet_rect.colliderect(enemy_rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    break

    screen.fill(BLACK)

    if not game_over:
        for bullet in bullets:
            pygame.draw.circle(screen, bullet_color, (int(bullet["pos"][0]), int(bullet["pos"][1])), bullet_size // 2)

        for enemy in enemies:
            enemy_surface = enemy["surface"]
            enemy_surface.fill(enemy_color)
            enemy_rect = enemy_surface.get_rect(center=enemy["pos"])
            screen.blit(enemy_surface, enemy_rect.topleft)

        screen.blit(rotated_player, rotated_rect.topleft)

        render_ui()
    else:
        game_over_text = game_over_font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()