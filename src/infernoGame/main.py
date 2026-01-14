import pygame
import sys
from settings import *
from sprites import Player, Platform


class InfernoGame:
    """
    Main game engine class. Manages the loop, rendering, and events.
    """

    def __init__(self):
        """
        Initialize pygame, display, and game objects.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("InfernoGame - Escape the Depths")
        self.clock = pygame.time.Clock()
        self.isRunning = True

        # Initialize sprite groups
        self.allSprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        self.setupGame()

    def setupGame(self):
        """
        Creates initial game objects like the player and starting platforms.
        """
        self.player = Player()
        self.allSprites.add(self.player)

        # Create a base platform for the start
        basePlatform = Platform(0, screenHeight - 10, screenWidth, 10)
        self.allSprites.add(basePlatform)
        self.platforms.add(basePlatform)

    def run(self):
        """
        Starts the main execution loop.
        """
        while self.isRunning:
            self.handleEvents()
            self.updateLogic()
            self.drawScene()
            self.clock.tick(frameRate)

        pygame.quit()
        sys.exit()

    def handleEvents(self):
        """
        Polls for keyboard and system events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def updateLogic(self):
        """
        Handles collisions and object updates.
        """
        self.allSprites.update()

        # Check for collisions between player and platforms
        if self.player.velocityY > 0:
            hits = pygame.sprite.spritecollide(
                self.player, self.platforms, False
            )
            if hits:
                # Snap to the top of the platform
                self.player.rect.bottom = hits[0].rect.top
                self.player.velocityY = 0

    def drawScene(self):
        """
        Clears the screen and draws the updated frame.
        """
        self.screen.fill(colorBlack)

        # Draw all managed sprites
        self.allSprites.draw(self.screen)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    # Create the game instance and launch
    gameInstance = InfernoGame()
    gameInstance.run()
