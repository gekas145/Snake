import tensorflow as tf
import keras
from enviroment import SnakeGame
import numpy as np
from wrappers import FrameStack


def get_model(env_w, env_h, num_actions, memory_length):
    inputs = keras.layers.Input(shape=(env_h, env_w, memory_length))

    layer1 = keras.layers.Conv2D(32, (8, 8), strides=4, activation="relu")(inputs)
    layer2 = keras.layers.Conv2D(64, (2, 2), activation="relu")(layer1)

    layer3 = keras.layers.Flatten()(layer2)

    layer4 = keras.layers.Dense(256, activation="relu")(layer3)
    actions = keras.layers.Dense(num_actions, activation="linear")(layer4)

    return keras.Model(inputs=inputs, outputs=actions)

env_w, env_h = 80, 80 # default snake game field size
num_actions = 4
memory_length = 3 # how many last game frames will snake see
snake_env = FrameStack(SnakeGame(), memory_length)

# adopted version of https://keras.io/examples/rl/deep_q_network_breakout/

model, target_model = get_model(env_w, env_h, num_actions, memory_length), get_model(env_w, env_h, num_actions, memory_length)
optimizer = keras.optimizers.Adam(learning_rate=0.001, clipnorm=1.0)

gamma = 0.95
epsilon = 1.0
epsilon_min = 0.0
epsilon_max = 1.0
epsilon_interval = epsilon_max - epsilon_min
batch_size = 32
max_steps_per_episode = 1000

action_history = []
state_history = []
state_next_history = []
rewards_history = []
done_history = []
episode_reward_history = []
running_reward = 0
episode_count = 0
frame_count = 0
# Number of frames to take random action and observe output
epsilon_random_frames = 50000
# Number of frames for exploration
epsilon_greedy_frames = 1000000.0
# Maximum replay length
# Note: The Deepmind paper suggests 1000000 however this causes memory issues
max_memory_buffer_length = 50000
# Train the model after 4 actions
update_after_actions = 4
# How often to update the target network
update_target_network = 10000
# Using Huber loss for stability
loss_function = keras.losses.Huber()

while True:  # Run until solved
    state = snake_env.restart()
    episode_reward = 0

    for timestep in range(1, max_steps_per_episode+1):
        frame_count += 1

        # use epsilon greedy policy
        if frame_count < epsilon_random_frames or np.random.uniform(0, 1) < epsilon:
            action = np.random.choice(num_actions)
        else:
            state_tensor = tf.convert_to_tensor(np.array(state))
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_probs = model(state_tensor, training=False)
            # Take best action
            action = tf.argmax(action_probs[0]).numpy()

        # Decay probability of taking random action
        epsilon -= epsilon_interval / epsilon_greedy_frames
        epsilon = max(epsilon, epsilon_min)

        # Apply the sampled action in our environment
        state_next, reward, done = snake_env.step(action)

        episode_reward += reward

        # Save actions and states in replay buffer
        action_history.append(action)
        state_history.append(state)
        state_next_history.append(state_next)
        done_history.append(done)
        rewards_history.append(reward)
        state = state_next

        # Update every update_after_actions frame and once batch size is over batch_size
        if frame_count % update_after_actions == 0 and len(done_history) > batch_size:

            # Get indices of samples for replay buffers
            indices = np.random.choice(range(len(done_history)), size=batch_size)

            # Sample from replay buffer
            state_sample = np.array([state_history[i] for i in indices])
            state_next_sample = np.array([state_next_history[i] for i in indices])
            rewards_sample = [rewards_history[i] for i in indices]
            action_sample = [action_history[i] for i in indices]
            done_sample = tf.convert_to_tensor([float(done_history[i]) for i in indices])

            # Build the updated Q-values for the sampled future states
            # Use the target model for stability
            future_rewards = target_model.predict(state_next_sample, verbose=0)
            # Q value = reward + discount factor * expected future reward
            updated_q_values = rewards_sample + gamma * tf.multiply(tf.reduce_max(future_rewards, axis=1), 1-done_sample)

            # Create a mask so we know which Q-values need to be updated
            masks = tf.one_hot(action_sample, num_actions)

            with tf.GradientTape() as tape:
                # Train the model on the states and updated Q-values
                q_values = model(np.array(state_sample))

                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                # Calculate loss between new Q-value and old Q-value
                loss = loss_function(updated_q_values, q_action)

            # Backpropagation
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if frame_count % update_target_network == 0:
            # update the the target network with new weights
            target_model.set_weights(model.get_weights())
            # Log details
            print(f"running reward: {running_reward:.2f} at episode {episode_count}, frame count {frame_count}, epsilon {epsilon}")
            target_model.save('snake_net.keras') # make backup

        # Limit the state and reward history
        if len(rewards_history) > max_memory_buffer_length:
            del rewards_history[:1]
            del state_history[:1]
            del state_next_history[:1]
            del action_history[:1]
            del done_history[:1]

        if done:
            break

    # Update running reward to check condition for solving
    episode_reward_history.append(episode_reward)
    if len(episode_reward_history) > 100: # keep last 100 episode results
        del episode_reward_history[:1]
    running_reward = np.mean(episode_reward_history)

    episode_count += 1

    if running_reward > 8:  # Condition to consider the task solved
        break

target_model.save('snake_net.keras')
