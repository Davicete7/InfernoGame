"""
Global settings and constants for InfernoGame.
Following PEP 8 formatting standards with CamelCase naming convention.
"""
import os

# --- Screen Dimensions ---
screenWidth = 1600
screenHeight = 1000
frameRate = 60

# --- Physics Constants ---
gravityValue = 0.8
jumpStrength = -24
playerSpeed = 9
terminalVelocity = 12  # MAX falling speed

# --- Platform Generation Settings ---
maxPlatforms = 10
platformMinW = 300
platformMaxW = 600
platformHeight = 80  # Thickness

# --- Separation Settings ---
platformMinYGap = 220
platformMaxYGap = 340
maxJumpDistance = 600

# --- Lava Settings ---
lavaRiseSpeed = 5

# --- Difficulty Thresholds (Score) ---
difficultyTier1 = 5
difficultyTier2 = 12
difficultyTier3 = 20

# --- Color Definitions (RGB) ---
colorBlack = (0, 0, 0)
colorWhite = (255, 255, 255)
colorLava = (255, 69, 0)
colorPlayer = (0, 255, 0)
colorPlatform = (0, 255, 255)
colorSecondaryText = (200, 200, 200)
colorAccent = (255, 215, 0)

# Enemy Colors
colorSpike = (150, 150, 150)
colorEnemyPatrol = (255, 0, 0)
colorEnemyRanged = (100, 0, 100)
colorProjectile = (255, 255, 0)

# --- Font Settings ---
fontName = 'arial'
fontSizeTitle = 90
fontSizeSubtitle = 54
fontSizeText = 36

# --- File Settings ---
baseDir = os.path.dirname(__file__)
highScoreFile = os.path.join(baseDir, "highscores.json")

# --- Asset Paths Configuration ---
assetsFolder = os.path.join(baseDir, "assets")
imagesFolder = os.path.join(assetsFolder, "images")

bgStartImage = os.path.join(imagesFolder, "bg_start.png")
bgGameImage = os.path.join(imagesFolder, "bg_game.png")
bgGameOverImage = os.path.join(imagesFolder, "bg_gameover.png")
playerImage = os.path.join(imagesFolder, "player.png")
playerJumpImage = os.path.join(imagesFolder, "player_jump.png")
platformImage = os.path.join(imagesFolder, "platform.png")
lavaImage = os.path.join(imagesFolder, "lava.png")

spikeImage = os.path.join(imagesFolder, "spike.png")
enemyPatrolImage = os.path.join(imagesFolder, "enemy_patrol.png")
enemyRangedImage = os.path.join(imagesFolder, "enemy_ranged.png")
projectileImage = os.path.join(imagesFolder, "projectile.png")
