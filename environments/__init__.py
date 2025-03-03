from gym.envs.registration import register

register(
    id="FoodDelivery-v0",
    entry_point="environments.food_delivery_env:FoodDeliveryEnv",  # Adjust the class name
)
