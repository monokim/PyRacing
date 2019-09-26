import gym
from gym import spaces
import numpy as np
from gym_race.envs.pyrace_2d import PyRace2D

class RaceEnv(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self):
        print("init")
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([10, 10, 10, 10, 10]), dtype=np.int)
        self.is_view = True
        self.pyrace = PyRace2D(self.is_view)
        self.memory = []

    def reset(self):
        del self.pyrace
        self.pyrace = PyRace2D(self.is_view)
        obs = self.pyrace.observe()
        return obs

    def step(self, action):
        self.pyrace.action(action)
        reward = self.pyrace.evaluate()
        done = self.pyrace.is_done()
        obs = self.pyrace.observe()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        if self.is_view:
            self.pyrace.view()

    def set_view(self, flag):
        self.is_view = flag

    def save_memory(self, file):
        np.save(file, self.memory)
        print(file + " saved")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
