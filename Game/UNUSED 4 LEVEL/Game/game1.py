import pygame
import random

pygame.init()

WIDTH, HEIGHT = 256, 298
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Побег Литтла от Снежка")

player_img = pygame.image.load("mouse.png")
player_img = pygame.transform.scale(player_img, (24, 24))
enemy_img = pygame.image.load("cat.png")
enemy_img = pygame.transform.scale(enemy_img, (48, 48))

def draw_objects(player_pos, enemy_pos, cheese_list):
    screen.fill((0, 0, 0))
    screen.blit(player_img, player_pos)
    screen.blit(enemy_img, enemy_pos)
    for cheese in cheese_list:
        pygame.draw.rect(screen, (255, 255, 0), cheese)
    pygame.display.update()

def collision(player_pos, enemy_pos):
    return pygame.Rect(*player_pos, 18, 18).colliderect(pygame.Rect(*enemy_pos, 44, 44))

def wrap_around(player_pos):
    if player_pos[1] < 0:
        player_pos[1] = HEIGHT - 24
    elif player_pos[1] > HEIGHT - 24:
        player_pos[1] = 0

def game():
    player_pos = [WIDTH/2, HEIGHT/2]
    enemy_pos = [random.randint(0, WIDTH - 48), random.randint(0, HEIGHT - 48)]
    cheese_list = [pygame.Rect(random.randint(0, WIDTH - 6), random.randint(0, HEIGHT - 6), 6, 6) for _ in range(10)]
    game_over = False
    cheese_collected = 0
    player_speed = 2

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if player_pos[0] < 0:
            player_pos[0] = WIDTH - 24
        elif player_pos[0] > WIDTH - 24:
            player_pos[0] = 0

        player_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
        player_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed
        wrap_around(player_pos)

        if player_pos[0] < enemy_pos[0]:
            enemy_pos[0] -= 1
        elif player_pos[0] > enemy_pos[0]:
            enemy_pos[0] += 1
        if player_pos[1] < enemy_pos[1]:
            enemy_pos[1] -= 1
        elif player_pos[1] > enemy_pos[1]:
            enemy_pos[1] += 1

        draw_objects(player_pos, enemy_pos, cheese_list)

        if collision(player_pos, enemy_pos):
            game_over = True

        for cheese in cheese_list:
            if cheese.colliderect(pygame.Rect(*player_pos, 18, 18)):
                cheese_list.remove(cheese)
                cheese_collected += 1

        if cheese_collected >= 10:
            font = pygame.font.SysFont(None, 30)  # Увеличен размер шрифта
            text = font.render("You win!", True, (255, 255, 255))
            screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            game_over = True

        pygame.time.Clock().tick(30)

    pygame.quit()

game()
