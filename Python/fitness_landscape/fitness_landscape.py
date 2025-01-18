import pandas as pd
import numpy as np
import os

file_path = 'Python/fitness_landscape/fitness_landscape_data.csv'

# Generate synthetic fitness landscape data
def generate_fitness_landscape(file_path, num_genotypes=100, num_phenotypes=100, seed=42):
    
    np.random.seed(seed)
    
    # Generate unique genotypes and phenotypes
    genotypes = np.arange(1, num_genotypes + 1)
    phenotypes = np.arange(1, num_phenotypes + 1)
    
    # Create a grid of genotype-phenotype pairs
    genotype_grid, phenotype_grid = np.meshgrid(genotypes, phenotypes)
    
    # Flatten the grid for DataFrame construction
    genotype_flat = genotype_grid.flatten()
    phenotype_flat = phenotype_grid.flatten()
    
    # Generate fitness values with a sparse, rugged landscape
    fitness = (
        np.sin(genotype_flat) * np.cos(phenotype_flat)  # Oscillatory base
        * np.exp(-0.1 * (genotype_flat + phenotype_flat))  # Exponential decay for sparsity
        + np.random.normal(0, 0.05, size=len(genotype_flat))  # Small random noise
    )
    
    # Create the DataFrame
    data = pd.DataFrame({
        "Genotype": genotype_flat,
        "Phenotype": phenotype_flat,
        "Fitness": fitness
    })
    
    # Save the DataFrame as a CSV file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

# Main script
if __name__ == "__main__":
    generate_fitness_landscape(file_path)