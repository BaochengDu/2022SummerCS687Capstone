import pygame

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600

# Set the bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        # Set the background area
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.speed = 10
    def move(self):
        self.rect.top -= self.speed

# Set the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, explosion_img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.explosion_img = explosion_img
        self.speed = 2
        # Set up a knockdown sequence
        self.explosion_index = 0
    def move(self):
        # The enemy's bullets can only go all the way down
        self.rect.top += self.speed

# Set the class of player
class Player(pygame.sprite.Sprite):
    def __init__(self, img, rect, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        # Separate the aircraft picture section
        for i in range(len(rect)):
            self.image.append(img.subsurface(rect[i]).convert_alpha())
        # Get the area of the aircraft
        self.rect = rect[0]
        self.rect.topleft = pos
        self.speed = 8
        # Generate a sprite group example
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        # Determine if an aircraft has been hit
        self.is_hit = False
        self.reward = {
            "live": 0.2,
            "kick": 2,
            "down": -5
        }
    def shoot(self, img):
        bullet = Bullet(img, self.rect.midtop)
        # Add bullet instances to the player's bullet group
        self.bullets.add(bullet)
    def moveUp(self):
        # When the top is encountered, set the upper top to 0
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed
    def moveDown(self):
        # When the bottom is encountered, the setting is always constant
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed
    def moveLeft(self):
        # When encountering the left side, keep stopping on the left side
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed
    def moveRight(self):
        # When encountering the right side, stop to the right
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed
