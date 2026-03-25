import os
import random
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("!!! DATABASE_URL not found in .env file!")

engine = create_engine(db_url)

def generate_mock_data():
    print("Generating Mock Wildlife Data...")

    with engine.connect() as conn:
        date_ids = [row[0] for row in conn.execute(text("SELECT date_id FROM dim_date")).fetchall()]
        env_ids = [row[0] for row in conn.execute(text("SELECT env_id FROM dim_environment")).fetchall()]
        
        conn.execute(
            text("INSERT INTO dim_location (region_name, indigenous_land_name, state) VALUES (:region, :land, :state) ON CONFLICT DO NOTHING"),
            {"region": "Sydney Basin", "land": "D'harawal", "state": "NSW"}
        )
        conn.execute(text("INSERT INTO dim_agency (agency_name, agency_type) VALUES ('UTS Research', 'Academic') ON CONFLICT DO NOTHING"))
        conn.commit()
        
        loc_id = conn.execute(text("SELECT location_id FROM dim_location LIMIT 1")).fetchone()[0]
        agn_id = conn.execute(text("SELECT agency_id FROM dim_agency LIMIT 1")).fetchone()[0]

    species_list = ['Koala', 'Eastern Grey Kangaroo', 'Common Brushtail Possum', 'Short-beaked Echidna', 'Platypus']
    animals = []
    for _ in range(50):
        animals.append({
            'species_name': random.choice(species_list) ,
            'sex': random.choice(['M', 'F', 'U']),
            'estimated_age': random.randint(1, 15)
        })
    
    df_animals = pd.DataFrame(animals)
    df_animals.to_sql('dim_animal', engine, if_exists='append', index=False)
    
    with engine.connect() as conn:
        animal_ids = [row[0] for row in conn.execute(text("SELECT animal_id FROM dim_animal")).fetchall()]

    observations = []
    for i in range(50):
        observations.append({
            'date_id': random.choice(date_ids),
            'animal_id': animal_ids[i],
            'location_id': loc_id,
            'agency_id': agn_id,
            'env_id': random.choice(env_ids),
            'body_temperature': round(random.uniform(35.5, 39.0), 2),
            'weight': round(random.uniform(2.0, 25.0), 2),
            'health_status_score': random.randint(1, 5)
        })

    df_obs = pd.DataFrame(observations)
    
    try:
        df_obs.to_sql('fact_observations', engine, if_exists='append', index=False)
        print(f"50 animals and 50 observations loaded into the warehouse.")
    except Exception as e:
        print(f"!!! Error: {e}")

if __name__ == "__main__":
    generate_mock_data()