import matplotlib.pyplot as plt
import seaborn as sns

def set_capstone_theme():
    """
    Configures a standardised, professional visual theme for all capstone report figures.
    Call this function before generating any plots.
    """
    # Use a clean, modern seaborn style
    sns.set_theme(style="whitegrid", palette="muted")
    
    # Customise matplotlib parameters for academic reporting
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.titleweight': 'bold',
        'figure.dpi': 300,        # High resolution for word documents
        'savefig.bbox': 'tight'   # Removes wasted white space around edges
    })

def add_watermark(ax, text="UTS Capstone Prototype: Wildlife Health Data Warehouse"):
    """
    Adds a subtle watermark to the bottom right of a plot.
    """
    ax.text(0.99, 0.01, text,
            transform=ax.transAxes, color='grey', alpha=0.5,
            fontsize=8, ha='right', va='bottom')