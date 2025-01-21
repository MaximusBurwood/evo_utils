import numpy as np
import os

# Constants/Parameters
CHROMOSOME_LENGTH = 16    # Length of binary representation of individuals
POPULATION_SIZE = 128     # Number of individuals in the population 
MUTATION_RATE = 0.05     # Probability of mutation for each bit
CROSSOVER_RATE = 0.8     # Probability of crossover
GENERATIONS = 100        # Number of generations to evolve

file_path = "Python/genetic_algorithm/genetic_algorithm_data.csv"  # File to save data

def fitness_function(chromosome):
    # Calculate the fitness of a chromosome (maximise x^2)
    x = int(''.join(map(str, chromosome)), 2)  # Convert binary to decimal
    return x ** 2

def create_individual():
    # Generate a random individual (binary chromosome)
    return np.random.randint(2, size=CHROMOSOME_LENGTH).tolist()

def create_population():
    # Create an initial population of random individuals
    return [create_individual() for _ in range(POPULATION_SIZE)]

def select_parent(population, fitness_scores):
    # Select a parent using roulette wheel selection
    total_fitness = sum(fitness_scores)
    selection_probabilities = [score / total_fitness for score in fitness_scores]
    return population[np.random.choice(range(len(population)), p=selection_probabilities)]

def crossover(parent1, parent2):
    # Perform single-point crossover between two parents
    if np.random.rand() < CROSSOVER_RATE:
        point = np.random.randint(1, CHROMOSOME_LENGTH)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

def mutate(chromosome):
    # Mutate a chromosome with a given mutation rate
    return [bit ^ 1 if np.random.rand() < MUTATION_RATE else bit for bit in chromosome]

def generate_genetic_algorithm_data(file_path):
    # Initialize population
    population = create_population()
    
    # Prepare the output file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write("Generation,Best_Fitness,Median_Fitness,Worst_Fitness\n")

    for generation in range(GENERATIONS):
        # Evaluate fitness
        fitness_scores = [fitness_function(individual) for individual in population]
        
        # Sort individuals by fitness
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1])
        population, fitness_scores = zip(*sorted_population)
        
        # Track statistics
        best_fitness = fitness_scores[-1]
        median_fitness = fitness_scores[len(population) // 2]
        worst_fitness = fitness_scores[0]
        
        # Save the data
        with open(file_path, "a") as file:
            file.write(f"{generation + 1},{best_fitness},{median_fitness},{worst_fitness}\n")
        
        # Create new population
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_scores)
            parent2 = select_parent(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2))
                
        population = new_population
    
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    np.random.seed(42)
    generate_genetic_algorithm_data(file_path)
