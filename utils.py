import math
import tensorflow as tf

def greedy_decision(env):
    chosen_move = 0
    min_dist = math.inf
    old_snake_head = env.env.snake[0].copy()
    for move_num, move in enumerate(env.env.possible_moves):
        env.env.snake[0] = [old_snake_head[0] + move[0], old_snake_head[1] + move[1]]
        is_collision = env.env.check_collision()
        if not is_collision:
            dist = abs(env.env.snake[0][0] - env.env.apple[0]) + abs(env.env.snake[0][1] - env.env.apple[1])
            if dist < min_dist:
                chosen_move = move_num
                min_dist = dist
    env.env.snake[0] = old_snake_head.copy()
    return chosen_move

def neural_net_decision(net, state):
    state_tensor = tf.convert_to_tensor(state)
    state_tensor = tf.expand_dims(state_tensor, 0)
    return tf.argmax(net(state_tensor, training=False)[0]).numpy()