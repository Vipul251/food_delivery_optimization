import pandas as pd

def load_data():
    orders = pd.read_csv("../data/synthetic_orders.csv")
    riders = pd.read_csv("../data/synthetic_riders.csv")
    deliveries = pd.read_csv("../data/synthetic_deliveries.csv")

    return orders, riders, deliveries
