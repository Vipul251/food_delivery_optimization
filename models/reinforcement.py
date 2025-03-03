import gym
import numpy as np

class DeliveryEnv(gym.Env):
    def __init__(self):
        super(DeliveryEnv, self).__init__()
        self.state = np.zeros(10)
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)

    def step(self, action):
        reward = -1
        if action == 0:
            reward = 10  # Assigning an order gives a reward
        elif action == 1:
            reward = -5  # Small penalty for waiting
        return self.state, reward, False, {}

    def reset(self):
        return np.zeros(10)
