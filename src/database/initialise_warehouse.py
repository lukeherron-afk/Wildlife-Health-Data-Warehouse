from sqlalchemy import text

from src.utils import get_engine

sql_dim_date = """
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE UNIQUE,
    day_of_week VARCHAR(10),
    month_name VARCHAR(15),
    calendar_year INTEGER,
    season VARCHAR(15)
);
"""

sql_dim_animal = """
CREATE TABLE IF NOT EXISTS dim_animal (
    animal_id SERIAL PRIMARY KEY,
    species_name VARCHAR(100) NOT NULL,
    sex VARCHAR(1) CHECK (sex IN ('M', 'F', 'U')),
    estimated_age INTEGER
);
"""

sql_dim_location = """
CREATE TABLE IF NOT EXISTS dim_location (
    location_id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    indigenous_land_name VARCHAR(100) NOT NULL,
    state VARCHAR(3) CHECK (state IN ('NSW', 'QLD', 'VIC', 'TAS', 'SA', 'WA', 'NT', 'ACT')), 
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    site_type VARCHAR(50)
);
"""

sql_dim_agency = """
CREATE TABLE IF NOT EXISTS dim_agency (
    agency_id SERIAL PRIMARY KEY,
    agency_name VARCHAR(150) NOT NULL UNIQUE,
    agency_type VARCHAR(50)
);
"""

sql_dim_environment = """
CREATE TABLE IF NOT EXISTS dim_environment (
    env_id SERIAL PRIMARY KEY,
    state VARCHAR(3) CHECK (state IN ('NSW', 'QLD', 'VIC', 'TAS', 'SA', 'WA', 'NT', 'ACT')), 
    climate_zone VARCHAR(50),
    phenological_season_name VARCHAR(100),
    is_breeding_season BOOLEAN,
    is_fire_season BOOLEAN
);
"""

sql_fact_observations = """
CREATE TABLE IF NOT EXISTS fact_observations (
    observation_id SERIAL PRIMARY KEY,
    date_id INTEGER REFERENCES dim_date(date_id),
    animal_id INTEGER REFERENCES dim_animal(animal_id),
    location_id INTEGER REFERENCES dim_location(location_id),
    agency_id INTEGER REFERENCES dim_agency(agency_id),
    env_id INTEGER REFERENCES dim_environment(env_id),
    body_temperature DECIMAL(4,2),
    weight DECIMAL(5,2),
    health_status_score SMALLINT CHECK (health_status_score BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_warehouse():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            print("Cleaning up warehouse...")

            # Drop tables in reverse order of dependencies (Fact first, then Dimensions)
            tables = [
                "fact_observations", "dim_date", "dim_animal", 
                "dim_location", "dim_agency", "dim_environment"
            ]

            for table in tables:
                conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
            
            conn.commit()

            print("Connecting to PostgreSQL...")
            
            conn.execute(text(sql_dim_date))
            conn.execute(text(sql_dim_animal))
            conn.execute(text(sql_dim_location))
            conn.execute(text(sql_dim_agency))
            conn.execute(text(sql_dim_environment))
            conn.execute(text(sql_fact_observations))
            
            conn.commit()
            print("Warehouse successfully initialized in 'wildlife_health'!")

    except Exception as e:
        print(f"!!! Pipeline Error during initialization: {e}")

if __name__ == "__main__":
    init_warehouse()