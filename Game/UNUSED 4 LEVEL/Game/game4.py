import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
BOAT_WIDTH = 150
BOAT_HEIGHT = 50
BOAT_SPEED = 5
WATER_COLOR = (30, 144, 255)
PLAYER_START_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
BOAT_COUNT = 4

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Crossy River')

player_image = pygame.image.load('Mouse.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
finish_image = pygame.image.load('finish.png').convert_alpha()
finish_image = pygame.transform.scale(finish_image, (SCREEN_WIDTH, PLAYER_SIZE))
boat_images = [
    pygame.image.load('Boat.png').convert_alpha(),
    pygame.image.load('boat2.png').convert_alpha(),
    pygame.image.load('boat3.png').convert_alpha(),
    pygame.image.load('boat4.png').convert_alpha()
]
for i, img in enumerate(boat_images):
    boat_images[i] = pygame.transform.scale(img, (BOAT_WIDTH, BOAT_HEIGHT))

player_rect = pygame.Rect(PLAYER_START_POS, (PLAYER_SIZE, PLAYER_SIZE))

boats = [
    {"rect": pygame.Rect(random.randrange(0, SCREEN_WIDTH - BOAT_WIDTH), i * (SCREEN_HEIGHT // BOAT_COUNT), BOAT_WIDTH, BOAT_HEIGHT), "image": img}
    for i, img in enumerate(random.sample(boat_images, BOAT_COUNT))
]

def reset_game():
    player_rect.topleft = PLAYER_START_POS
    for i in range(5):
        boats[i] = {
            "rect": pygame.Rect(random.randrange(0, SCREEN_WIDTH - BOAT_WIDTH), i * 120, BOAT_WIDTH, BOAT_HEIGHT),
            "image": random.choice(boat_images)
        }

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

font = pygame.font.SysFont(None, 48)

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_rect.y -= 5
        if keys[pygame.K_s]:
            player_rect.y += 5
        if keys[pygame.K_a]:
            player_rect.x -= 5
        if keys[pygame.K_d]:
            player_rect.x += 5

        player_rect.clamp_ip(screen.get_rect())
        
        for boat in boats:
            boat["rect"].x += BOAT_SPEED if boat["rect"].y % 240 < 120 else -BOAT_SPEED
            if boat["rect"].right < 0 or boat["rect"].left > SCREEN_WIDTH:
                boat["rect"].x = -BOAT_WIDTH if boat["rect"].x > 0 else SCREEN_WIDTH
            
            if player_rect.colliderect(boat["rect"]):
                game_over = True

        if player_rect.top <= 0 and not game_over:
            draw_text('You Win!', font, (0, 128, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            reset_game()
            game_over = False

    screen.fill(WATER_COLOR)
    for boat in boats:
        screen.blit(boat["image"], boat["rect"].topleft)

    if game_over:
        draw_text('Game Over!', font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    else:
        screen.blit(player_image, player_rect.topleft)

    pygame.display.flip()
    
    pygame.time.Clock().tick(30)

pygame.quit()