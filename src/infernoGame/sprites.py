import random
import pygame
from settings import *

# Layer Constants
LAYER_PLATFORM = 1
LAYER_ENTITIES = 2
LAYER_LAVA = 3


def trim_image(img, min_height=10):
    """
    Automatic cropping: Removes transparent margins.
    Safety: Prevents creating rects too small for physics.
    """
    try:
        rect = img.get_bounding_rect()
        if rect.height < min_height:
            return img
        return img.subsurface(rect).copy()
    except ValueError:
        return img


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = LAYER_ENTITIES
        super().__init__()
        self.game = game

        if self.game.playerImg:
            raw_walk = pygame.transform.scale(self.game.playerImg, (40, 50))
            self.walk_img = trim_image(raw_walk)
            self.walk_img.set_colorkey(colorBlack)
        else:
            self.walk_img = pygame.Surface((30, 40))
            self.walk_img.fill(colorPlayer)

        jump_img_source = getattr(self.game, 'playerJumpImg', None)
        if jump_img_source:
            raw_jump = pygame.transform.scale(jump_img_source, (40, 50))
            self.jump_img = trim_image(raw_jump)
            self.jump_img.set_colorkey(colorBlack)
        else:
            self.jump_img = self.walk_img.copy()

        self.image = self.walk_img
        self.rect = self.image.get_rect()
        self.rect.center = (screenWidth // 2, screenHeight - 150)
        self.mask = pygame.mask.from_surface(self.image)

        self.velocityX = 0
        self.velocityY = 0
        self.onGround = False
        self.facingRight = True

    def update(self):
        self.applyGravity()
        self.handleMovement()
        # Animation is handled in main.py

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        if self.rect.right > screenWidth:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = screenWidth

    def animate(self):
        previous_bottom = self.rect.bottom
        previous_center_x = self.rect.centerx

        if self.onGround:
            current_img = self.walk_img
        else:
            current_img = self.jump_img

        if not self.facingRight:
            current_img = pygame.transform.flip(current_img, True, False)

        self.image = current_img
        self.rect = self.image.get_rect()
        self.rect.bottom = previous_bottom
        self.rect.centerx = previous_center_x
        self.mask = pygame.mask.from_surface(self.image)

    def applyGravity(self):
        self.velocityY += gravityValue
        if self.velocityY > terminalVelocity:
            self.velocityY = terminalVelocity

    def handleMovement(self):
        self.velocityX = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocityX = -playerSpeed
            self.facingRight = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocityX = playerSpeed
            self.facingRight = True

    def jump(self):
        if self.onGround:
            self.velocityY = jumpStrength
            self.onGround = False


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = LAYER_PLATFORM
        super().__init__()
        self.game = game
        if self.game.platformImg:
            self.image = pygame.transform.scale(
                self.game.platformImg, (width, height)
            )
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(colorPlatform)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


class Lava(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = LAYER_LAVA
        super().__init__()
        self.game = game
        if self.game.lavaImg:
            self.image = pygame.transform.scale(
                self.game.lavaImg, (screenWidth, screenHeight * 2)
            )
            self.image.set_alpha(220)
        else:
            self.image = pygame.Surface((screenWidth, screenHeight * 2))
            self.image.fill(colorLava)
            self.image.set_alpha(200)

        self.rect = self.image.get_rect()
        self.rect.top = screenHeight
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= lavaRiseSpeed
        if self.rect.top > screenHeight:
            self.rect.top = screenHeight


# --- ENEMIES ---

class Spike(pygame.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = LAYER_ENTITIES
        super().__init__()
        self.game = game
        self.platform = platform

        if self.game.spikeImg:
            # SIZE: (180, 135)
            raw_img = pygame.transform.scale(self.game.spikeImg, (180, 135))
            self.image = trim_image(raw_img)
        else:
            self.image = pygame.Surface((180, 135), pygame.SRCALPHA)
            pygame.draw.polygon(
                self.image, colorSpike, [(0, 135), (90, 0), (180, 135)]
            )

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        maxOffset = platform.rect.width - self.rect.width
        if maxOffset > 0:
            offset = random.randint(0, int(maxOffset))
        else:
            offset = 0

        # VISUAL FIX: Overlap +35 pixels
        self.rect.bottom = platform.rect.top + 35
        self.rect.x = platform.rect.x + offset

    def update(self):
        if not self.platform.alive():
            self.kill()
            return

        self.rect.bottom = self.platform.rect.top + 35
        self.rect.x = max(
            self.platform.rect.x,
            min(self.rect.x, self.platform.rect.right - self.rect.width)
        )
        if self.rect.top >= screenHeight:
            self.kill()


class PatrolEnemy(pygame.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = LAYER_ENTITIES
        super().__init__()
        self.game = game
        self.platform = platform

        if self.game.enemyPatrolImg:
            # SIZE: (100, 100)
            raw_img = pygame.transform.scale(
                self.game.enemyPatrolImg, (100, 100)
            )
            self.image = trim_image(raw_img)
        else:
            self.image = pygame.Surface((100, 100))
            self.image.fill(colorEnemyPatrol)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # VISUAL FIX: +35 pixels overlap
        self.rect.bottom = platform.rect.top + 35
        self.rect.centerx = platform.rect.centerx

        self.speed = 3
        self.direction = 1

    def update(self):
        if not self.platform.alive():
            self.kill()
            return

        self.rect.x += self.speed * self.direction
        if self.rect.right > self.platform.rect.right:
            self.direction = -1
        if self.rect.left < self.platform.rect.left:
            self.direction = 1

        # Maintain overlap
        self.rect.bottom = self.platform.rect.top + 35

        if self.rect.top >= screenHeight:
            self.kill()


class RangedEnemy(pygame.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = LAYER_ENTITIES
        super().__init__()
        self.game = game
        self.platform = platform

        if self.game.enemyRangedImg:
            raw_img = pygame.transform.scale(
                self.game.enemyRangedImg, (80, 120)
            )
            self.image = trim_image(raw_img)
        else:
            self.image = pygame.Surface((80, 120))
            self.image.fill(colorEnemyRanged)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # VISUAL FIX: +35 pixels overlap
        self.rect.bottom = platform.rect.top + 35

        # POSITION FIX: Move inwards from edges
        margin = platform.rect.width // 6

        if random.choice([True, False]):
            self.rect.centerx = platform.rect.left + margin
            self.shootDir = 1
        else:
            self.rect.centerx = platform.rect.right - margin
            self.shootDir = -1

        self.lastShot = pygame.time.get_ticks()
        self.shootDelay = 2000

    def update(self):
        if not self.platform.alive():
            self.kill()
            return

        # Maintain overlap
        self.rect.bottom = self.platform.rect.top + 35
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay:
            self.lastShot = now
            self.shoot()

        if self.rect.top >= screenHeight:
            self.kill()

    def shoot(self):
        p = Projectile(
            self.game, self.rect.centerx, self.rect.centery, self.shootDir
        )
        self.game.allSprites.add(p)
        self.game.hazards.add(p)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self._layer = LAYER_ENTITIES
        super().__init__()
        self.game = game
        self.speed = 6 * direction

        if self.game.projectileImg:
            raw_img = pygame.transform.scale(self.game.projectileImg, (40, 15))
            self.image = trim_image(raw_img)
        else:
            self.image = pygame.Surface((20, 8))
            self.image.fill(colorProjectile)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += self.speed
        isOffScreen = (
            self.rect.right < 0 or
            self.rect.left > screenWidth or
            self.rect.top > screenHeight
        )
        if isOffScreen:
            self.kill()
