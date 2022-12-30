from enviroment import SnakeGame
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
from tensorflow import keras
from wrappers import FrameStack
from utils import neural_net_decision, greedy_decision
import sys

def make_step():
    global state
    global reward
    move = neural_net_decision(snake_net, state)
    # move = greedy_decision(snake_env)
    state, r, done = snake_env.step(move)
    reward += int(r > 0)
    if done:
        anim.save("images/cnn.gif", dpi=300, writer=PillowWriter(fps=fps))
        sys.exit()
    state = np.array(state)
    return state[:,:,-1]

snake_env = FrameStack(SnakeGame(), 3)
snake_net = keras.models.load_model('snake_net.keras')

np.random.seed(8458)#2210
state = np.array(snake_env.restart())
reward = 0

fps = 10
nSeconds = 30

fig = plt.figure()
im = plt.imshow(np.zeros((snake_env.env.h, snake_env.env.w)), interpolation='none', aspect='auto', vmin=0, vmax=1, cmap='gray')
plt.title(f'Cost: 0')

def animate_func(i):
    current_state = make_step()
    im.set_array(current_state)
    plt.title(f'Cost: {reward}')
    return [im]

anim = FuncAnimation(fig, 
                    animate_func, 
                    frames = nSeconds * fps,
                    interval = 1000 / fps,
                    repeat=False)
                    
anim.save("images/cnn.gif", dpi=300, writer=PillowWriter(fps=fps))