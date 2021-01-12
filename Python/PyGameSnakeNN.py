import gym
import pygame
import time
import random
import numpy as np
import math
from pygame.locals import *

#  ---Neural Network imports--- #
# from keras.optimizers import Adam
# from keras.models import Sequential
# from keras.layers.core import Dense
# from operator import add

pygame.init()

client_W = 600
client_H = 400
dis = pygame.display.set_mode((client_W, client_H))  # Sets the dimensions of the client

pygame.display.set_caption('Snake Game')  # Displays the name on the bar

white = (255, 255, 255)  # Produces the colour white
red = (255, 0, 0)  # Produces the colour red
black = (0, 0, 0)  # Produces the colour black
yellow = (255, 255, 102)  # Produces the colour yellow
green = (0, 200, 0)  # Produces the colour green
light_green = (0, 150, 0)  # Produces the colour green
light_red = (200, 0, 0)  # Produces the colour red

snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("Retro", 50)
score_font = pygame.font.SysFont("Retro", 30)

#  -------------------Neural Network variables -------------------  #
# first_layer = 150  # Neurons in the first layer
# learning_rate = 0.0005
# load_weights = True
# weights = 'weights/weights.hdf5'

class retro_snake():

    # def network():
    #     model = Sequential()
    #     model = add(Dense(output_dim=first_layer, activation='relu', input_dim=11))
    #     model.add(Dense(output_dim=3, activation='softmax'))
    #     opt = Adam(learning_rate)
    #     model.compile(loss='mse', optimizer=opt)
    #
    #     if load_weights:
    #         model.load_weights(weights)
    #     return model

    # Variables for q-learning
    action_space = 20
    observation_space = 20
    goal_position = +1

    def text_obj(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def replay_button(self):
        pygame.draw.rect(dis, green, (150, 200, 100, 50))
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_obj("Replay!", smallText)
        textRect.center = ((150 + (100 / 2)), (200 + (50 / 2)))
        dis.blit(textSurf, textRect)

    def exit_button(self):
        pygame.draw.rect(dis, red, (350, 200, 100, 50))
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_obj("Exit!", smallText)
        textRect.center = ((350 + (100 / 2)), (200 + (50 / 2)))
        dis.blit(textSurf, textRect)

    def text_obj(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def score_count(self, score):
        value = score_font.render("Score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])

    def message(self, msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [client_W / 6, client_H / 4])


    def gameLoop(self):  # Creating a function for the whole Snake Game


        game_over = False
        game_close = False

        x1 = client_W / 2
        y1 = client_H / 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        foodx = round(random.randrange(0, client_W - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, client_H - snake_block) / 10.0) * 10.0

        while not game_over:

            while game_close == True:
                dis.fill(black)
                self.message("Game Over! You Scored: " + str(length_of_snake - 1), red)
                self.replay_button()
                self.exit_button()

                for evento in pygame.event.get():
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[1] >= 200:
                            if pygame.mouse.get_pos()[0] <= 250 and pygame.mouse.get_pos()[1] <= 250:
                                self.gameLoop()
                        if pygame.mouse.get_pos()[0] >= 350 and pygame.mouse.get_pos()[1] >= 200:
                            if pygame.mouse.get_pos()[0] <= 450 and pygame.mouse.get_pos()[1] <= 250:
                                pygame.quit()
                                quit()
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Initialising Quit
                    game_over = True  # Game will close
                if event.type == pygame.KEYDOWN:  # Set Arrow keys as controls
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        x1_change = 0
                        y1_change = -snake_block
                    elif event.key == pygame.K_DOWN:
                        x1_change = 0
                        y1_change = snake_block

            if x1 >= client_W or x1 < 0 or y1 >= client_H or y1 < 0:
                game_close = True


            x1 += x1_change
            y1 += y1_change
            dis.fill(black)

            pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])



            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True


            self.our_snake(snake_block, snake_list)
            self.score_count(length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, client_W - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, client_H - snake_block) / 10.0) * 10.0
                length_of_snake += 1

            clock.tick(snake_speed)


        pygame.quit()
        quit()

rs = retro_snake()
rs.gameLoop()
