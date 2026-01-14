import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    """
    Main character class responsible for movement and physics.
    """

    def __init__(self):
        super().__init__()
        # Create a placeholder surface for the player
        self.image = pygame.Surface((30, 40))
        self.image.fill(colorPlayer)
        self.rect = self.image.get_rect()

        # Initial position
        self.rect.center = (screenWidth // 2, screenHeight - 50)

        # Movement state
        self.velocityX = 0
        self.velocityY = 0

    def update(self):
        """
        Calculates position changes for the current frame.
        """
        self.applyGravity()
        self.handleMovement()

        # Update position coordinates
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        # Basic boundary check for the floor
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
            self.velocityY = 0

    def applyGravity(self):
        """
        Increments downward velocity based on global gravity settings.
        """
        self.velocityY += gravityValue

    def handleMovement(self):
        """
        Reads keyboard input to set horizontal velocity.
        """
        self.velocityX = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.velocityX = -playerSpeed
        if keys[pygame.K_RIGHT]:
            self.velocityX = playerSpeed

    def jump(self):
        """
        Trigger a jump if the player is grounded.
        """
        # Simple check for the prototype: only jump if velocity is zero
        if self.velocityY == 0:
            self.velocityY = jumpStrength


class Platform(pygame.sprite.Sprite):
    """
    Static platforms that the player can jump on.
    """

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(colorPlatform)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
