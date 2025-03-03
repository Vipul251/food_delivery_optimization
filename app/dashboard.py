# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from streamlit_folium import folium_static

# # Placeholder function for route optimization (to be replaced with real model)
# def optimize_routes(orders_df, riders_df):
#     optimized_routes = []
#     for _, order in orders_df.iterrows():
#         rider = np.random.choice(riders_df["Rider ID"].values)
#         optimized_routes.append({"Order ID": order["Order ID"], "Assigned Rider": rider})
#     return pd.DataFrame(optimized_routes)

# # Streamlit UI
# st.title("Food Delivery Optimization Dashboard")

# # Order Input
# st.sidebar.header("Order Input")
# num_orders = st.sidebar.number_input("Number of Orders", min_value=1, max_value=100, value=10)
# num_riders = st.sidebar.number_input("Number of Riders", min_value=1, max_value=20, value=5)

# # Generate sample data for orders and riders
# orders_data = {
#     "Order ID": [f"O-{i+1}" for i in range(num_orders)],
#     "Latitude": np.random.uniform(26.8, 26.9, num_orders),
#     "Longitude": np.random.uniform(80.9, 81.0, num_orders)
# }
# orders_df = pd.DataFrame(orders_data)

# riders_data = {
#     "Rider ID": [f"R-{i+1}" for i in range(num_riders)],
#     "Latitude": np.random.uniform(26.8, 26.9, num_riders),
#     "Longitude": np.random.uniform(80.9, 81.0, num_riders)
# }
# riders_df = pd.DataFrame(riders_data)

# # Optimize and display results
# if st.button("Optimize Delivery Routes"):
#     optimized_df = optimize_routes(orders_df, riders_df)
#     st.subheader("Optimized Assignments")
#     st.dataframe(optimized_df)
    
#     # Map visualization
#     st.subheader("Route Visualization")
#     map_center = [orders_df["Latitude"].mean(), orders_df["Longitude"].mean()]
#     map_ = folium.Map(location=map_center, zoom_start=13)
    
#     # Plot orders
#     for _, row in orders_df.iterrows():
#         folium.Marker([row["Latitude"], row["Longitude"],], popup=row["Order ID"], icon=folium.Icon(color='blue')).add_to(map_)
    
#     # Plot riders
#     for _, row in riders_df.iterrows():
#         folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Rider ID"], icon=folium.Icon(color='red')).add_to(map_)
    
#     folium_static(map_)

# st.sidebar.text("Developed for optimized food delivery.")
import streamlit as st
import pandas as pd
import numpy as np
import faiss
import folium
from streamlit_folium import folium_static
# Function to optimize routes using FAISS for nearest neighbor search
def optimize_routes(orders_df, riders_df):
    d = 2  # Dimension for latitude and longitude
    index = faiss.IndexFlatL2(d)
    rider_locations = np.column_stack((riders_df["Latitude"].values, riders_df["Longitude"].values)).astype('float32')
    index.add(rider_locations)
    
    optimized_routes = []
    for _, order in orders_df.iterrows():
        order_location = np.array([[order["Latitude"], order["Longitude"]]], dtype='float32')
        _, idx = index.search(order_location, 1)
        assigned_rider = riders_df.iloc[idx[0][0]]["Rider ID"]
        optimized_routes.append({"Order ID": order["Order ID"], "Assigned Rider": assigned_rider})
    
    return pd.DataFrame(optimized_routes)

# Streamlit UI
st.title("Food Delivery Optimization Dashboard")

# Order Input
st.sidebar.header("Order Input")
num_orders = st.sidebar.number_input("Number of Orders", min_value=1, max_value=100, value=10)
num_riders = st.sidebar.number_input("Number of Riders", min_value=1, max_value=20, value=5)

# Generate sample data for orders and riders
orders_data = {
    "Order ID": [f"O-{i+1}" for i in range(num_orders)],
    "Latitude": np.random.uniform(26.8, 26.9, num_orders),
    "Longitude": np.random.uniform(80.9, 81.0, num_orders)
}
orders_df = pd.DataFrame(orders_data)

riders_data = {
    "Rider ID": [f"R-{i+1}" for i in range(num_riders)],
    "Latitude": np.random.uniform(26.8, 26.9, num_riders),
    "Longitude": np.random.uniform(80.9, 81.0, num_riders)
}
riders_df = pd.DataFrame(riders_data)

# Optimize and display results
if st.button("Optimize Delivery Routes"):
    optimized_df = optimize_routes(orders_df, riders_df)
    st.subheader("Optimized Routes")
    st.dataframe(optimized_df)
    
    # Map visualization
    st.subheader("Route Visualization")
    map_center = [orders_df["Latitude"].mean(), orders_df["Longitude"].mean()]
    map_ = folium.Map(location=map_center, zoom_start=13)
    
    # Plot orders
    for _, row in orders_df.iterrows():
        folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Order ID"], icon=folium.Icon(color='blue')).add_to(map_)
    
    # Plot riders
    for _, row in riders_df.iterrows():
        folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Rider ID"], icon=folium.Icon(color='red')).add_to(map_)
    
    folium_static(map_)

st.sidebar.text("Developed for optimized food delivery using FAISS and RL.")
