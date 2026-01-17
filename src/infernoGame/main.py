import sys
import json
import os
import random
import pygame

from settings import *
from sprites import (
    Player, Platform, Lava, Spike, PatrolEnemy, RangedEnemy
)


class InfernoGame:
    """
    Main game engine class. Manages the loop, rendering, events, and scoring.
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
        self.fontName = pygame.font.match_font(fontName)

        # Load visual assets (images)
        self.loadAssets()

        # Game state variables
        self.score = 0
        self.playerName = ""
        self.highScores = self.loadHighScores()

        # Initialize sprite groups containers
        # Use LayeredUpdates to respect drawing order (z-index)
        self.allSprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()  # Lava, Spikes, Enemies

    def loadAssets(self):
        """
        Loads images from disk using paths defined in settings.
        If not found, variables are set to None.
        """
        # Backgrounds
        self.bgStartImg = self.loadImage(bgStartImage)
        self.bgGameImg = self.loadImage(bgGameImage)
        self.bgGameOverImg = self.loadImage(bgGameOverImage)

        # Main entities
        self.playerImg = self.loadImage(playerImage)
        self.playerJumpImg = self.loadImage(playerJumpImage)
        self.platformImg = self.loadImage(platformImage)
        self.lavaImg = self.loadImage(lavaImage)

        # Enemy Assets
        self.spikeImg = self.loadImage(spikeImage)
        self.enemyPatrolImg = self.loadImage(enemyPatrolImage)
        self.enemyRangedImg = self.loadImage(enemyRangedImage)
        self.projectileImg = self.loadImage(projectileImage)

        if not os.path.exists(assetsFolder):
            print(f"Warning: The folder '{assetsFolder}' was not found.")

    def loadImage(self, filePath):
        if os.path.exists(filePath):
            try:
                img = pygame.image.load(filePath).convert_alpha()
                return img
            except pygame.error as e:
                print(f"Error loading image: {filePath} - {e}")
        return None

    def loadHighScores(self):
        if not os.path.exists(highScoreFile):
            return []
        try:
            with open(highScoreFile, 'r') as f:
                return json.load(f)
        except (ValueError, IOError):
            return []

    def saveHighScore(self):
        nameToSave = (
            self.playerName if self.playerName.strip() else "Anonymous"
        )
        newEntry = {"name": nameToSave, "score": int(self.score)}
        self.highScores.append(newEntry)
        self.highScores.sort(key=lambda x: x["score"], reverse=True)
        self.highScores = self.highScores[:5]
        try:
            with open(highScoreFile, 'w') as f:
                json.dump(self.highScores, f)
        except IOError:
            print("Error saving high scores.")

    def setupGame(self):
        self.score = 0
        self.allSprites.empty()
        self.platforms.empty()
        self.hazards.empty()

        # Pass 'self' to sprites so they can access loaded assets
        self.player = Player(self)
        self.allSprites.add(self.player)

        # Base platform - FIXED SIZE AND POSITION
        # Updated to use platformHeight (80)
        baseY = screenHeight - platformHeight
        basePlatform = Platform(self, 0, baseY, screenWidth, platformHeight)
        self.allSprites.add(basePlatform)
        self.platforms.add(basePlatform)

        self.lava = Lava(self)
        self.allSprites.add(self.lava)
        self.hazards.add(self.lava)

        for i in range(maxPlatforms):
            self.spawnPlatform()

    def spawnPlatform(self):
        """
        Platform generation + Difficulty Scaling for Enemies
        """
        if len(self.platforms) == 0:
            lastX = screenWidth // 2
            lastY = screenHeight
        else:
            lastPlatform = min(self.platforms, key=lambda p: p.rect.y)
            lastX = lastPlatform.rect.centerx
            lastY = lastPlatform.rect.y

        minX = max(0, lastX - maxJumpDistance)
        maxX = min(screenWidth - platformMaxW, lastX + maxJumpDistance)
        width = random.randrange(platformMinW, platformMaxW)

        if maxX + width > screenWidth:
            maxX = screenWidth - width
        if minX > maxX:
            minX = max(0, screenWidth // 2 - maxJumpDistance)
            maxX = min(screenWidth - width, screenWidth // 2 + maxJumpDistance)

        x = random.randint(int(minX), int(maxX))
        y = lastY - random.randrange(platformMinYGap, platformMaxYGap)

        newPlatform = Platform(self, x, y, width, platformHeight)
        self.allSprites.add(newPlatform)
        self.platforms.add(newPlatform)

        # --- DIFFICULTY & ENEMY SPAWNING ---
        self.spawnEnemy(newPlatform)

    def spawnEnemy(self, platform):
        """
        Decides if an enemy spawns on the platform based on current Score.
        """
        roll = random.random()  # 0.0 to 1.0

        # Phase 1: Spikes Only
        if difficultyTier1 <= self.score < difficultyTier2:
            if roll < 0.5:
                spike = Spike(self, platform)
                self.allSprites.add(spike)
                self.hazards.add(spike)

        # Phase 2: Spikes + Patrol
        elif difficultyTier2 <= self.score < difficultyTier3:
            if roll < 0.3:
                spike = Spike(self, platform)
                self.allSprites.add(spike)
                self.hazards.add(spike)
            elif roll < 0.6:
                patrol = PatrolEnemy(self, platform)
                self.allSprites.add(patrol)
                self.hazards.add(patrol)

        # Phase 3: Total Chaos
        elif self.score >= difficultyTier3:
            if roll < 0.2:
                spike = Spike(self, platform)
                self.allSprites.add(spike)
                self.hazards.add(spike)
            elif roll < 0.5:
                patrol = PatrolEnemy(self, platform)
                self.allSprites.add(patrol)
                self.hazards.add(patrol)
            elif roll < 0.8:
                ranged = RangedEnemy(self, platform)
                self.allSprites.add(ranged)
                self.hazards.add(ranged)

    def drawText(self, text, size, color, x, y, align="center"):
        try:
            font = pygame.font.Font(self.fontName, size)
        except TypeError:
            font = pygame.font.SysFont(fontName, size)
        textSurface = font.render(str(text), True, color)
        textRect = textSurface.get_rect()
        if align == "center":
            textRect.midtop = (x, y)
        elif align == "left":
            textRect.topleft = (x, y)
        elif align == "right":
            textRect.topright = (x, y)
        self.screen.blit(textSurface, textRect)

    def showStartScreen(self):
        waiting = True
        self.playerName = ""
        while waiting:
            self.clock.tick(frameRate)
            if self.bgStartImg:
                scaledBg = pygame.transform.scale(
                    self.bgStartImg, (screenWidth, screenHeight)
                )
                self.screen.blit(scaledBg, (0, 0))
            else:
                self.screen.fill(colorBlack)

            self.drawText(
                "InfernoGame", fontSizeTitle, colorLava, screenWidth / 2, 100
            )
            self.drawText(
                "Escape the Depths", fontSizeSubtitle,
                colorWhite, screenWidth / 2, 200
            )
            self.drawText(
                "TOP PLAYERS", fontSizeText, colorAccent, screenWidth / 2, 320
            )

            yPos = 380
            if not self.highScores:
                self.drawText(
                    "No scores yet!", fontSizeText,
                    colorSecondaryText, screenWidth / 2, yPos
                )
            else:
                for idx, entry in enumerate(self.highScores):
                    scoreText = (f"{idx + 1}. "
                                 f"{entry['name']} - {entry['score']}")
                    self.drawText(
                        scoreText, fontSizeText,
                        colorWhite, screenWidth / 2, yPos
                    )
                    yPos += 40

            inputY = screenHeight - 300
            self.drawText(
                "ENTER YOUR NAME:", fontSizeSubtitle,
                colorPlatform, screenWidth / 2, inputY
            )
            cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            self.drawText(
                self.playerName + cursor, fontSizeSubtitle,
                colorWhite, screenWidth / 2, inputY + 60
            )
            self.drawText(
                "WASD / Arrows to move, SPACE to jump", fontSizeText,
                colorSecondaryText, screenWidth / 2, screenHeight - 100
            )
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.playerName) > 0:
                            waiting = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.playerName = self.playerName[:-1]
                    else:
                        isPrintable = event.unicode.isprintable()
                        if len(self.playerName) < 15 and isPrintable:
                            self.playerName += event.unicode

    def showGameOverScreen(self):
        if not self.isRunning:
            return
        self.saveHighScore()
        waiting = True
        while waiting:
            self.clock.tick(frameRate)
            if self.bgGameOverImg:
                scaledBg = pygame.transform.scale(
                    self.bgGameOverImg, (screenWidth, screenHeight)
                )
                self.screen.blit(scaledBg, (0, 0))
            elif self.bgGameImg:
                scaledBg = pygame.transform.scale(
                    self.bgGameImg, (screenWidth, screenHeight)
                )
                self.screen.blit(scaledBg, (0, 0))
            else:
                self.screen.fill(colorBlack)

            self.drawText(
                "GAME OVER", fontSizeTitle,
                colorLava, screenWidth / 2, screenHeight / 3
            )
            self.drawText(
                f"Final Score: {int(self.score)}", fontSizeSubtitle,
                colorWhite, screenWidth / 2, screenHeight / 2
            )
            self.drawText(
                "Press SPACE to return to Menu", fontSizeText,
                colorSecondaryText, screenWidth / 2, screenHeight * 3 / 4
            )
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def run(self):
        while self.isRunning:
            self.showStartScreen()
            if not self.isRunning:
                break
            self.setupGame()
            self.isPlaying = True
            while self.isPlaying:
                self.handleEvents()
                self.updateLogic()
                self.drawScene()
                self.clock.tick(frameRate)
            self.showGameOverScreen()
        pygame.quit()
        sys.exit()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isPlaying = False
                self.isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                    self.player.jump()

    def updateLogic(self):
        self.player.onGround = False
        self.allSprites.update()

        # Platform Collisions
        if self.player.velocityY > 0:
            hits = pygame.sprite.spritecollide(
                self.player, self.platforms, False
            )
            if hits:
                lowestHit = None
                for hit in hits:
                    # Check if player feet are above the CENTER of platform.
                    if self.player.rect.bottom < hit.rect.centery:
                        condition = (
                            lowestHit is None or
                            hit.rect.top < lowestHit.rect.top
                        )
                        if condition:
                            lowestHit = hit

                if lowestHit:
                    if self.player.rect.bottom > lowestHit.rect.top:
                        # VISUAL FIX: Sink 35px into the platform
                        self.player.rect.bottom = lowestHit.rect.top + 35
                        self.player.velocityY = 0
                        self.player.onGround = True

        # Hazard Collisions
        hitHazard = pygame.sprite.spritecollide(
            self.player, self.hazards, False, pygame.sprite.collide_mask
        )
        if hitHazard:
            self.isPlaying = False

        # Scrolling
        if self.player.rect.top <= screenHeight / 2:
            scrollSpeed = abs(self.player.velocityY)
            self.player.rect.y += scrollSpeed

            for plat in self.platforms:
                plat.rect.y += scrollSpeed
                if plat.rect.top >= screenHeight:
                    plat.kill()
                    self.score += 1

            self.lava.rect.y += scrollSpeed
            if self.lava.rect.top > screenHeight:
                self.lava.rect.top = screenHeight

            for sprite in self.hazards:
                if isinstance(sprite, (Lava, Spike, PatrolEnemy, RangedEnemy)):
                    pass
                else:
                    sprite.rect.y += scrollSpeed

        while len(self.platforms) < maxPlatforms:
            self.spawnPlatform()

        if self.player.rect.top > screenHeight:
            self.isPlaying = False

        self.player.animate()

    def drawScene(self):
        if self.bgGameImg:
            scaledBg = pygame.transform.scale(
                self.bgGameImg, (screenWidth, screenHeight)
            )
            self.screen.blit(scaledBg, (0, 0))
        else:
            self.screen.fill(colorBlack)
        self.allSprites.draw(self.screen)
        self.drawText(
            f"Score: {int(self.score)}", fontSizeText,
            colorWhite, screenWidth / 2, 20
        )
        pygame.display.flip()


if __name__ == "__main__":
    gameInstance = InfernoGame()
    gameInstance.run()
