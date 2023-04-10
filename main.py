import pygame

class Game:
    def __init__(self):
        pygame.init()

        # set screen dimensions
        self.screen_width = 1920
        self.screen_height = 1080

        # create screen object
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # load bubble image
        bubble_image = pygame.image.load("assets/bubble.png")
        bubble_rect = bubble_image.get_rect()

        # load monomer image
        monomer_image = pygame.image.load("assets/monomer.png")
        monomer_rect = monomer_image.get_rect()

        # set window title
        pygame.display.set_caption("ChemoTaxios Simulation")

        # set background color
        self.background_color = (100, 149, 237)  # white

    def run(self):
        # game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # fill screen with background color
            self.screen.fill(self.background_color)

            # update screen
            pygame.display.flip()

        # quit pygame
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
