import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("!!! DATABASE_URL not found in .env file!")

engine = create_engine(db_url)

def get_australian_season(month):                                                           # TODO: To be improved, too rough of an estimate
    if month in [12, 1, 2]: return 'Summer'
    if month in [3, 4, 5]: return 'Autumn'
    if month in [6, 7, 8]: return 'Spring'
    return 'Spring'

    #? Can pull actual temperature and rainfall data from the Bureau of Meteorology (BOM) to confirm the season. Need to add more coloumns into the observations table to detail this.
    #? Maybe can do it by tracking data? Although seems very complex and time wasteful. e.g. breeding season, migration season, etc.
    #* A season starts when the 7-day rolling average temperature hits a certain threshold.

def populate_dim_date():
    print("Populating Date Dimension...")

    start_date = '2024-01-01'
    end_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')                  #* Future proofing. Basically today + 1 year.
    dates = pd.date_range(start_date, end_date)

    df_date = pd.DataFrame({'full_date': dates})

    df_date['date_id'] = df_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    df_date['day_of_week'] = df_date['full_date'].dt.day_name()
    df_date['month_name'] = df_date['full_date'].dt.month_name()
    df_date['calendar_year'] = df_date['full_date'].dt.year
    df_date['season'] = df_date['full_date'].dt.month.apply(get_australian_season)

    try:
        df_date.to_sql('dim_date', engine, if_exists='append', index=False)
        print(f"--- {len(df_date)} days loaded into 'dim_date'. ---")
    except Exception as e:
        print(f"!!! Error during date population: {e}")

if __name__ == "__main__":
    populate_dim_date()
