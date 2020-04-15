import sys
import numpy as np
import math
import random
import matplotlib.pyplot as plt

import gym
import gym_race

def simulate():
    learning_rate = get_learning_rate(0)
    explore_rate = get_explore_rate(0)
    discount_factor = 0.99
    total_reward = 0
    total_rewards = []
    training_done = False
    threshold = 1000
    env.set_view(True)
    for episode in range(NUM_EPISODES):

        total_rewards.append(total_reward)
        if episode == 50000:
            plt.plot(total_rewards)
            plt.ylabel('rewards')
            plt.show()
            env.save_memory('50000')
            break

        obv = env.reset()
        state_0 = state_to_bucket(obv)
        total_reward = 0

        if episode >= threshold:
            explore_rate = 0.01

        for t in range(MAX_T):
            action = select_action(state_0, explore_rate)
            obv, reward, done, _ = env.step(action)
            state = state_to_bucket(obv)
            env.remember(state_0, action, reward, state, done)
            total_reward += reward

            # Update the Q based on the result
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])

            # Setting up for the next iteration
            state_0 = state
            env.render()
            if done or t >= MAX_T - 1:
                print("Episode %d finished after %i time steps with total reward = %f."
                      % (episode, t, total_reward))
                break
        # Update parameters
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)

def load_and_play():
    print("Start loading history")
    history_list = ['30000.npy']

    # load data from history file
    print("Start updating q_table")
    discount_factor = 0.99
    for list in history_list:
        history = load_data(list)
        learning_rate = get_learning_rate(0)
        print(list)
        file_size = len(history)
        print("file size : " + str(file_size))
        i = 0
        for data in history:
            state_0, action, reward, state, done = data
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])
            if done == True:
                i += 1
                learning_rate = get_learning_rate(i)

    print("Updating q_table is complete")


    # play game
    env.set_view(True)
    reward_count = 0
    for episode in range(NUM_EPISODES):
        obv = env.reset()
        state_0 = state_to_bucket(obv)
        total_reward = 0
        for t in range(MAX_T):
            action = select_action(state_0, 0.01)
            obv, reward, done, _ = env.step(action)
            state = state_to_bucket(obv)
            total_reward += reward
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])
            state_0 = state
            env.render()
            if done or t >= MAX_T - 1:
                print("Episode %d finished after %i time steps with total reward = %f."
                      % (episode, t, total_reward))
                break
        if total_reward >= 1000:
            reward_count += 1
        else:
            reward_count = 0

        if reward_count >= 10:
            env.set_view(True)

        learning_rate = get_learning_rate(i + episode)


def load_and_simulate():
    print("Start loading history")
    history_list = ['30000.npy']

    # load data from history file
    print("Start updating q_table")
    discount_factor = 0.99
    i = 0
    for list in history_list:
        history = load_data(list)
        learning_rate = get_learning_rate(0)
        print(list)
        file_size = len(history)
        print("file size : " + str(file_size))
        for data in history:
            state_0, action, reward, state, done = data
            env.remember(state_0, action, reward, state, done)
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])
            if done == True:
                i += 1
                learning_rate = get_learning_rate(i)

    print("Updating q_table is complete")


    # simulate
    env.set_view(False)
    for episode in range(NUM_EPISODES):
        obv = env.reset()
        state_0 = state_to_bucket(obv)
        total_reward = 0

        if episode > 3000 and episode <= 3010:
            if episode == 3001:
                env.save_memory('3000_aft')
            env.set_view(True)
        elif episode > 5000 and episode <= 5010:
            if episode == 5001:
                env.save_memory('5000_aft')
            env.set_view(True)

        for t in range(MAX_T):
            action = select_action(state_0, 0.01)
            obv, reward, done, _ = env.step(action)
            state = state_to_bucket(obv)
            env.remember(state_0, action, reward, state, done)
            state_0 = state
            total_reward += reward
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])
            env.render()
            if done or t >= MAX_T - 1:
                print("Episode %d finished after %i time steps with total reward = %f."
                      % (episode, t, total_reward))
                break

        learning_rate = get_learning_rate(i + episode)



def select_action(state, explore_rate):
    if random.random() < explore_rate:
        action = env.action_space.sample()
    else:
        action = int(np.argmax(q_table[state]))
    return action

def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))

def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))

def state_to_bucket(state):
    bucket_indice = []
    for i in range(len(state)):
        if state[i] <= STATE_BOUNDS[i][0]:
            bucket_index = 0
        elif state[i] >= STATE_BOUNDS[i][1]:
            bucket_index = NUM_BUCKETS[i] - 1
        else:
            # Mapping the state bounds to the bucket array
            bound_width = STATE_BOUNDS[i][1] - STATE_BOUNDS[i][0]
            offset = (NUM_BUCKETS[i]-1)*STATE_BOUNDS[i][0]/bound_width
            scaling = (NUM_BUCKETS[i]-1)/bound_width
            bucket_index = int(round(scaling*state[i] - offset))
        bucket_indice.append(bucket_index)
    return tuple(bucket_indice)

def load_data(file):
    np_load_old = np.load
    np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
    data = np.load(file)
    np.load = np_load_old
    return data

if __name__ == "__main__":

    env = gym.make("Pyrace-v0")
    NUM_BUCKETS = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    NUM_ACTIONS = env.action_space.n
    STATE_BOUNDS = list(zip(env.observation_space.low, env.observation_space.high))

    MIN_EXPLORE_RATE = 0.001
    MIN_LEARNING_RATE = 0.2
    DECAY_FACTOR = np.prod(NUM_BUCKETS, dtype=float) / 10.0
    print(DECAY_FACTOR)

    NUM_EPISODES = 9999999
    MAX_T = 2000
    #MAX_T = np.prod(NUM_BUCKETS, dtype=int) * 100

    q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,), dtype=float)
    simulate()
    #load_and_play()
