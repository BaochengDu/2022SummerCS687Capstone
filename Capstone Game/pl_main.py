import pygame, random
from sys import exit
from pygame.locals import *
from pl_model import *
import random
import sys
from utils import *


# def writePrint():
#     output_content = open("a.txt")
#     sys.stdout = output_content
# Set the width of the screen
SCREEN_WIDTH = 450
# Set the height of the screen
SCREEN_HEIGHT = 600
# Initialize window
pygame.init()
# Set window title
pygame.display.set_caption("bullet curtain game")
# Set the screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Hide Mouse
pygame.mouse.set_visible(False)
# Set background image
bg = pygame.image.load("resources/image/bg.png")
# Set the game over image
bg_game_over = pygame.image.load("resources/image/bg_game_over.png")
# Loading Aircraft Resources Pictures
img_plane = pygame.image.load("resources/image/shoot.png")
img_start = pygame.image.load("resources/image/start.png")
img_pause = pygame.image.load("resources/image/pause.png")
img_icon = pygame.image.load("resources/image/plane.png").convert_alpha()

pygame.display.set_icon(img_icon)
# Initialize aircraft area
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
# Player wiped out image
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
# Initialization Location
player_pos = [200, 450]
# Generate Player Classes
player = Player(img_plane, player_rect, player_pos)
# Set the effective range of the bullet
bullet_rect = pygame.Rect(1004, 987, 9, 21)
# Loading bullet pictures
bullet_img = pygame.image.load("resources/image/bullet.png")
# Set the effective range of the enemy
enemy_rect = pygame.Rect(534, 612, 57, 43)
# Set enemy picture
enemy_img = img_plane.subsurface(enemy_rect)
# Set the image of the enemy being defeated
enemy_explosion_imgs = []
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(930, 697, 57, 43)))
# Set up the enemy sprite group
enemies = pygame.sprite.Group()
# Set enemy aircraft to be hit by sprite group
enemies_explosion = pygame.sprite.Group()
# Set firing frequency
shoot_frequency = 0
# Set enemy aircraft frequency
enemy_frequency = 0
# Set image order
player_explosion_index = 16
score = 0
running = True
is_pause = False
is_game_over = False
clock = pygame.time.Clock()

# Start the game and set up a loop
while running:
    # Set the game frame rate to 60
    clock.tick(60)
    if not is_pause and not is_game_over:
        if not player.is_hit:
            # Set continuous fire, because 60 frames per second, 15/60 = 0.25 seconds to fire a bullet
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            # When the set firing frequency is greater than 15, set to 0
            if shoot_frequency >= 15:
                shoot_frequency = 0
        # Control the frequency of generating enemy aircraft
        if enemy_frequency % 50 == 0:
            # Set the enmy random place
            enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_rect.width), 0]
            enemy = Enemy(enemy_img, enemy_explosion_imgs, enemy_pos)
            enemies.add(enemy)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0
        # Control of bullet display operation
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        # Control the operation of enemy aircraft
        for enemy in enemies:
            enemy.move()
            # Determine if an enemy aircraft collides with the player's aircraft
            if pygame.sprite.collide_circle(enemy, player):
                enemies_explosion.add(enemy)
                enemies.remove(enemy)
                player.is_hit = True
                # Set the player's plane to be destroyed
                is_game_over = True
            # Determine if enemy aircraft are in the windows
            if enemy.rect.top < 0:
                enemies.remove(enemy)
        # Set the enemy aircraft to return the instance of the hit enemy aircraft when it touches the player's aircraft bullets
        enemy_explosion = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
        for enemy in enemy_explosion:
            enemies_explosion.add(enemy)
    # Drawing screen
    screen.fill(0)
    # Load background image
    screen.blit(bg, (0, 0))
    # Add player image into the window
    if not player.is_hit:
        screen.blit(player.image[int(player.img_index)], player.rect)
        player.img_index = shoot_frequency / 8
    else:
        if player_explosion_index > 47:
            is_game_over = True
        else:
            player.img_index = player_explosion_index / 8
            screen.blit(player.image[int(player.img_index)], player.rect)
            player_explosion_index += 1
    # The effect of enemy hit by bullet is shown
    for enemy in enemies_explosion:
        if enemy.explosion_index == 0:
            pass
        if enemy.explosion_index > 7:
            enemies_explosion.remove(enemy)
            score += 100
            continue
        # 
        screen.blit(enemy.explosion_img[int(enemy.explosion_index / 2)], enemy.rect)
        enemy.explosion_index += 1
    # Show the bullets
    player.bullets.draw(screen)
    # Show the enemy
    enemies.draw(screen)
    # The display of scores
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    
    # Set text
    text_rect = score_text.get_rect()
    # Set the place to put the text
    text_rect.topleft = [20, 10]
    # Set the shown of the score
    screen.blit(score_text, text_rect)
    left, middle, right = pygame.mouse.get_pressed()
    # Pause the game

    if right == True and not is_game_over:
        is_pause = True
    if left == True:
        # Reset the game
        if is_game_over:
            is_game_over = False
            player_rect = []
            player_rect.append(pygame.Rect(0, 99, 102, 126))
            player_rect.append(pygame.Rect(165, 360, 102, 126))
            player_rect.append(pygame.Rect(165, 234, 102, 126))
            player_rect.append(pygame.Rect(330, 624, 102, 126))
            player_rect.append(pygame.Rect(330, 498, 102, 126))
            player_rect.append(pygame.Rect(432, 624, 102, 126))
            player = Player(img_plane, player_rect, player_pos)
            bullet_rect = pygame.Rect(1004, 987, 9, 21)
            bullet_img = img_plane.subsurface(bullet_rect)
            enemy_rect = pygame.Rect(534, 612, 57, 43)
            enemy_img = img_plane.subsurface(enemy_rect)
            enemy_explosion_imgs = []
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 347, 57, 43)))
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(873, 697, 57, 43)))
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 296, 57, 43)))
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(930, 697, 57, 43)))
            enemies = pygame.sprite.Group()
            enemies_explosion = pygame.sprite.Group()
            score = 0
            shoot_frequency = 0
            enemy_frequency = 0
            player_explosion_index = 16
        
            
            
        # Contune the game
        if is_pause:
            is_pause = False
    # End the game
    if is_game_over:

        font = pygame.font.SysFont("Verdana", 48)
        text = font.render("Score: " + str(score), True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 70
        #print("Score: ",str(score))
        # if __name__ == "__main__":
        #     writePrint()
        #     #print(random.randint(1, 20))
        #     print(str(score))
        # Show the display that the game is over
        screen.blit(bg_game_over, (0, 0))
        # Show the score
        screen.blit(text, text_rect)
        font = pygame.font.SysFont("Verdana", 40)
        text = font.render("Press Left Mouse to Restart", True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 150
        screen.blit(text, text_rect)
 
    


    # Refresh the screen
    pygame.display.update()

    # Hand the game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not is_pause and not is_game_over:
        key = pygame.key.get_pressed()
        if key[K_w] or key[K_UP]:
            player.moveUp()
        if key[K_s] or key[K_DOWN]:
            player.moveDown()
        if key[K_a] or key[K_LEFT]:
            player.moveLeft()
        if key[K_d] or key[K_RIGHT]:
            player.moveRight()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # refresh the display

    pygame.display.update()
