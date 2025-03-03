import random
import pandas as pd
import numpy as np
import faiss
from geopy.distance import geodesic
# Load synthetic data
df_orders = pd.read_csv("data/synthetic_orders.csv")
df_riders = pd.read_csv("data/synthetic_riders.csv")

def parse_location(location_str):
    """Convert string location (lat, lon) to tuple."""
    lat, lon = map(float, location_str.strip('()').split(','))
    return (lat, lon)
# Convert rider locations to FAISS index for fast nearest search
rider_locations = np.array([parse_location(loc) for loc in df_riders['Location']])
rider_index = faiss.IndexFlatL2(2)  # 2D space (latitude, longitude)
rider_index.add(rider_locations.astype(np.float32))

def assign_orders():
    """Assign orders to the nearest available rider while considering capacity."""
    assignments = []
    
    for order in df_orders.itertuples():
        order_id = order.Order_ID
         # Generate a random restaurant location (Simulated since Restaurant_ID does not contain lat/lon)
        order_location = (round(random.uniform(26.50, 27.17), 5), round(random.uniform(80.50, 81.22), 5))
  # Simulated as a location
        
        # Search for the nearest available rider
        _, rider_idx = rider_index.search(np.array([order_location], dtype=np.float32), k=1)
        assigned_rider_id = df_riders.iloc[rider_idx[0][0]]['Rider_ID']
        
        assignments.append([order_id, assigned_rider_id])
    
    df_assignments = pd.DataFrame(assignments, columns=["Order_ID", "Rider_ID"])
    df_assignments.to_csv("data/order_assignments.csv", index=False)
    print("Order assignments saved successfully!")

if __name__ == "__main__":
    assign_orders()
