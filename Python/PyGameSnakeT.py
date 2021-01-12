import pygame
import time
import random

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


# first_layer = 150  # Neurons in the first layer
# learning_rate = 0.0005
# load_weights = True
# weights = 'weights/weights.hdf5'
#
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


def text_obj(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def replay_button():
    pygame.draw.rect(dis, green, (150, 200, 100, 50))
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_obj("Replay!", smallText)
    textRect.center = ((150 + (100 / 2)), (200 + (50 / 2)))
    dis.blit(textSurf, textRect)


def exit_button():
    pygame.draw.rect(dis, red, (350, 200, 100, 50))
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_obj("Exit!", smallText)
    textRect.center = ((350 + (100 / 2)), (200 + (50 / 2)))
    dis.blit(textSurf, textRect)


def text_obj(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def score_count(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [client_W / 6, client_H / 4])


def client_replay():
    gameLoop()


def client_exit(self):
    exit()


def gameLoop():  # Creating a function for the whole Snake Game
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
            message("Game Over! You Scored: " + str(length_of_snake - 1), red)
            replay_button()
            exit_button()

            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[1] >= 200:
                        if pygame.mouse.get_pos()[0] <= 250 and pygame.mouse.get_pos()[1] <= 250:
                            gameLoop()
                    if pygame.mouse.get_pos()[0] >= 350 and pygame.mouse.get_pos()[1] >= 200:
                        if pygame.mouse.get_pos()[0] <= 450 and pygame.mouse.get_pos()[1] <= 250:
                            pygame.quit()
                            quit()
            pygame.display.update()

        #  Non-Smart AI - moves the snake depending on the random INT given
        for random_number in range(1):  # For loop to pick a number between 0-3
            random_number = random.randint(0, 3)
            print(random_number)
            #  Chosen number determines the direction of the Snake.
            if random_number == 0:
                x1_change = 0
                y1_change = -snake_block
                continue
            elif random_number == 1:
                x1_change = -snake_block
                y1_change = 0
                continue
            elif random_number == 2:
                x1_change = snake_block
                y1_change = 0
                continue
            elif random_number == 3:
                x1_change = 0
                y1_change = snake_block
                continue

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

        our_snake(snake_block, snake_list)
        score_count(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, client_W - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, client_H - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()



gameLoop()
