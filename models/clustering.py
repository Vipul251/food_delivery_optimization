from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

def assign_orders_using_clustering(df_orders, df_riders):
    X = df_orders[["Order_Value", "Food_Prep_Time"]]
    kmeans = KMeans(n_clusters=len(df_riders), random_state=42)
    df_orders["Assigned_Cluster"] = kmeans.fit_predict(X)

    # Assign riders to each cluster
    df_orders["Assigned_Rider"] = df_orders["Assigned_Cluster"].apply(lambda x: f"RIDER_{x+1}")

    return df_orders
