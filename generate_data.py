import pandas as pd
import numpy as np
import random

#Generate restaurant data

num_orders = 1000  # Adjust as needed

orders = []
for i in range(num_orders):
    order_id = f"ORD_{i+1}"
    restaurant_id = f"REST_{random.randint(1, 50)}"  # 50 restaurants
    customer_id = f"CUST_{random.randint(1, 500)}"  # 500 customers
    order_time = pd.Timestamp('2025-03-01') + pd.to_timedelta(random.randint(0, 86400), unit='s')  # Random time in a day
    food_prep_time = random.randint(5, 20)  # 5 to 20 minutes
    packaging_time = random.randint(2, 10)  # 2 to 10 minutes
    order_value = random.randint(100, 500)  # ₹100 to ₹500

    orders.append([order_id, restaurant_id, customer_id, order_time, food_prep_time, packaging_time, order_value])

df_orders = pd.DataFrame(orders, columns=["Order_ID", "Restaurant_ID", "Customer_ID", "Order_Time", "Food_Prep_Time", "Packaging_Time", "Order_Value"])

#generate rider data
num_riders = 50  # Adjust as needed

riders = []
for i in range(num_riders):
    rider_id = f"RIDER_{i+1}"
    rider_location = (round(random.uniform(26.50, 27.17), 5), round(random.uniform(80.50, 81.22), 5))  # Random location in Lucknow
    rider_availability = random.choice(["Available", "Busy"])
    max_capacity = 20  # Max orders a rider can carry

    riders.append([rider_id, rider_location, rider_availability, max_capacity])

df_riders = pd.DataFrame(riders, columns=["Rider_ID", "Location", "Availability", "Max_Capacity"])

#generate delivery data
deliveries = []
for order in df_orders.itertuples():
    pickup_location = (round(random.uniform(26.50, 27.17), 5), round(random.uniform(80.50, 81.22), 5))
    dropoff_location = (round(random.uniform(26.50, 27.17), 5), round(random.uniform(80.50, 81.22), 5))
    distance = round(random.uniform(1, 10), 2)  # Distance in km
    delivery_time_window = order.Order_Time + pd.to_timedelta(order.Food_Prep_Time + order.Packaging_Time + 15, unit='m')  # Adding buffer for delivery
    delivery_status = "Pending"

    deliveries.append([order.Order_ID, pickup_location, dropoff_location, distance, delivery_time_window, delivery_status])

df_deliveries = pd.DataFrame(deliveries, columns=["Order_ID", "Pickup_Location", "Dropoff_Location", "Distance", "Delivery_Time_Window", "Status"])
df_orders.to_csv("synthetic_orders.csv", index=False)
df_riders.to_csv("synthetic_riders.csv", index=False)
df_deliveries.to_csv("synthetic_deliveries.csv", index=False)

