import random

CHROMOSOME_LENGTH = 16  # Length of binary representation of individuals
POPULATION_SIZE = 128   # Number of individuals in the population
MUTATION_RATE = 0.05    # Probability of mutation for each bit
CROSSOVER_RATE = 0.8    # Probability of crossover
GENERATIONS = 100      # Number of generations to evolve

file_path = "Python/genetic_algorithm/genetic_algorithm_data.csv"  # File to save data for graphing

def fitness_function(chromosome):
    """Calculate the fitness of a chromosome (maximize x^2)."""
    x = int(''.join(map(str, chromosome)), 2)  # Convert binary to decimal
    return x ** 2

def create_individual():
    """Generate a random individual (binary chromosome)."""
    return [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]

def create_population():
    """Create an initial population of random individuals."""
    return [create_individual() for _ in range(POPULATION_SIZE)]

def select_parent(population, fitness_scores):
    """Select a parent using roulette wheel selection."""
    total_fitness = sum(fitness_scores)
    selection_probabilities = [score / total_fitness for score in fitness_scores]
    return population[random.choices(range(len(population)), weights=selection_probabilities, k=1)[0]]

def crossover(parent1, parent2):
    """Perform single-point crossover between two parents."""
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

def mutate(chromosome):
    """Mutate a chromosome with a given mutation rate."""
    return [bit ^ 1 if random.random() < MUTATION_RATE else bit for bit in chromosome]

def genetic_algorithm():
    """Run the Genetic Algorithm."""
    # Initialize population
    population = create_population()

    # Prepare the output file
    with open(file_path, "w") as file:
        file.write("Generation,Best_Fitness,Median_Fitness,Worst_Fitness\n")

    for generation in range(GENERATIONS):
        # Evaluate fitness
        fitness_scores = [fitness_function(individual) for individual in population]

        # Sort individuals by fitness
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1])
        population, fitness_scores = zip(*sorted_population)

        # Track the best, median, and worst individuals
        best_individual = population[-1]
        best_fitness = fitness_scores[-1]
        median_individual = population[len(population) // 2]
        median_fitness = fitness_scores[len(population) // 2]
        worst_individual = population[0]
        worst_fitness = fitness_scores[0]

        print(f"Generation {generation + 1}: Best fitness = {best_fitness}, Best individual = {''.join(map(str, best_individual))}")
        print(f"                   Median fitness = {median_fitness}, Median individual = {''.join(map(str, median_individual))}")
        print(f"                   Worst fitness = {worst_fitness}, Worst individual = {''.join(map(str, worst_individual))}")

        # Save the data to the file
        with open(file_path, "a") as file:
            file.write(f"{generation + 1},{best_fitness},{median_fitness},{worst_fitness}\n")

        # Create a new population through selection, crossover, and mutation
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_scores)
            parent2 = select_parent(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2))

        population = new_population

    # Return the best solution found
    return max(population, key=fitness_function)

if __name__ == "__main__":
    best_solution = genetic_algorithm()
    print(f"Best solution: {''.join(map(str, best_solution))}, Fitness = {fitness_function(best_solution)}")