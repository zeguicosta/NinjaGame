import sys
import pygame
from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds


# Making the game an object
class Game:
    def __init__(self):
        pygame.init()

        # Sets the window name
        pygame.display.set_caption('Ninja Game')

        # Creates the window and sets the resolution in pixels (2x self.display size)
        self.screen = pygame.display.set_mode((640, 480))

        # The function Surface generates an empty surface(image)
        # Render on this smaller display, later we scale it up to fit in the screen above
        self.display = pygame.Surface((320, 240))

        # Creates the clock so we can change the game fps
        self.clock = pygame.time.Clock()

        # Movement
        self.movement = [False, False]

        # Loading the images
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),

        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        # Setting the player
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        # Setting the tilemap (Getting its value from the script and assigning it into self.tilemap)
        self.tilemap = Tilemap(self, tile_size = 16)

        # Starts the camera at the position 0, 0
        # The idea of a camera is just to move everything else in the scene
        self.scroll = [0, 0]


    def run(self):
        # Creates the game loop
        while True:
            # Adds the background
            self.display.blit(self.assets['background'], (0, 0))

            # Makes the camera follow the player.
            # The camera starts on the top left of the screen, so if we put the camera directly
            # into the player's position, the player would be on the top left.
            # This way we put the player at the center of the screen.
            # Diving by 30 makes the movement smoother
            # Everything inside the () represents how far away the camera is from where we want it to be, 
            # and then we add it all to the camera pos.
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

            # To deal with subpixels issues converting the float numbers to int
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            # True converts to 1 and False converts to 0
            # If both are true (holding both down) this adds up to 0
            # Y parameter is 0 because we only move sideways on platform
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            # Shows the player
            self.player.render(self.display, offset=render_scroll)

            # Gets the input
            # "event" is a click on the mouse, a key press, etc
            for event in pygame.event.get():
                # Closes the game (pressing the X)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # If a key is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        # [0] = x
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        # [1] = y
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                # If a key is released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            # Blits the display onto the screen and scales it up to fit the same size
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Updates the screen
            pygame.display.update()
            # Sets the fps to 60
            self.clock.tick(60)

# Initializing the game
Game().run()
