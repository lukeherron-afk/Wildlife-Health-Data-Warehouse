import random
import pandas as pd
from sqlalchemy import text
from src.utils import get_engine, generate_random_coordinate_for_zone, get_indigenous_land_name

def generate_mock_data():
    print("Generating Advanced Mock Wildlife Data with Spatial Enrichment...")
    engine = get_engine()

    with engine.begin() as conn:
        # 1. Setup Multi-Agency Data
        agencies = [
            {'name': 'UTS Research', 'type': 'Academic'},
            {'name': 'NSW National Parks', 'type': 'Government'},
            {'name': 'Wildlife Rescue NGO', 'type': 'Non-Profit'}
        ]
        for a in agencies:
            conn.execute(text("INSERT INTO dim_agency (agency_name, agency_type) VALUES (:name, :type) ON CONFLICT DO NOTHING"), a)

        # 2. Setup Spatial Data (CARE Principle ETL Demonstration)
        print("Enriching raw GPS coordinates with Indigenous Land data...")
        zones = ["D'harawal", "Dharug", "Guringai", "Gadigal"]
        
        # Simulate 20 distinct remote tracking sites
        for _ in range(20):
            target = random.choice(zones)
            # Simulate a raw GPS coordinate coming from a tracker
            raw_lat, raw_lon = generate_random_coordinate_for_zone(target)
            
            # AUTOMATED ETL ENRICHMENT: Resolve the Indigenous Land Name dynamically
            resolved_land = get_indigenous_land_name(raw_lat, raw_lon)
            
            loc_data = {
                'region': 'Greater Sydney',
                'land': resolved_land,
                'state': 'NSW',
                'lat': raw_lat,
                'lon': raw_lon,
                'site': 'Tracking Station'
            }
            conn.execute(text("""
                INSERT INTO dim_location 
                (region_name, indigenous_land_name, state, latitude, longitude, site_type) 
                VALUES (:region, :land, :state, :lat, :lon, :site)
            """), loc_data)

        # Fetch IDs for relationships
        date_ids = [row[0] for row in conn.execute(text("SELECT date_id FROM dim_date")).fetchall()]
        env_ids = [row[0] for row in conn.execute(text("SELECT env_id FROM dim_environment WHERE state='NSW'")).fetchall()]
        loc_ids = [row[0] for row in conn.execute(text("SELECT location_id FROM dim_location")).fetchall()]
        agn_ids = [row[0] for row in conn.execute(text("SELECT agency_id FROM dim_agency")).fetchall()]

    # 3. Biological Rule Engine for Species
    species_profiles = {
        'Koala': {'temp_range': (35.5, 36.5), 'weight_range': (4.0, 15.0)},
        'Eastern Grey Kangaroo': {'temp_range': (35.5, 37.0), 'weight_range': (15.0, 66.0)},
        'Common Brushtail Possum': {'temp_range': (35.0, 36.2), 'weight_range': (1.2, 4.5)},
        'Short-beaked Echidna': {'temp_range': (30.0, 34.0), 'weight_range': (2.0, 7.0)},
        'Platypus': {'temp_range': (31.0, 33.0), 'weight_range': (0.7, 3.0)}
    }

    # Generate 200 Animals
    animals = []
    species_list = list(species_profiles.keys())
    for _ in range(200):
        animals.append({
            'species_name': random.choice(species_list),
            'sex': random.choice(['M', 'F', 'U']),
            'estimated_age': random.randint(1, 15)
        })
    
    df_animals = pd.DataFrame(animals)
    with engine.begin() as conn:
        df_animals.to_sql('dim_animal', conn, if_exists='append', index=False)
        animal_records = conn.execute(text("SELECT animal_id, species_name FROM dim_animal")).fetchall()

    # Generate 1000 Observations
    print("Generating clinical observations...")
    observations = []
    for _ in range(1000):
        animal = random.choice(animal_records)
        a_id = animal[0]
        species = animal[1]
        profile = species_profiles[species]

        base_temp = random.uniform(profile['temp_range'][0], profile['temp_range'][1])
        base_weight = random.uniform(profile['weight_range'][0], profile['weight_range'][1])
        
        if random.random() < 0.10:
            health_score = random.randint(1, 2)
            base_temp += random.uniform(1.0, 2.5)
        else:
            health_score = random.randint(3, 5)

        observations.append({
            'date_id': random.choice(date_ids),
            'animal_id': a_id,
            'location_id': random.choice(loc_ids),
            'agency_id': random.choice(agn_ids),
            'env_id': random.choice(env_ids),
            'body_temperature': round(base_temp, 2),
            'weight': round(base_weight, 2),
            'health_status_score': health_score
        })

    df_obs = pd.DataFrame(observations)
    with engine.begin() as conn:
        df_obs.to_sql('fact_observations', conn, if_exists='append', index=False)
    
    print(f"Success: 200 animals and 1000 observations loaded into the warehouse.")

if __name__ == "__main__":
    generate_mock_data()