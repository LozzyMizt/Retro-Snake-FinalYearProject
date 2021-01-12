import PyGameSnakeNN as retro_snake
import argparse
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import Adam
import numpy as np
import random
import json
from random import sample as rsample
import time



INPUT_SHAPE = (80, 80, 2)  # Shape of the image imported into the NN
NB_ACTIONS = 5  # NB_ACTIONS is the number of actions the player can do
BATCH = 100
GAME_INPUT = [0, 1, 2, 3, 4]
EPSILON = 1
EPSILON_DECAY = 0.99
FINAL_EPSILON = 0.3
LEARNING_RATE = 1e-4
GAMMA = 0.7
NB_FRAMES = 1

def build_model():

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(8, 8), strides=(4, 4), activation='relu',
                     input_shape=(30, 30, 4)))
    model.add(MaxPooling2D(pool_size=(4, 4), strides=(2, 2), padding='same'))
    model.add(Conv2D(64, kernel_size=(4, 4), strides=(2, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1), padding='same'))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(NB_ACTIONS))
    # I chose to use a Adam optimizer, I have used it before with good results
    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss="mean_squared_error", optimizer=adam)
    print(model.summary())
    return model


def experience_replay(batch_size):
    memory = []
    while True:
        experience = (
            yield rsample(memory, batch_size) if batch_size <= len(memory) else None
        )
        memory.append(experience)



def nn_loadOld_weights(model):
    print("Now we load weight")
    model.load_weights("model.h5")
    print("Weight load successfully")
    print("Let the training begin!")
    train_network(model)


def stack_image(x_t1_colored):
    pass


def train_network(model):
    epsilon = EPSILON
    game_state = retro_snake.gameLoop()  # Starting up a game
    game_state.set_start_state()
    game_image, score, game_lost = game_state.run(
        0
    )  # The game is started but no action is performed
    s_t = stack_image(game_image)
    terminal = False
    t = 0
    exp_replay = experience_replay(BATCH)
    exp_replay.__next__()  # Start experience replay coroutine
    while True:
        loss = 0
        Q_sa = 0
        action_index = 4
        r_t = 0
        a_t = "no nothing"
        if terminal:
            game_state.set_start_state()
        if t % NB_FRAMES == 0:
            if random.random() <= epsilon:
                action_index = random.randrange(NB_ACTIONS)
                a_t = GAME_INPUT[action_index]
            else:
                action_index = np.argmax(model.predict(s_t))
                a_t = GAME_INPUT[action_index]
        if epsilon > FINAL_EPSILON:
            epsilon = epsilon * EPSILON_DECAY
        else:
            epsilon = FINAL_EPSILON
        # run the selected action and observed next state and reward
        x_t1_colored, r_t, terminal = game_state.run(a_t)
        s_t1 = stack_image(x_t1_colored)
        experience = (s_t, a_t, r_t, s_t1)
        batch = exp_replay.send(experience)
        s_t1 = stack_image(x_t1_colored)
        if batch:
            inputs = np.zeros((BATCH, s_t.shape[1], s_t.shape[2], s_t.shape[3]))
            targets = np.zeros((BATCH, NB_ACTIONS))
            i = 0
            for s, a, r, s_pred in batch:
                inputs[i : i + 1] = s
                if r < 0:
                    targets[i, a] = r
                else:
                    Q_sa = model.predict(s_pred)
                    targets[i, a] = r + GAMMA * np.max(Q_sa)
                i += 1
            loss += model.train_on_batch(inputs, targets)
            # Exploration vs Exploitation

        t += 1
        # save progress every 10000 iterations
        if t % 1000 == 0:
            print("Now we save model")
            model.save_weights("model.h5", overwrite=True)
            with open("model.json", "w") as outfile:
                json.dump(model.to_json(), outfile)

        if t % 500 == 0:
            print(
                "TIMESTEP",
                t,
                "/ EPSILON",
                epsilon,
                "/ ACTION",
                action_index,
                "/ REWARD",
                r_t,
                "/ Q_MAX ",
                np.max(Q_sa),
                "/ Loss ",
                loss,
            )

    print("Episode finished!")
    print("************************")


def nn_playGame(model):
    print("Now we load weight")
    model.load_weights("model.h5")
    print("Weight load successfully")
    print("Let the game begin!")
    game_state = retro_snake.gameLoop() # Starting up a game
    game_state.set_start_state()
    game_image, score, game_lost = game_state.run(
        4
    )  # The game is started but no action is performed
    s_t = stack_image(game_image)
    s_t1 = s_t
    a_t = 4
    while True:

        if game_lost:
            print("Game lost")
            time.sleep(2)
            print("Game is restarting")
            game_state.set_start_state()

        action_index = np.argmax(model.predict(s_t1))
        a_t = GAME_INPUT[action_index]
        x_t1_colored, _, terminal = game_state.run(a_t)
        s_t1 = stack_image(x_t1_colored)
        game_lost = terminal


def playGame(args):
    model = build_model()
    if args["mode"] == "Run":
        nn_playGame(model)
    elif args["mode"] == "Re-train":
        nn_loadOld_weights(model)
    elif args["mode"] == "Train":
        train_network(model)
    else:
        print("*** Not valid argument ***")
        print("Run argument for running game with a trained weights")
        print("Re-train argument for continue training model")
        print("Train to train train from scratch")
        print("*********************************")


def main():
    parser = argparse.ArgumentParser(
        description="How you would like your program to run"
    )
    parser.add_argument("-m", "--mode", help="Train / Run / Re-train", required=True)
    args = vars(parser.parse_args())
    playGame(args)


if __name__ == "__main__":
    main()