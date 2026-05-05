import pandas as pd
from src.utils.db_utils import get_engine

def populate_dim_environment():
    print("Populating Environment Dimension...")

    # Defining the 6 BOM Standard National Climate Zones
    climate_zones = [
        'Equatorial', 'Tropical', 'Subtropical', 
        'Desert', 'Grassland', 'Temperate'
    ]

    states = ['NSW', 'QLD', 'VIC', 'TAS', 'SA', 'WA', 'NT', 'ACT']
    env_records = []

    for state in states:
        for zone in climate_zones:
            if state == 'NSW' and zone == 'Temperate':
                # * CARE Principle Implementation: NSW D'harawal Seasons
                dharawal = [
                    ('Burran', True, False),        # Jan-Mar: Kangaroo breeding
                    ('Marrai\'gang', True, False),  # Apr-Jun: Quoll breeding
                    ('Burrugin', True, False),      # Jun-Jul: Echidna breeding
                    ('Wiritjiribin', True, False),  # Jul-Aug: Lyrebird breeding
                    ('Ngoonungi', False, False),    # Sep-Oct: Flying Fox gathering
                    ('Parra\'dowee', False, True)   # Nov-Dec: Eel journey / Storms
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
                # * Biological Rule Engine for Standard Seasons
                seasons = ['Summer', 'Autumn', 'Winter', 'Spring']
                for season in seasons:
                    # Default rules for most of Australia (Temperate/Grassland)
                    is_breeding = True if season == 'Spring' else False
                    is_fire = True if season in ['Summer', 'Spring'] else False
                    
                    # Tropical/Equatorial adjustment (Wet/Dry season biological triggers)
                    if zone in ['Tropical', 'Equatorial']:
                        if season == 'Summer':   # Wet Season
                            is_breeding = True
                            is_fire = False
                        elif season == 'Winter': # Dry Season
                            is_fire = True
                            
                    env_records.append({
                        'state': state,
                        'climate_zone': zone,
                        'phenological_season_name': season,
                        'is_breeding_season': is_breeding,
                        'is_fire_season': is_fire
                    })
                    
    df_env = pd.DataFrame(env_records)

    try:
        engine = get_engine()
        with engine.begin() as conn:
            df_env.to_sql('dim_environment', conn, if_exists='append', index=False)
            print(f"--- {len(df_env)} Environmental logs loaded into 'dim_environment'. ---")
    except Exception as e:
        print(f"!!! Error during environment population: {e}")

if __name__ == "__main__":
    populate_dim_environment()