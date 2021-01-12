from PyGameSnakeNN import retro_snake
import numpy as np
env = retro_snake
LEARNING_RATE = 0.2  # How quick you want to learn
DISCOUNT = 0.85  # How important you want the agent to learn future actions
EPISODES = 25000  # How many times you want the agent to run
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(np.int))

for episode in range(EPISODES):

    discrete_state = get_discrete_state(env.gameLoop())

    print(discrete_state)

    print(np.argmax(q_table[discrete_state]))

    done = False

    while not done:
        action = np.argmax(q_table[discrete_state])
        new_state, reward, done, _ = env.our_snake(action)

        new_discrete_state = get_discrete_state(new_state)
        print(reward, new_state)
        env.gameLoop()
        if not done:
            max_future_q = np.max(q_table[new_state])
            current_q = q_table[discrete_state + (action, )]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state + (action, )] = new_q
        elif new_state[0] >= env.goal_position:
            q_table[discrete_state + (action, )] = 0

        discrete_state = new_discrete_state

env.close()

