import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

file_path = 'Python/fitness_landscape/fitness_landscape_data.csv'

# Load fitness landscape data
def load_fitness_landscape(file_name):
    try:
        data = pd.read_csv(file_name)
        if not {'Genotype', 'Phenotype', 'Fitness'}.issubset(data.columns):
            raise ValueError("CSV must contain columns: 'Genotype', 'Phenotype', 'Fitness'")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Plot fitness landscape
def plot_fitness_landscape(data):
    # Create a grid
    X_unique = np.sort(data['Genotype'].unique())
    Y_unique = np.sort(data['Phenotype'].unique())
    X_grid, Y_grid = np.meshgrid(X_unique, Y_unique)

    # Interpolate Z values for the grid
    Z_grid = np.zeros_like(X_grid, dtype=float)
    for i in range(len(X_unique)):
        for j in range(len(Y_unique)):
            match = data[(data['Genotype'] == X_unique[i]) & (data['Phenotype'] == Y_unique[j])]
            Z_grid[j, i] = match['Fitness'].iloc[0] if not match.empty else np.nan

    # Create finer grid for smoothing
    X_fine = np.linspace(X_unique.min(), X_unique.max(), 100)
    Y_fine = np.linspace(Y_unique.min(), Y_unique.max(), 100)
    X_fine_grid, Y_fine_grid = np.meshgrid(X_fine, Y_fine)

    # Interpolate to finer grid
    Z_fine_grid = griddata(
        (X_grid.flatten(), Y_grid.flatten()), 
        Z_grid.flatten(), 
        (X_fine_grid, Y_fine_grid), 
        method='cubic'
    )

    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(
        x=X_fine_grid,
        y=Y_fine_grid,
        z=Z_fine_grid,
        colorscale='viridis'
    )])

    # Update the layout
    fig.update_layout(
        title='Fitness Landscape',
        scene=dict(
            xaxis_title='Genotype',
            yaxis_title='Phenotype',
            zaxis_title='Fitness'
        ),
        width=1000,
        height=700
    )

    # Show the plot
    fig.show()

# Main script
if __name__ == "__main__":
    data = load_fitness_landscape(file_path)
    if data is not None:
        plot_fitness_landscape(data)