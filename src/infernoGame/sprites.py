import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    """
    Main character class responsible for movement and physics.
    """

    def __init__(self, game):
        super().__init__()
        self.game = game  # Reference to the main game to access assets
        
        # Use image if available, else fallback to color
        if self.game.playerImg:
            self.image = pygame.transform.scale(self.game.playerImg, (40, 50))
            # Removing the black background from the image (transparency)
            self.image.set_colorkey(colorBlack) 
        else:
            self.image = pygame.Surface((30, 40))
            self.image.fill(colorPlayer)
            
        self.rect = self.image.get_rect()

        # Initial position
        self.rect.center = (screenWidth // 2, screenHeight - 150)

        # Movement state
        self.velocityX = 0
        self.velocityY = 0
        self.onGround = False

    def update(self):
        """
        Calculates position changes for the current frame.
        """
        self.applyGravity()
        self.handleMovement()

        # Update position coordinates
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        # Screen wrapping
        if self.rect.right > screenWidth:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = screenWidth

    def applyGravity(self):
        self.velocityY += gravityValue

    def handleMovement(self):
        self.velocityX = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocityX = -playerSpeed
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocityX = playerSpeed

    def jump(self):
        if self.onGround:
            self.velocityY = jumpStrength
            self.onGround = False


class Platform(pygame.sprite.Sprite):
    """
    Static platforms that the player can jump on.
    """

    def __init__(self, game, x, y, width, height):
        super().__init__()
        self.game = game
        
        if self.game.platformImg:
            self.image = pygame.transform.scale(self.game.platformImg, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(colorPlatform)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Lava(pygame.sprite.Sprite):
    """
    Deadly rising entity that chases the player.
    """
    def __init__(self, game):
        super().__init__()
        self.game = game
        
        self.image = pygame.Surface((screenWidth, screenHeight * 2))
        self.image.fill(colorLava)
        # Optional: Add simple transparency to see through lava slightly
        self.image.set_alpha(200) 
        
        self.rect = self.image.get_rect()
        self.rect.top = screenHeight + 50 

    def update(self):
        self.rect.y -= lavaRiseSpeed