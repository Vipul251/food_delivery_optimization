import networkx as nx

def optimize_routes(df_deliveries):
    G = nx.Graph()

    for _, row in df_deliveries.iterrows():
        G.add_edge(row["Pickup_Location"], row["Dropoff_Location"], weight=row["Distance"])

    shortest_paths = {}
    for order_id in df_deliveries["Order_ID"].unique():
        path = nx.shortest_path(G, source=df_deliveries.iloc[0]["Pickup_Location"], 
                                target=df_deliveries.iloc[-1]["Dropoff_Location"], weight="weight")
        shortest_paths[order_id] = path

    return shortest_paths
