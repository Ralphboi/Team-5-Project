import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 480, 576
BOAT_SPEED = 2
GAME_TIME = 60
MIN_DISTANCE = 40
COLLISION_RADIUS = 20
LAPS_TO_WIN = 10

point_sound = pygame.mixer.Sound("Point Collected.wav")
boat_sprite = pygame.image.load('boat.png')
boat_sprite = pygame.transform.scale(boat_sprite, (32 * 3, 32 * 3))
boat2_sprite = pygame.image.load('boat2.png')
boat2_sprite = pygame.transform.scale(boat2_sprite, (32 * 3, 32 * 3))
boat3_sprite = pygame.image.load('boat3.png')
boat3_sprite = pygame.transform.scale(boat3_sprite, (32 * 3, 32 * 3))
boat4_sprite = pygame.image.load('boat4.png')
boat4_sprite = pygame.transform.scale(boat4_sprite, (32 * 3, 32 * 3))
finish_sprite = pygame.image.load('finish.png')
finish_sprite = pygame.transform.scale(finish_sprite, (32 * 3, 32 * 3))

boat_x = WIDTH // 2
barrier_y = HEIGHT  # Позиция барьера на нижней границе
line_y = random.randint(0, HEIGHT - boat2_sprite.get_height())
boat_y = line_y
boat2_y = line_y
boat3_y = line_y
boat4_y = line_y

offset = 20
boat2_x = boat_x + random.randint(-offset, offset)
boat3_x = boat_x + random.randint(-offset, offset)
boat4_x = boat_x + random.randint(-offset, offset)

game_over = False
time_remaining = GAME_TIME * 60
laps = 0
opponent_laps = 0  # Счетчик кругов противника

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boat Race")
clock = pygame.time.Clock()


def draw_background():
    screen.fill((0, 0, 50))


def handle_events():
    global boat_x, boat_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        boat_x -= BOAT_SPEED
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        boat_x += BOAT_SPEED
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        boat_y -= BOAT_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        boat_y += BOAT_SPEED


def draw_objects():
    screen.blit(boat_sprite, (boat_x, boat_y))
    screen.blit(boat2_sprite, (boat2_x, boat2_y))
    screen.blit(boat3_sprite, (boat3_x, boat3_y))
    screen.blit(boat4_sprite, (boat4_x, boat4_y))


def check_collision(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distance < COLLISION_RADIUS * 2:
        return True
    return False


def check_boundaries(boat_x, boat_y):
    if boat_x < 0:
        boat_x = WIDTH - boat_sprite.get_width()
    elif boat_x > WIDTH - boat_sprite.get_width():
        boat_x = 0
    if boat_y < 0:
        boat_y = HEIGHT - boat_sprite.get_height()
    elif boat_y > HEIGHT - boat_sprite.get_height():
        boat_y = HEIGHT - boat_sprite.get_height()
    return boat_x, boat_y


def main():
    pygame.init()

    global boat_x, boat_y, boat2_x, boat2_y, boat3_x, boat3_y, boat4_x, boat4_y, time_remaining, game_over, laps, opponent_laps

    font = pygame.font.Font("Pixeltype.ttf", 24)

    while True:
        draw_background()
        handle_events()

        boat2_y -= random.randint(1, 5) / 2 * 1.2
        boat3_y -= random.randint(1, 5) / 2 * 1.2
        boat4_y -= random.randint(1, 5) / 2 * 1.2

        boat_x, boat_y = check_boundaries(boat_x, boat_y)

        # Обновляем счетчик кругов игрока и проверяем поражение
        if boat_y == 0:
            laps += 1
            point_sound.play()

        # Обновляем счетчик кругов противника и проверяем поражение
        if boat2_y < -boat2_sprite.get_height():
            boat2_x = random.randint(0, WIDTH - boat2_sprite.get_width())
            boat2_y = HEIGHT
            opponent_laps += 1

        if boat3_y < -boat3_sprite.get_height():
            boat3_x = random.randint(0, WIDTH - boat3_sprite.get_width())
            boat3_y = HEIGHT

        if boat4_y < -boat4_sprite.get_height():
            boat4_x = random.randint(0, WIDTH - boat4_sprite.get_width())
            boat4_y = HEIGHT

        # Проверяем столкновения
        if check_collision(boat_x, boat_y, boat2_x, boat2_y) or \
                check_collision(boat_x, boat_y, boat3_x, boat3_y) or \
                check_collision(boat_x, boat_y, boat4_x, boat4_y):
            game_over = True

        # Проверяем достижение противником 10 очков
        if opponent_laps >= LAPS_TO_WIN:
            game_over = True

        # Рисуем объекты на экране
        draw_objects()

        # Выводим счетчик кругов на экран
        laps_text = font.render(f"Laps: {laps}", True, (255, 255, 255))
        screen.blit(laps_text, (10, 10))

        # Выводим счетчик кругов противника на экран
        opponent_laps_text = font.render(f"Opponent Laps: {opponent_laps}", True, (255, 255, 255))
        screen.blit(opponent_laps_text, (10, 40))

        pygame.display.flip()
        time_remaining -= 1
        clock.tick(60)


if __name__ == "__main__":
    main()
