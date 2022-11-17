#main file where game will be played

import obstacleComponent #import obstacle component
import time #import time

#################################
#INITIALIZE PYGAME#
import pygame 
import sys
import math
import random
pygame.init() 
pygame.font.init()
fps=30
fpsclock=pygame.time.Clock()
window_x = 500
window_y = 800
window = pygame.display.set_mode((window_x,window_y))
pygame.display.set_caption("Flyer")

###############define player attributes
player_width = 75
player_height = 100
player_x = (window_x/2)-(player_width/2) #players start position on x axis
player_y = window_y - (window_y/4) #players start position on y axis
player_left =  player_x 
player_right = player_x + player_width
player_color = (255,255,255)
collision_state = False #True when player collides with obstacle

##start text
font = pygame.font.Font('freesansbold.ttf', 32) 
starttext = font.render('Press Space to Start', True, (255,255,255), (0,0,0))
starttextRect = starttext.get_rect()
starttextRect.center = (window_x/2, window_y/2)
#end text
def determine_end_text():
    global endtext
    global endtextRect
    endtext = font.render('SCORE: ' + str(obstacleComponent.obstacles_cleared*100), True, (255,255,255), (0,0,0))
    endtextRect = endtext.get_rect()
    endtextRect.center = ((window_x/2, window_y/2 -40))  
endtext = font.render('Score: 100', True, (255,255,255), (0,0,0))
endtextRect = endtext.get_rect()
endtextRect.center = ((window_x/2, window_y/2 -40))  
restart_text = font.render('press r to restart', True, (255,255,255), (0,0,0))
restart_text_Rect = restart_text.get_rect()
restart_text_Rect.center = ((window_x/2, window_y/2 +40)) 
#reset_game
def reset_game():
    global player_color
    global player_x
    obstacleComponent.reset_obstacles_cleared() #reset obstacles cleared counter
    obstacleComponent.obstacles_set_start() #reset obstacle positions
    player_color = (255,255,255) #reset player color
    player_x = (window_x/2)-(player_width/2) #reset player position

###############Collision logic
def determine_collision():
    for obstacle in obstacleComponent.obstacles: #for each object in objects
        if (obstacle.get_y() + 20 == player_y): #check if object height = player height
            collision_coordinates = [] #containing all x values of obstacle
            obstacle_left = obstacle.get_x() #left side of obstacle
            obstacle_right = obstacle.get_x() + obstacle.get_width() #right side of obstacle
            while (obstacle_left < obstacle_right): #for each obstacle coordinate from left to right
                collision_coordinates.append(obstacle_left) #add coordinate to collision_coordinates
                obstacle_left += 1 #increment to next coordinate
            for coordinate in collision_coordinates: #for each coordinate in collision coordinates
                player_left = player_x #get players leftmost coordinate
                player_right = player_left + player_width #get players right most coordinate
                if ((coordinate >= player_left) & (coordinate <= player_right)): #if coordinate is > player_left and < player_right
                    #collision had occured
                    global collision_state
                    global player_color
                    player_color = (255, 0, 0) #set player color to red
                    collision_state = True #set collision state to true
                    break #break out of loop once collion is found
            obstacleComponent.increment_obstacles_cleared() #only reachable if an obstacle has been cleared without a collision. increment obstacles cleared
###############player Movement
a_key_down = False #store a key state
d_key_down = False #store d key state
def movePlayer(): 
    moveValue = 0 #move value of -0.5 = left, 0.5 = right
    if a_key_down:
        if (player_x > 0):
            moveValue = -0.5
    if d_key_down:
        if (player_x < (window_x-player_width)):
            moveValue = 0.5
    return moveValue
    
#function for displaying item on screen. Much easier to keep in main than in respective components.
def drawObstacle():
    i = 0 
    for item in obstacleComponent.obstacles: #draw each obstacle
        pygame.draw.rect(window, (0, 0, 255), [obstacleComponent.obstacles[i].get_x(), obstacleComponent.obstacles[i].get_y(), obstacleComponent.obstacles[i].get_width(), obstacleComponent.obstacles[i].get_height()], 0)
        i+=1

#reset game


# Run until the user asks to quit
running = True #holds game running state
in_progress = False #holds in_progress state (true once user decides to start game)

##################Start Game###############
while running:
    #check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                a_key_down = True                 
        if event.type == pygame.KEYUP:            
            if event.key == pygame.K_a:
                a_key_down = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                d_key_down = True                 
        if event.type == pygame.KEYUP:            
            if event.key == pygame.K_d:
                d_key_down = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                in_progress = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if ((in_progress == False) & (collision_state == True)):
                    reset_game()
                    collision_state = False
        
    #check for start game
    if ((in_progress == False) & (collision_state == False)):
        window.fill((0, 0, 0)) #fill background with black
        pygame.draw.rect(window, player_color, [player_x,player_y,player_width,player_height],0) #draw player
        window.blit(starttext, starttextRect) #start game text
    #check for collision, end game screen show    
    elif ((in_progress == False) & (collision_state == True)):
        determine_end_text() #update score with correct score
        window.blit(endtext, endtextRect) #display score
        window.blit(restart_text, restart_text_Rect) #display restart option
    #Game in progress
    else:
        window.fill((0, 0, 0)) # Fill the background with black
        determine_collision() #check for collision
        player_x += movePlayer() #move player
        pygame.draw.rect(window, player_color, [player_x,player_y,player_width,player_height],0) #Draw player
        drawObstacle() #draw all obstacles
        obstacleComponent.moveObstacles() #move obstacles
        obstacleComponent.resetObstacles() #reset obstacles that have reached the bottom
    pygame.display.flip() # Flip the display
    #check for end game
    if((collision_state == True) & (in_progress == True)):
        in_progress = False #pause game play
    
#quit game 
pygame.quit()