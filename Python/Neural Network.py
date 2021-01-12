import numpy as np
from tflearn import DNN
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression

from PyGameSnakeNN import retro_snake

# Create the Network
network = input_data(shape=[None, 5, 1], name='input')
network = fully_connected(network, 25, activation='relu')
network = fully_connected(network, 1, activation='linear')
network = regression(network, optimizer='adam', learning_rate=1e-2, loss='mean_square', name='target')

# Create the model
model = DNN(network, tensorboard_dir='log')

# Load training data
X = np.array([i[0] for i in x]).reshape(-1, 5, 1)
Y = np.array([i[0] for i in y]).reshape(-1, 1)

# train the NN
NN_filename = "model.h5"
model.fit(X, Y, n_epoch=3, shuffle=True, run_id=NN_filename)

# load trained model
model.load("model.h5", weights_only=True)

# Let the NN play a game
s2 = retro_snake(gui=True) # retro_snake is a class which contains the Snake game
input_vect, output_vect = s2.play(testNN=True, _model=model) # Play method runs the game with trained NN model


