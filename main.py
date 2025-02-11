# Sources: https://www.geeksforgeeks.org/how-to-make-flappy-bird-game-in-pygame/

import random
import sys
import pygame
from pygame.locals import *

# Initialize pygame
pygame.init()

# Game Variables
window_width = 600
window_height = 499
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('KDappy Bird Game')

elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = 'dagger.png'
background_image = 'KDackground.png'
birdplayer_image = 'bird.png'
sealevel_image = 'white.png'

def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    return [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True
    for pipe in up_pipes:
        if vertical < pipe['y'] + game_images['pipeimage'][0].get_height() and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    for pipe in down_pipes:
        if vertical + game_images['flappybird'].get_height() > pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False

def flappygame():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    mytempheight = 100
    
    first_pipe = createPipe()
    second_pipe = createPipe()
    
    down_pipes = [{'x': window_width + 300 - mytempheight, 'y': first_pipe[1]['y']},
                  {'x': window_width + 300 - mytempheight + (window_width / 2), 'y': second_pipe[1]['y']}]
    up_pipes = [{'x': window_width + 300 - mytempheight, 'y': first_pipe[0]['y']},
                {'x': window_width + 200 - mytempheight + (window_width / 2), 'y': second_pipe[0]['y']}]
    
    pipeVelX = -4
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    birdAccY = 1
    bird_flap_velocity = -8
    bird_flapped = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        if isGameOver(horizontal, vertical, up_pipes, down_pipes):
            return

        playerMidPos = horizontal + game_images['flappybird'].get_width() // 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() // 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Your score is {your_score}")
        
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
        if bird_flapped:
            bird_flapped = False
        
        playerHeight = game_images['flappybird'].get_height()
        vertical = max(0, min(vertical + bird_velocity_y, elevation - playerHeight))
        
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
        
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
        
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1], (lowerPipe['x'], lowerPipe['y']))
        window.blit(game_images['sea_level'], (0, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))
        
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)

# Load images
framepersecond_clock = pygame.time.Clock()
game_images['scoreimages'] = (
    pygame.image.load('0.png').convert_alpha(),
    pygame.image.load('1.png').convert_alpha(),
    pygame.image.load('2.png').convert_alpha(),
    pygame.image.load('3.png').convert_alpha(),
    pygame.image.load('4.png').convert_alpha(),
    pygame.image.load('5.png').convert_alpha(),
    pygame.image.load('6.png').convert_alpha(),
    pygame.image.load('7.png').convert_alpha(),
    pygame.image.load('8.png').convert_alpha(),
    pygame.image.load('9.png').convert_alpha()
)
game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
game_images['background'] = pygame.image.load(background_image).convert_alpha()
game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                            pygame.image.load(pipeimage).convert_alpha())

print("WELCOME TO THE KDAPPY BEAR GAME")
print("Press space or enter to start the game")

while True:
    horizontal = int(window_width / 5)
    vertical = int((window_height - game_images['flappybird'].get_height()) / 2)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappygame()
            else:
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['flappybird'], (horizontal, vertical))
                window.blit(game_images['sea_level'], (0, elevation))
                pygame.display.update()
                framepersecond_clock.tick(framepersecond)