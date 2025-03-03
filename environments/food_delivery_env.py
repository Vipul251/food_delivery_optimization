import numpy as np
import gym
from gym import spaces

class FoodDeliveryEnv(gym.Env):
    def __init__(self):
        super(FoodDeliveryEnv, self).__init__()

        # Define observation space (modify according to your environment)
        self.observation_space = spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32)

        # Define action space (modify according to your environment)
        self.action_space = spaces.Discrete(4)

        self.state = None  # Placeholder for initial state
        self.seed()  # Initialize seed

    def seed(self, seed=None):
        """Set the environment's random seed."""
        np.random.seed(seed)

    def reset(self, seed=None, options=None):
        """Resets the environment and ensures compatibility with Stable-Baselines3"""
        # Ensure compatibility with Gymnasium
        super().reset(seed=seed)  

        # If a seed is provided, apply it
        if seed is not None:
            self.seed(seed)

        self.state = np.zeros(2, dtype=np.float32)  # Example state initialization

        return self.state, {}  # Return observation and empty info dict

    def step(self, action):
        """Takes an action and returns the next state, reward, done flag, truncated flag, and info."""
        # Example state transition (modify this based on your actual logic)
        self.state += np.random.randn(2) * 0.1  # Small random movement

        reward = -1  # Define reward logic
        done = False  # Define termination condition

        return self.state, reward, done, False, {}  # Return all necessary values

