import pygame
import sys
import random
import json
import os
from settings import *
from sprites import Player, Platform, Lava


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
        self.allSprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()

    def loadAssets(self):
        """
        Loads images from disk. If not found, variables are set to None.
        """
        self.bgStartImg = self.loadImage(bgStartImage)
        self.bgGameImg = self.loadImage(bgGameImage)
        self.playerImg = self.loadImage(playerImage)
        self.platformImg = self.loadImage(platformImage)
        # Note: bgStartImage etc. must be defined in settings.py

    def loadImage(self, fileName):
        """
        Helper to safely load an image.
        """
        if os.path.exists(fileName):
            try:
                img = pygame.image.load(fileName).convert()
                return img
            except pygame.error:
                print(f"Error loading image: {fileName}")
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
        nameToSave = self.playerName if self.playerName.strip() else "Anonymous"
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

        # Pass 'self' (game instance) to sprites so they can access assets
        self.player = Player(self)
        self.allSprites.add(self.player)

        basePlatform = Platform(self, 0, screenHeight - 60, screenWidth, 40)
        self.allSprites.add(basePlatform)
        self.platforms.add(basePlatform)

        self.lava = Lava(self)
        self.allSprites.add(self.lava)
        self.hazards.add(self.lava)

        for i in range(maxPlatforms):
            self.spawnPlatform()

    def spawnPlatform(self):
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
        
        if maxX + width > screenWidth: maxX = screenWidth - width
        if minX > maxX:
            minX = max(0, screenWidth // 2 - maxJumpDistance)
            maxX = min(screenWidth - width, screenWidth // 2 + maxJumpDistance)

        x = random.randint(int(minX), int(maxX))
        y = lastY - random.randrange(platformMinYGap, platformMaxYGap)

        newPlatform = Platform(self, x, y, width, platformHeight)
        self.allSprites.add(newPlatform)
        self.platforms.add(newPlatform)

    def drawText(self, text, size, color, x, y, align="center"):
        try:
            font = pygame.font.Font(self.fontName, size)
        except TypeError:
            font = pygame.font.SysFont(fontName, size)
        textSurface = font.render(str(text), True, color)
        textRect = textSurface.get_rect()
        if align == "center": textRect.midtop = (x, y)
        elif align == "left": textRect.topleft = (x, y)
        elif align == "right": textRect.topright = (x, y)
        self.screen.blit(textSurface, textRect)

    def showStartScreen(self):
        waiting = True
        self.playerName = ""
        
        while waiting:
            self.clock.tick(frameRate)
            
            # Draw Background if available
            if self.bgStartImg:
                scaledBg = pygame.transform.scale(self.bgStartImg, (screenWidth, screenHeight))
                self.screen.blit(scaledBg, (0, 0))
            else:
                self.screen.fill(colorBlack)
            
            # UI Elements
            self.drawText("InfernoGame", fontSizeTitle, colorLava, screenWidth / 2, 80)
            self.drawText("Escape the Depths", fontSizeSubtitle, colorWhite, screenWidth / 2, 150)
            self.drawText("TOP PLAYERS", fontSizeText, colorAccent, screenWidth / 2, 250)
            
            yPos = 300
            if not self.highScores:
                self.drawText("No scores yet!", fontSizeText, colorSecondaryText, screenWidth / 2, yPos)
            else:
                for idx, entry in enumerate(self.highScores):
                    scoreText = f"{idx + 1}. {entry['name']} - {entry['score']}"
                    self.drawText(scoreText, fontSizeText, colorWhite, screenWidth / 2, yPos)
                    yPos += 35

            inputY = screenHeight - 250
            self.drawText("ENTER YOUR NAME:", fontSizeSubtitle, colorPlatform, screenWidth / 2, inputY)
            cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            self.drawText(self.playerName + cursor, fontSizeSubtitle, colorWhite, screenWidth / 2, inputY + 60)
            self.drawText("WASD / Arrows to move, SPACE to jump", fontSizeText, colorSecondaryText, screenWidth / 2, screenHeight - 100)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.playerName) > 0: waiting = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.playerName = self.playerName[:-1]
                    else:
                        if len(self.playerName) < 12 and event.unicode.isprintable():
                            self.playerName += event.unicode

    def showGameOverScreen(self):
        if not self.isRunning: return
        self.saveHighScore()
        waiting = True
        while waiting:
            self.clock.tick(frameRate)
            
            # Draw game background faintly or black
            if self.bgGameImg:
                self.screen.blit(pygame.transform.scale(self.bgGameImg, (screenWidth, screenHeight)), (0, 0))
            else:
                self.screen.fill(colorBlack)

            self.drawText("GAME OVER", fontSizeTitle, colorLava, screenWidth / 2, screenHeight / 3)
            self.drawText(f"Final Score: {int(self.score)}", fontSizeSubtitle, colorWhite, screenWidth / 2, screenHeight / 2)
            self.drawText("Press SPACE to return to Menu", fontSizeText, colorSecondaryText, screenWidth / 2, screenHeight * 3 / 4)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: waiting = False

    def run(self):
        while self.isRunning:
            self.showStartScreen()
            if not self.isRunning: break
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
        # Reset onGround status each frame
        self.player.onGround = False
        self.allSprites.update()

        # Improved Collision Logic
        if self.player.velocityY > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # Find the lowest platform (highest Y coord) that is below the player's feet
                # Actually we want the platform whose TOP is closest to player's BOTTOM
                # And valid only if we are falling onto it.
                
                lowestHit = None
                for hit in hits:
                    # Tolerance check: 
                    # Did we fall through it this frame? (Previous frame bottom < hit top)
                    # Or are we just slightly inside it?
                    if self.player.rect.bottom < hit.rect.bottom:
                        if lowestHit is None or hit.rect.top < lowestHit.rect.top:
                            lowestHit = hit
                
                if lowestHit:
                    # Snap player to top of platform
                    if self.player.rect.bottom > lowestHit.rect.top:
                        self.player.rect.bottom = lowestHit.rect.top
                        self.player.velocityY = 0
                        self.player.onGround = True

        if pygame.sprite.collide_rect(self.player, self.lava):
            self.isPlaying = False

        if self.player.rect.top <= screenHeight / 4:
            scrollSpeed = abs(self.player.velocityY)
            self.player.rect.y += scrollSpeed
            self.score += scrollSpeed
            for plat in self.platforms:
                plat.rect.y += scrollSpeed
                if plat.rect.top >= screenHeight: plat.kill()
            self.lava.rect.y += scrollSpeed

        while len(self.platforms) < maxPlatforms:
            self.spawnPlatform()

        if self.player.rect.top > screenHeight:
            self.isPlaying = False

    def drawScene(self):
        # Draw Background
        if self.bgGameImg:
            # Simple static background (could be made scrolling later)
            scaledBg = pygame.transform.scale(self.bgGameImg, (screenWidth, screenHeight))
            self.screen.blit(scaledBg, (0, 0))
        else:
            self.screen.fill(colorBlack)
            
        self.allSprites.draw(self.screen)
        self.drawText(f"Score: {int(self.score)}", fontSizeText, colorWhite, screenWidth / 2, 20)
        pygame.display.flip()


if __name__ == "__main__":
    gameInstance = InfernoGame()
    gameInstance.run()