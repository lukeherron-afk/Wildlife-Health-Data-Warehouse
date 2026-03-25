import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("!!! DATABASE_URL not found in .env file!")

engine = create_engine(db_url)

def get_seasonal_data(engine, is_standard=True):
    condition = "IN" if is_standard else "NOT IN"
    query = f"""
        SELECT e.phenological_season_name AS season, f.health_status_score
        FROM fact_observations f
        JOIN dim_environment e ON f.env_id = e.env_id
        WHERE e.state = 'NSW' 
        AND e.phenological_season_name {condition} ('Summer', 'Autumn', 'Winter', 'Spring');
    """
    return pd.read_sql(query, engine)

def style_subplot(ax, df, title, palette):
    sns.barplot(
        data=df, x='season', y='health_status_score', 
        hue='season', palette=palette, ax=ax, 
        legend=False, errorbar=None
    )
    ax.set_title(title, fontsize=14)
    ax.set_ylim(0, 5.5)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)

def generate_report():
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    datasets = [
        (ax1, get_seasonal_data(engine, True), 'Standard Seasons', 'viridis'),
        (ax2, get_seasonal_data(engine, False), 'D\'harawal Phenological Seasons', 'magma')
    ]

    for ax, df, title, palette in datasets:
        style_subplot(ax, df, title, palette)

    fig.suptitle('Average Wildlife Health Score by Season (NSW)', fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    
    fig.savefig('Seasonal_Health_Report.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    generate_report()