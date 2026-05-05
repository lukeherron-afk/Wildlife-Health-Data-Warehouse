import math
import random
import pandas as pd
from datetime import datetime, timedelta

# Clean import using our new module setup
from src.utils.db_utils import get_engine


# Simulates Australian daily temperatures using a cosine wave. Peaks around late January, lowest in late July.
def simulate_temperature_curve(df): 
    # 20 base temp, +/- 10 degrees amplitude, peaking at day 30 (Jan 30)
    df['day_of_year'] = df['full_date'].dt.dayofyear
    df['base_temp'] = df['day_of_year'].apply(
        lambda x: 20 + 10 * math.cos(2 * math.pi * (x - 30) / 365.25)
    )
    
    # Adding random noise (between -3 and +3 degrees)
    df['daily_temp'] = df['base_temp'] + df['base_temp'].apply(lambda x: random.uniform(-3, 3))
    
    return df

# Determines the season based on rolling temperatures and trajectory.
def get_australian_season(row):
    temp = row['rolling_temp']
    temp_change = row['temp_trajectory']
    
    if temp >= 23.0:
        return 'Summer'
    elif temp <= 16.0:
        return 'Winter'
    # If in the middle, determine season by checking if the earth is warming or cooling
    elif temp_change < 0: 
        return 'Autumn'
    else:
        return 'Spring'

def populate_dim_date():
    print("Populating Date Dimension with rolling temperature logic...")

    # The date range
    start_date = '2024-01-01'
    end_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    dates = pd.date_range(start_date, end_date)

    df_date = pd.DataFrame({'full_date': dates})

    # Dimension Columns
    df_date['date_id'] = df_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    df_date['day_of_week'] = df_date['full_date'].dt.day_name()
    df_date['month_name'] = df_date['full_date'].dt.month_name()
    df_date['calendar_year'] = df_date['full_date'].dt.year

    # --- ADVANCED SEASON LOGIC (DSR Prototype Feature) ---
    df_date = simulate_temperature_curve(df_date)
    
    # Calculate 7-day rolling average (min_periods=1 handles the first 6 days)
    df_date['rolling_temp'] = df_date['daily_temp'].rolling(window=7, min_periods=1).mean()
    
    # Calculate trajectory to differentiate Spring (warming) from Autumn (cooling) by comparing today's rolling average to the rolling average 14 days ago
    df_date['temp_trajectory'] = df_date['rolling_temp'].diff(periods=14).fillna(0)
    
    df_date['season'] = df_date.apply(get_australian_season, axis=1)

    # Dropping temp columns to not break the SQL insert
    df_date = df_date.drop(columns=['day_of_year', 'base_temp', 'daily_temp', 'rolling_temp', 'temp_trajectory'])

    try:
        engine = get_engine()
        
        with engine.begin() as conn:
            df_date.to_sql('dim_date', conn, if_exists='append', index=False)
            print(f"--- {len(df_date)} days loaded into 'dim_date'. ---")
    except Exception as e:
        print(f"!!! Error during date population: {e}")

if __name__ == "__main__":
    populate_dim_date()