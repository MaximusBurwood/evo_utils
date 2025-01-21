import pandas as pd
import numpy as np
import os

# Constants/Parameters
NUM_GENOTYPES = 100    # Number of unique genotypes
NUM_PHENOTYPES = 100   # Number of unique phenotypes
DECAY_RATE = 0.1      # Rate of exponential decay for fitness landscape
NOISE_STD = 0.05      # Standard deviation of random noise

file_path = "Python/fitness_landscape/fitness_landscape_data.csv"  # File to save data

def calculate_fitness(genotypes, phenotypes):
    # Calculate fitness values for genotype-phenotype pairs
    return (
        np.sin(genotypes) * np.cos(phenotypes)  # Oscillatory base
        * np.exp(-DECAY_RATE * (genotypes + phenotypes))  # Exponential decay
        + np.random.normal(0, NOISE_STD, size=len(genotypes))  # Random noise
    )

def generate_fitness_landscape_data(file_path):
    # Generate unique genotypes and phenotypes
    genotypes = np.arange(1, NUM_GENOTYPES + 1)
    phenotypes = np.arange(1, NUM_PHENOTYPES + 1)
    
    # Create a grid of genotype-phenotype pairs
    genotype_grid, phenotype_grid = np.meshgrid(genotypes, phenotypes)
    genotype_flat = genotype_grid.flatten()
    phenotype_flat = phenotype_grid.flatten()
    
    # Calculate fitness values
    fitness = calculate_fitness(genotype_flat, phenotype_flat)
    
    # Create and save DataFrame
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data = pd.DataFrame({
        "Genotype": genotype_flat,
        "Phenotype": phenotype_flat,
        "Fitness": fitness
    })
    data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    np.random.seed(42)
    generate_fitness_landscape_data(file_path)