"""
Global settings and constants for InfernoGame.
Following PEP 8 standards and camelCase naming convention.
"""
import os

# Screen dimensions
screenWidth = 720
screenHeight = 900
frameRate = 60

# Physics constants
gravityValue = 0.8
jumpStrength = -22
playerSpeed = 6

# Platform generation settings
maxPlatforms = 10
platformMinW = 70
platformMaxW = 140
platformHeight = 25

# Separation settings
platformMinYGap = 110
platformMaxYGap = 190
maxJumpDistance = 220

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
fontSizeTitle = 64
fontSizeSubtitle = 36
fontSizeText = 28

# File settings
highScoreFile = "highscores.json"

# Image Assets (Filenames)
# Ensure these files exist in your project folder, or the game will use colors.
bgStartImage = "bg_start.png"
bgGameImage = "bg_game.png"
playerImage = "player.png"
platformImage = "platform.png"
lavaImage = "lava.png" # Optional, can remain a rect