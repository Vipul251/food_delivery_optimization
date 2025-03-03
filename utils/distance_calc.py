import numpy as np

# Function to calculate distance using Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth.
    Parameters:
    lat1, lon1: Latitude and Longitude of point 1
    lat2, lon2: Latitude and Longitude of point 2
    Returns:
    Distance in kilometers
    """
    R = 6371  # Radius of Earth in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return R * c

# Example usage
if __name__ == "__main__":
    lat1, lon1 = 26.85, 80.92  # Example location 1 (Lucknow)
    lat2, lon2 = 26.88, 80.95  # Example location 2

    print(f"Distance: {haversine_distance(lat1, lon1, lat2, lon2):.2f} km")
