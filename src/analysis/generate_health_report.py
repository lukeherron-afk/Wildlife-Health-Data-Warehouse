import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import text

# Import our custom utilities
from src.utils.db_utils import get_engine
from src.utils.reporting_utils import set_capstone_theme, add_watermark

def get_seasonal_data(engine, species, is_standard=True):
    """Fetches analytical data from the warehouse using a Star Schema join."""
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
    """Applies specific styling to an individual subplot."""
    if df.empty:
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
        ax.set_title(title)
        return
    
    order = [
        'Summer', 'Autumn', 'Winter', 'Spring',
        'Burran', 'Marrai\'gang', 'Burrugin', 'Wiritjiribin',
        'Ngoonungi', 'Parra\'dowee'
    ]

    # Only plot seasons that actually exist in the data
    current_order = [s for s in order if s in df['season'].unique()]

    sns.barplot(
        data=df, x='season', y='health_status_score', 
        order=current_order, hue='season', palette=palette,
        ax=ax, legend=False, errorbar=None
    )
    
    ax.set_title(title)
    ax.set_ylim(0, 5.5)
    ax.set_ylabel('Avg Health Score (1-5)')
    ax.set_xlabel('Phenological Season')
    
    # Add data labels to the top of the bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)

def generate_report(species):
    """Generates and saves a comparative health report for a specific species."""
    print(f"Generating analytics for {species}...")
    engine = get_engine()
    
    # Apply our capstone visual theme
    set_capstone_theme()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    datasets = [
        (ax1, get_seasonal_data(engine, species, True), 'Standard Seasons', 'viridis'),
        (ax2, get_seasonal_data(engine, species, False), "D'harawal Phenological Seasons", 'magma')
    ]

    for ax, df, title, palette in datasets:
        style_subplot(ax, df, title, palette)

    fig.suptitle(f'Longitudinal Health Trend Analysis: {species} (NSW)', fontsize=16)
    
    # Add our custom academic watermark to both subplots
    add_watermark(ax1)
    add_watermark(ax2)
    
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save the figure ready for Word insertion
    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)
    
    # Create the safe file path
    filename = f'Health_Report_{species.replace(" ", "_")}.png'
    filepath = os.path.join(docs_dir, filename)
    
    # Save the figure to the new path
    fig.savefig(filepath)
    print(f"Successfully saved '{filepath}'")
    plt.close(fig) # Close the figure to free up memory

def batch_generate_all():
    """Generates reports for all species in the database."""
    engine = get_engine()
    with engine.connect() as conn:
        # Query the database to find all unique species
        result = conn.execute(text("SELECT DISTINCT species_name FROM dim_animal"))
        all_species = [row[0] for row in result.fetchall()]
        
    print(f"Found {len(all_species)} species. Beginning batch generation...")
    for species in all_species:
        generate_report(species)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate seasonal health reports for specific wildlife species.")
    parser.add_argument("--species", type=str, default="All", help="Species name (e.g., Koala) or 'All' to batch generate.")
    
    args = parser.parse_args()
    
    if args.species.lower() == "all":
        batch_generate_all()
    else:
        generate_report(args.species)