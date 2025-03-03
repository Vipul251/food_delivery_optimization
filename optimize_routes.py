import pandas as pd
import networkx as nx
import random

# Load delivery data
df_deliveries = pd.read_csv("data/synthetic_deliveries.csv")

# Create a graph for the city road network (simulated)
G = nx.grid_2d_graph(100, 100)  # 100x100 grid as a city map

# Assign weights (randomized for now)
for u, v in G.edges():
    G[u][v]['weight'] = random.uniform(1, 10)

# Convert GPS coordinates to grid indices
def convert_to_grid(lat, lon, min_lat=26.7, max_lat=27.7, min_lon=80.8, max_lon=81.8, grid_size=100):
    """Convert GPS coordinates (lat, lon) to a valid (x, y) grid coordinate."""
    x = int((lat - min_lat) / (max_lat - min_lat) * (grid_size - 1))
    y = int((lon - min_lon) / (max_lon - min_lon) * (grid_size - 1))
    return max(0, min(grid_size - 1, x)), max(0, min(grid_size - 1, y))

def find_best_route(pickup, dropoff):
    """Find the shortest route using Dijkstra’s algorithm."""
    return nx.shortest_path(G, source=pickup, target=dropoff, weight='weight')

# Process each delivery
routes = []
for delivery in df_deliveries.itertuples():
    try:
        # Ensure pickup and dropoff are tuples
        pickup_lat, pickup_lon = map(float, delivery.Pickup_Location.strip("()").split(","))
        dropoff_lat, dropoff_lon = map(float, delivery.Dropoff_Location.strip("()").split(","))

        # Convert GPS coordinates to grid
        pickup = convert_to_grid(pickup_lat, pickup_lon)
        dropoff = convert_to_grid(dropoff_lat, dropoff_lon)

        # Check if nodes exist in graph
        if pickup not in G or dropoff not in G:
            print(f"Skipping order {delivery.Order_ID}: No valid grid location found.")
            continue

        # Find best route
        best_route = find_best_route(pickup, dropoff)
        routes.append([delivery.Order_ID, best_route])

    except Exception as e:
        print(f"Error processing order {delivery.Order_ID}: {e}")

# Save routes
df_routes = pd.DataFrame(routes, columns=["Order_ID", "Optimized_Route"])
df_routes.to_csv("data/optimized_routes.csv", index=False)
print("Optimized routes saved successfully!")
