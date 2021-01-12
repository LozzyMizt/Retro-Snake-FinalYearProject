import pygame
import time
import random
from pygame import mixer
from pygame.locals import *

pygame.init()

client_W = 600
client_H = 420
display = pygame.display.set_mode((client_W, client_H))  # Sets the dimensions of the client

#  Background image
background = pygame.image.load('RetroSnakeBG.jpg')
gameoverscreen = pygame.image.load('GameOver.jpg')
play = pygame.image.load('Play.jpg')
exit = pygame.image.load('Exit.jpg')
playagain = pygame.image.load('PlayAgain.jpg')

pygame.display.set_caption('Retro Snake!')  # Displays the name on the bar

white = (255, 255, 255)  # Produces the colour white
red = (255, 0, 0)  # Produces the colour red
black = (0, 0, 0)  # Produces the colour black
yellow = (255, 255, 102)  # Produces the colour yellow
green = (0, 200, 0)  # Produces the colour green
light_green = (0, 150, 0)  # Produces the colour green
light_red = (200, 0, 0)  # Produces the colour red
grey = (128, 128, 128)  # Produces the colour grey

snake_block = 10
snake_speed = 30

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("Retro", 50)
score_font = pygame.font.SysFont("Retro", 30)


class retro_snake():

    #  Background music
    def backgrounmusic(self):
        mixer.music.load('RetroBG.mp3')
        mixer.music.play(-1)
        mixer.music.set_volume(0.3)


    def text_obj(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()


    def start_button(self):
        display.blit(play, (150, 200))

    def replay_button(self):
        display.blit(playagain, (150, 200))

    def exit_button(self):
        display.blit(exit, (350, 200))

    def text_obj(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def score_count(self, score):
        value = score_font.render("Score: " + str(score), True, yellow)
        display.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(display, white, [x[0], x[1], snake_block, snake_block])

    def message(self, msg, color):
        mesg = font_style.render(msg, True, color)
        display.blit(mesg, [client_W / 1.33, client_H / 3.1])




    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill(white)
            display.blit(background, (0, 0))  # Display the background image
            self.start_button()  # Display the start button
            self.exit_button()  # Display the exit button

            pygame.display.update()
            clock.tick(60)

            # Making interactive buttons
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

    def gameLoop(self):  # Creating a function for the whole Snake Game
        global updatedspeed
        game_over = False
        game_close = False
        mixer.music.unpause()


        x1 = client_W / 2
        y1 = client_H / 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        # Random positioning of the food
        foodx = round(random.randrange(0, client_W - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(20, client_H - snake_block) / 10.0) * 10.0

        while not game_over:

            while game_close == True:
                mixer.music.pause()
                display.fill(black)
                display.blit(gameoverscreen, (0, 0))  # Load Game Over background image
                self.message(str(length_of_snake - 1), white)  # End of Game score
                self.replay_button()  # Load the play again button
                self.exit_button()  # Load the exit button

                # Make the location of the buttons interactive with commands
                for evento in pygame.event.get():
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[1] >= 200:
                            if pygame.mouse.get_pos()[0] <= 300 and pygame.mouse.get_pos()[1] <= 250:
                                self.gameLoop()  # Load the game
                        if pygame.mouse.get_pos()[0] >= 350 and pygame.mouse.get_pos()[1] >= 200:
                            if pygame.mouse.get_pos()[0] <= 450 and pygame.mouse.get_pos()[1] <= 250:
                                pygame.quit()
                                quit()  # Exit game
                pygame.display.update()


            # Snake Movement
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

            # If the Snake collides with the border
            if x1 >= client_W or x1 < 0 or y1 >= client_H or y1 < 20:
                game_close = True
                gameover_sound = mixer.Sound('GameOverFX.ogg')  # Play sound when game is over
                gameover_sound.play()
                gameover_sound.set_volume(0.5)

            x1 += x1_change
            y1 += y1_change
            display.fill(black)

            # Creates the food and spawns it in a random location using foodx and foody
            pygame.draw.rect(display, red, [foodx, foody, snake_block, snake_block])

            # Creates a border
            pygame.draw.rect(display, grey, (-5, 20, 620, 410), 3)

            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            # Game over if the Snake hits itself
            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True
                    gameover_sound = mixer.Sound('GameOverFX.ogg')  # Play sound when game is over
                    gameover_sound.play()
                    gameover_sound.set_volume(0.5)

            self.our_snake(snake_block, snake_list)
            self.score_count(length_of_snake - 1)


            pygame.display.update()

            # Collision between the Snake and the Food
            if x1 == foodx and y1 == foody:
                eating_sound = mixer.Sound('PointFX.ogg')  # Play sound when the Snake makes contact with the food
                eating_sound.play()
                eating_sound.set_volume(0.5)
                foodx = round(random.randrange(0, client_W - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(20, client_H - snake_block) / 10.0) * 10.0
                length_of_snake += 1


            clock.tick(snake_speed)

        pygame.quit()
        quit()




rs = retro_snake()
rs.backgrounmusic()  # Play Background music
rs.game_intro()  # Load Main Menu first
rs.gameLoop()
