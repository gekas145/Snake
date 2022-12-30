from enviroment import SnakeGame
from wrappers import FrameStack
from utils import neural_net_decision, greedy_decision
from tensorflow import keras
import numpy as np


snake_env = FrameStack(SnakeGame(), 3)
snake_net = keras.models.load_model('snake_net.keras')
rewards = [0]*100
best_seed = None # search for the best seed for replay
best_score = -np.Inf
max_steps = 1000
np.random.seed(145)
seeds = np.random.choice(10000, len(rewards), replace=False)

for i in range(len(rewards)):
    done = False
    reward = 0
    np.random.seed(int(seeds[i]))
    state = snake_env.restart()
    steps = 0
    while not done and steps <= max_steps:
        move = neural_net_decision(snake_net, state)
        # move = greedy_decision(snake_env)
        state, r, done = snake_env.step(move)
        reward += int(r > 0)
        steps += 1
    
    if reward > best_score:
        best_score = reward
        best_seed = seeds[i]

    rewards[i] = reward


print(f'Mean reward: {np.mean(rewards)}')
print(f'Max reward: {best_score}')
print(f'Best seed: {best_seed}')
