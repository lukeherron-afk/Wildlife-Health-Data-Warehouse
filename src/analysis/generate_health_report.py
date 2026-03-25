import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found!")
    return create_engine(db_url)

def get_seasonal_data(engine, species, is_standard=True):
    condition = "IN" if is_standard else "NOT IN"
    
    query = text(f"""
        SELECT e.phenological_season_name AS season, f.health_status_score
        FROM fact_observations f
        JOIN dim_environment e ON f.env_id = e.env_id
        JOIN dim_animal a ON f.animal_id = a.animal_id
        WHERE e.state = 'NSW' 
        AND a.species_name = :species
        AND e.phenological_season_name {condition} ('Summer', 'Autumn', 'Winter', 'Spring');
    """)
    return pd.read_sql(query, engine, params={"species": species})

def style_subplot(ax, df, title, palette):
    if df.empty:
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
        ax.set_title(title)
        return
    
    order = [
        'Summer', 'Autumn', 'Winter', 'Spring',
        'Burran', 'Marrai\'gang', 'Burruggang', 'Wiritjiribin',
        'Ngoonungi', 'Parra\'dowee'
    ]

    current_order = [s for s in order if s in df['season'].unique()]

    sns.barplot(
        data=df, x='season', y='health_status_score', 
        order=current_order, hue='season', palette=palette,
        ax=ax, legend=False, errorbar=None
    )
    ax.set_title(title, fontsize=14)
    ax.set_ylim(0, 5.5)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)

def generate_report(species):
    engine = get_engine()
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    datasets = [
        (ax1, get_seasonal_data(engine, species, True), 'Standard Seasons', 'viridis'),
        (ax2, get_seasonal_data(engine, species, False), 'D\'harawal Phenological Seasons', 'magma')
    ]

    for ax, df, title, palette in datasets:
        style_subplot(ax, df, title, palette)

    fig.suptitle(f'Average Health Score: {species} (NSW)', fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    
    filename = f'Health_Report_{species.replace(" ", "_")}.png'
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Successfully saved report as '{filename}'")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate seasonal health reports for specific wildlife species.")
    parser.add_argument("--species", type=str, default="Koala", help="Species name (e.g., Koala, Kangaroo)")
    
    args = parser.parse_args()
    generate_report(args.species)