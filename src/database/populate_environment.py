import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("!!! DATABASE_URL not found in .env file!")

engine = create_engine(db_url)

def populate_dim_environment():
    print("Populating Environment Dimension...")


    # defining the 6 BOM Standard National Climate Zones
    climate_zones = [
        'Equatorial', 'Tropical', 'Subtropical', 
        'Desert', 'Grassland', 'Temperate'
    ]

    states = ['NSW', 'QLD', 'VIC', 'TAS', 'SA', 'WA', 'NT', 'ACT']

    env_records = []

    for state in states:
        for zone in climate_zones:
            if state == 'NSW' and zone == 'Temperate':
                # Special Case Test: NSW D'harawal Seasons
                dharawal = [
                    ('Burran', True, False),                                                                # Jan-Mar: Kangaroo breeding
                    ('Marrai\'gang', True, False),                                                          # Apr-Jun: Quoll breeding
                    ('Burrugin', True, False),                                                              # Jun-Jul: Echidna breeding
                    ('Wiritjiribin', True, False),                                                          # Jul-Aug: Lyrebird breeding
                    ('Ngoonungi', False, False),                                                            # Sep-Oct: Flying Fox gathering
                    ('Parra\'dowee', False, True)                                                           # Nov-Dec: Eel journey / Storms
                ]

                for name, breeding, fire in dharawal:
                    env_records.append({
                        'state': state,
                        'climate_zone': zone,
                        'phenological_season_name': name,
                        'is_breeding_season': breeding,
                        'is_fire_season': fire
                    })
            else:
                seasons = ['Summer','Autumn','Winter','Spring']
                for season in seasons:
                    env_records.append({
                        'state': state,
                        'climate_zone': zone,
                        'phenological_season_name': season,
                        'is_breeding_season': False,                                                        # TODO: To be updated via tracking data later
                        'is_fire_season': True if season in ['Summer', 'Spring'] else False
                    })
                    
    df_env = pd.DataFrame(env_records)

    try:
        df_env.to_sql('dim_environment', engine, if_exists='append', index=False)
        print(f"{len(df_env)} Environmental logs loaded.")
    except Exception as e:
        print(f"!!! Error: {e}")

if __name__ == "__main__":
    populate_dim_environment()