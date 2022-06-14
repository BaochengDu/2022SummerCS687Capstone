import re
from shutil import move
import pygame, random
from sys import exit
from pygame.locals import *
from pl_model import *
import random
import sys
import numpy as np

import math
import xlwt
import json

def reset_game():
    ###Reset the game location, initialize

    global is_game_over
    global player_rect
    global player
    global bullet_rect
    global bullet_img
    global enemy_rect
    global enemy_img
    global enemy_explosion_imgs
    global enemies
    global enemies_explosion
    global score
    global shoot_frequency
    global enemy_frequency
    global player_explosion_index
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
def train_update(epsilon, reward):
    ###Select the action with the training status and update the relevant parameters

    global enemies
    global player
    global q_table
    valid_action = ['u', 'd', 'l', 'r']

    state = get_state(enemies, player)

    create_Qtable(state)  # For the current state, retrieve the Q table, if it does not exist, add it to the Q table

    action = random.choice(valid_action) if random.random() < epsilon else max(
        q_table[state], key=q_table[state].get)  # Select Action

    move_plane(player, action)# Move with the given action

    next_state = get_state(enemies, player)  # Get the position of the action after execution

    create_Qtable(next_state)  # For the current next_state, retrieve the Q table, and if it does not exist, add it to the Q table

    update_Qtable(reward, action, state, next_state, gamma, alpha)  # Update Q value in Q table

    update_parameter()  # Update other parameters

    return action, reward

def get_state(enemies, player):
    ###Get the relative coordinates of the aircraft to the nearest enemy aircraft as status

    min_distance = 100000
    state_x = 0
    state_y = 0
    for enemy in enemies.sprites():
        x = player.rect.topleft[0] - enemy.rect.topleft[0]
        y = player.rect.topleft[1] - enemy.rect.topleft[1]
        if y < 0:
            continue
        elif math.sqrt(x * x + y * y) < min_distance:
            min_distance = math.sqrt(x * x + y * y)
            state_x = x
            state_y = y
    return (state_x, state_y)
    
def create_Qtable(state):
        """
        Create a Q table with the current aircraft status；
        If the current state does not exist, add a new column to the Q table
        If the current state already exists, no change will be made
        """
        global q_table
        if state not in q_table:
            q_table[state] = { a: 0.0 for a in ['u', 'd', 'l', 'r']}

def move_plane(player, action):

    ###Move plane
    if action == 'u':
        player.moveUp()
    elif action == 'd':
        player.moveDown()
    elif action == 'l':
        player.moveLeft()
    elif action == 'r':
        player.moveRight()
def update_Qtable(r, action, state, next_state, gamma, alpha):
        """
        Update the Q value in the Q table
        r: Returned reward value
        action: Aircraft selection actions
        state: Current Status
        next_state: The state of the aircraft after performing the action
        gamma： gamma Parameters of Q-learning
        alpha： alpha Parameters of Q-learning
        """
        global q_table
        current_r = q_table[state][action]

        update_r = r + gamma * float(max(q_table[next_state].values()))

        q_table[state][action] += alpha * (update_r - current_r)
def update_parameter():
        """
        Attenuation of the possibility of randomly selected actions
        """
        global t
        global epsilon
        t += 1
        if epsilon < 0.01:
            epsilon = 0.01
        else:
            epsilon -= t * 0.1

        return epsilon

# Set the width of the screen
if __name__ == "__main__":

    q_table = {} 
    epoch = 5000  # Number of training rounds
    epsilon = 0.5  # Initial exploration probability
    alpha = 0.5  # The formula for ⍺
    gamma = 0.9  # The formula for γ
    t = 0   # For attenuate epsilon
    reward = 0.2

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
    is_game_over = False
    clock = pygame.time.Clock()

    # Start the game and set up a loop

    # f = open("score.txt", "w")
    # Create the excel file to be written
    workbook = xlwt.Workbook(encoding='utf-8')       #Create Excel 
    sheet1 = workbook.add_sheet("ceshi")          #create sheet
    sheet1.write(0, 0, "epoch")
    sheet1.write(0, 1, "score")


    for epoch_i in range (2,epoch):
        reset_game()
        while not is_game_over:
            # Set the game frame rate to 60
            clock.tick(60)
            if not is_game_over:
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
                    # Set the location of the enemy aircraft
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
            # Add background image
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
                    reward = 2
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
            score_text = score_font.render("score: " + str(score), True, (128, 128, 128))

            
            # Show current rounds（epoch）
            epoch_i_font = pygame.font.Font(None, 36)
            epoch_i_text = epoch_i_font.render("epoch: " + str(epoch_i), True, (128, 128, 128))

            # Set text
            text_rect = score_text.get_rect()
            # Set the place to put the text
            text_rect.topleft = [20, 10]
            # Set the shown of the score
            screen.blit(score_text, text_rect)

            # Set text
            epoch_i_rect = epoch_i_text.get_rect()
            # Set the place to put the text
            epoch_i_rect.topleft = [300, 10]
            # Set the shown of the score
            screen.blit(epoch_i_text, epoch_i_rect)

            left, middle, right = pygame.mouse.get_pressed()
            # Pause the game
        
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if is_game_over:
                reward = -5
            
            train_update(epsilon, reward)

        ###Write one score per epoch
        sheet1.write(epoch_i, 0, epoch_i)
        sheet1.write(epoch_i, 1, score)

        print("finish")

    ###Save each round score in excel
    workbook.save('score.xlsx')

    ###Save the model, whitch is the q_table learned during Q-learning
    q_table_json = json.dumps({str(q_item): q_table[q_item] for q_item in q_table})
    f = open('q_table.json', 'w')
    f.write(q_table_json)