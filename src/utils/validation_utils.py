import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def validate_observation(species_name: str, temp: float, weight: float, health_score: int) -> dict:
    """
    Validates clinical wildlife observations against known biological baselines.
    Ensures data quality and integrity for the warehouse.
    
    Returns a dictionary with 'is_valid' boolean and a list of 'flags'.
    """
    
    # Biological baselines (Min Temp, Max Temp, Min Weight, Max Weight)
    # These bounds are slightly wider than the mock generator to allow for natural variance
    biological_bounds = {
        'Koala': {'temp': (34.0, 38.5), 'weight': (3.0, 16.0)},
        'Eastern Grey Kangaroo': {'temp': (34.5, 38.0), 'weight': (12.0, 70.0)},
        'Common Brushtail Possum': {'temp': (34.0, 37.5), 'weight': (1.0, 5.0)},
        'Short-beaked Echidna': {'temp': (28.0, 35.0), 'weight': (1.5, 8.0)},
        'Platypus': {'temp': (30.0, 34.5), 'weight': (0.5, 3.5)}
    }

    result = {
        "is_valid": True,
        "flags": []
    }

    if not isinstance(health_score, int) or not (1 <= health_score <= 5):
        result["is_valid"] = False
        result["flags"].append(f"Invalid health score ({health_score}). Must be an integer between 1 and 5.")

    if species_name in biological_bounds:
        bounds = biological_bounds[species_name]
        
        if not (bounds['temp'][0] <= temp <= bounds['temp'][1]):
            result["is_valid"] = False
            result["flags"].append(f"Temperature {temp}°C out of realistic range for {species_name}.")
            
        if not (bounds['weight'][0] <= weight <= bounds['weight'][1]):
            result["is_valid"] = False
            result["flags"].append(f"Weight {weight}kg out of realistic range for {species_name}.")
    else:
        # If a new species is added without a baseline, flag it for manual review
        result["flags"].append(f"Warning: No biological baseline established for {species_name}.")
        logging.warning(result["flags"][-1])

    if not result["is_valid"]:
        logging.error(f"Data validation failed for {species_name}: {', '.join(result['flags'])}")

    return result

def clean_dataframe(df):
    """
    A utility wrapper that could be applied to a pandas DataFrame 
    during the automated ETL pipeline to drop invalid rows.
    """
    #! This is a placeholder for how you would apply the validation function 
    # across an entire batch of data coming from a CSV or API.
    pass