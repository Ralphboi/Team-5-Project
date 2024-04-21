import pygame
from pygame.locals import *
import random
import time

def main():
    pygame.init()

    width = 500
    height = 500
    screen_size = (width, height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Уровень 5')

    green = (76, 208, 56)

    lane_marker_move_y = 0

    player_x = 250
    player_y = 400

    clock = pygame.time.Clock()
    fps = 120

    point_sound = pygame.mixer.Sound("Point Collected 2.wav")
    explosion_sound = pygame.mixer.Sound("Damage.wav")
    font_pixeltype = pygame.font.Font('Pixeltype.ttf', 24)

    class Vehicle(pygame.sprite.Sprite):
        
        def __init__(self, image, x, y, scale=1.5):
            pygame.sprite.Sprite.__init__(self)
            
            image_scale = 45 / image.get_rect().width * scale
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (int(new_width), int(new_height))) 
            
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            
    class PlayerVehicle(Vehicle):
        
        def __init__(self, x, y):
            image = pygame.image.load('images/car.png')
            super().__init__(image, x, y)
            
    player_group = pygame.sprite.Group()
    vehicle_group = pygame.sprite.Group()

    player = PlayerVehicle(player_x, player_y)
    player_group.add(player)

    cat_images = [pygame.image.load('images/' + filename) for filename in ['cat1.png', 'cat2.png', 'cat3.png']]

    crash = pygame.image.load('images/crash.png')
    crash_rect = crash.get_rect()

    def reset_game():
        nonlocal score, speed, gameover
        
        score = 0
        speed = 2
        vehicle_group.empty()
        player.rect.center = [player_x, player_y]
        gameover = False

    reset_game()

    running = True
    while running:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                    
            if event.type == KEYDOWN:
                
                if event.key == K_a and player.rect.center[0] > 150:
                    player.rect.x -= 100
                elif event.key == K_d and player.rect.center[0] < 350:
                    player.rect.x += 100
                        
                for vehicle in vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle):
                        
                        gameover = True
                        
                        if event.key == K_a:
                            player.rect.left = vehicle.rect.right
                            crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                        elif event.key == K_d:
                            player.rect.right = vehicle.rect.left
                            crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                
                
        screen.fill(green)
        
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= 50 * 2:
            lane_marker_move_y = 0
                
        if len(vehicle_group) < 2:
            
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
                        
            if add_vehicle:
                lane = random.choice([150, 250, 350])
                    
                image = random.choice(cat_images)
                vehicle = Vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle)
            
        for vehicle in vehicle_group:
            vehicle.rect.y += speed
                
            if vehicle.rect.top >= height:
                vehicle.kill()
                    
                score += 1
                    
                if score > 0 and score % 1 == 0:
                    speed += 0.3
                    point_sound.play()
        
        player_group.draw(screen)
        vehicle_group.draw(screen)
        
        text = font_pixeltype.render('Score: ' + str(score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (50, 400)
        screen.blit(text, text_rect)
        
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]
                
        if gameover:
            screen.blit(crash, crash_rect)
            pygame.display.update()
            explosion_sound.play()  
            time.sleep(1)  
            reset_game()
                
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
