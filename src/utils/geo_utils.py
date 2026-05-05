# Define approximate bounding boxes (Min Lat, Max Lat, Min Lon, Max Lon)
#! These are simplified rectangles for a prototype.
indigenous_zones = {
    "D'harawal": {"lat": (-34.50, -33.90), "lon": (150.50, 151.20)},  # South of Sydney to Illawarra
    "Dharug": {"lat": (-33.90, -33.30), "lon": (150.00, 151.00)},     # Western Sydney / Blue Mountains
    "Guringai": {"lat": (-33.70, -33.30), "lon": (151.00, 151.40)},   # Northern Beaches / Ku-ring-gai
    "Gadigal": {"lat": (-33.90, -33.70), "lon": (151.10, 151.30)}     # Sydney CBD / Eastern Suburbs
}

def get_indigenous_land_name(lat: float, lon: float) -> str:
    """ 
        Maps GPS coordinates to Indigenous Country names using approximate bounding boxes.
        This function is a prototype. Would replace with PostGIS alongside some complex polygon "shapeflies" to perfectly map the coords TODO.
        
        Args:
            lat (float): Latitude coordinate.
            lon (float): Longitude coordinate.
            
        Returns:
            str: The name of the Indigenous land, or 'Unmapped/Unceded' if outside bounds.
    """

    # Iterate through the zones to see if the coordinates fall within a box
    for land_name, bounds in indigenous_zones.items():
        min_lat, max_lat = bounds["lat"]
        min_lon, max_lon = bounds["lon"]
        
        if (min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon):
            return land_name
            
    return "Unmapped/Unceded"

def generate_random_coordinate_for_zone(land_name: str) -> tuple:
    """
    Reverse function used for generating mock data. 
    Returns a random (lat, lon) pair within the specified Indigenous land.
    """

    import random
    
    if land_name in indigenous_zones:
        bounds = indigenous_zones[land_name]
        lat = random.uniform(bounds["lat"][0], bounds["lat"][1])
        lon = random.uniform(bounds["lon"][0], bounds["lon"][1])
        return round(lat, 6), round(lon, 6)
    
    # Default to a random spot generally in NSW if the zone isn't defined
    return round(random.uniform(-35.0, -28.0), 6), round(random.uniform(141.0, 153.0), 6)