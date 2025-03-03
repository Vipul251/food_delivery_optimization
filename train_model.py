import pandas as pd
import numpy as np
import gymnasium as gym  # Corrected import
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# Load synthetic data
df_orders = pd.read_csv("data/synthetic_orders.csv")
df_riders = pd.read_csv("data/synthetic_riders.csv")

# Example mapping of restaurant IDs to coordinates (Replace with real data)
restaurant_locations = {
    "REST_30": (26.850000, 80.949997),  # Example coordinates for Lucknow
    "REST_31": (26.8467, 80.9462),
    # Add more restaurant IDs with their coordinates
}

def parse_location(location_str):
    """Parse location from a string containing coordinates or a restaurant ID."""
    try:
        if isinstance(location_str, str):
            location_str = location_str.strip()

            if "(" in location_str and "," in location_str:  # If already a coordinate string
                lat, lon = map(float, location_str.strip("()").split(","))
                return lat, lon
            elif location_str in restaurant_locations:  # If it's a restaurant ID
                return restaurant_locations[location_str]
            else:
                print(f"⚠️ Warning: Unknown location identifier '{location_str}', using default location.")
                return (26.85, 80.95)  # Default Lucknow coordinates
        
        print(f"⚠️ Warning: Invalid location format '{location_str}', using default location.")
        return (26.85, 80.95)  # Default location

    except Exception as e:
        print(f"⚠️ Error parsing location '{location_str}': {e}")
        return (26.85, 80.95)  # Default fallback location

class FoodDeliveryEnv(gym.Env):
    """Custom Reinforcement Learning environment for food delivery optimization."""
    def __init__(self, orders, riders):
        super(FoodDeliveryEnv, self).__init__()
        self.orders = orders
        self.riders = riders
        self.num_orders = len(orders)
        self.num_riders = len(riders)

        self.action_space = gym.spaces.Discrete(self.num_riders)  # Choose a rider
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(self.num_orders, 3), dtype=np.float32)

        self.current_order_idx = 0
        self.state = self._get_observation()

    def reset(self, seed=None, options=None):
        """Reset environment state and return (observation, info)."""
        super().reset(seed=seed)  # Ensures compatibility with Gymnasium
        self.current_order_idx = 0
        self.state = self._get_observation()
        return self.state, {}  # Return observation and empty info dict

    def step(self, action):
        """Take an action and return next state, reward, done, truncated, info."""
        rider = self.riders.iloc[action]
        order = self.orders.iloc[self.current_order_idx]

        # Ensure valid locations before computing distance
        order_location = parse_location(order.get("Restaurant_ID", ""))
        rider_location = parse_location(rider.get("Location", ""))

        try:
            distance = np.linalg.norm(np.array(order_location) - np.array(rider_location))
            reward = -distance  # Minimize distance
        except Exception as e:
            print(f"⚠️ Error calculating distance: {e}")
            reward = -100  # Penalize heavily for invalid distance calculations

        self.current_order_idx += 1
        done = self.current_order_idx >= self.num_orders
        truncated = False  # No early termination

        return self._get_observation(), reward, done, truncated, {}

    def _get_observation(self):
        """Generate observation state."""
        obs = np.random.rand(self.num_orders, 3)  # Random example state
        return obs.astype(np.float32)

# Initialize environment
env = DummyVecEnv([lambda: FoodDeliveryEnv(df_orders, df_riders)])

# Train reinforcement learning model
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save trained model
model.save("models/food_delivery_rl")
print("Reinforcement learning model trained and saved!")
