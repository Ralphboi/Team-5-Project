import pygame
import sys
import game1
import game2
import game3  

class Menu:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Main Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Pixeltype.ttf", 36)
        self.selected_option = 0
        self.options = ["Game 1", "Game 2", "Game 3", "Quit"] 

    def display_menu(self):
        self.screen.fill((0, 0, 0))  # Чисто черный фон
        for i, option in enumerate(self.options):
            color = (0, 255, 0) if i == self.selected_option else (255, 255, 255)
            text_render = self.font.render(option, True, color)
            text_rect = text_render.get_rect(center=(self.WIDTH // 2, 200 + i * 50))
            self.screen.blit(text_render, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        game1.main()
                    elif self.selected_option == 1:
                        width, height = game2.main()
                        self.WIDTH, self.HEIGHT = width, height
                        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                    elif self.selected_option == 2:
                        game3.main()  
                    elif self.selected_option == 3:
                        pygame.quit()
                        sys.exit()

    def run_menu(self):
        while True:
            self.display_menu()
            self.handle_events()
            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    menu = Menu()
    menu.run_menu()
