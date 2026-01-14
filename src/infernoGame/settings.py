"""
Global settings and constants for InfernoGame.
Following PEP 8 standards and camelCase naming convention.
"""
import os

# Screen dimensions
screenWidth = 1440
screenHeight = 900
frameRate = 60

# Physics constants
gravityValue = 0.8
jumpStrength = -22
playerSpeed = 8

# Platform generation settings
maxPlatforms = 15
platformMinW = 100
platformMaxW = 220
platformHeight = 30

# Separation settings
platformMinYGap = 100
platformMaxYGap = 180
maxJumpDistance = 350

# Lava settings
lavaRiseSpeed = 0.6

# Color definitions (RGB)
colorBlack = (0, 0, 0)
colorWhite = (255, 255, 255)
colorLava = (255, 69, 0)
colorPlayer = (0, 255, 0)
colorPlatform = (0, 255, 255)
colorSecondaryText = (200, 200, 200)
colorAccent = (255, 215, 0)

# Font settings
fontName = 'arial'
fontSizeTitle = 80
fontSizeSubtitle = 48
fontSizeText = 32

# File settings
# Use absolute path for highscores too
baseDir = os.path.dirname(__file__)
highScoreFile = os.path.join(baseDir, "highscores.json")

# Asset Paths Configuration
# Construct absolute paths to ensure assets are found regardless of execution context
assetsFolder = os.path.join(baseDir, "assets")
imagesFolder = os.path.join(assetsFolder, "images")
soundsFolder = os.path.join(assetsFolder, "sounds")

# Image File Paths
bgStartImage = os.path.join(imagesFolder, "bg_start.png")
bgGameImage = os.path.join(imagesFolder, "bg_game.png")
playerImage = os.path.join(imagesFolder, "player.png")
platformImage = os.path.join(imagesFolder, "platform.png")
lavaImage = os.path.join(imagesFolder, "lava.png")