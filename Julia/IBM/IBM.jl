using EvoId
using Plots

# --------------------------
# Customisable Parameters
# --------------------------
Base.@kwdef struct ModelParams
    population_size = 100      # Initial number of individuals
    world_size = (20, 20)      # Size of the 2D environment
    mutation_rate = 0.01       # Probability of mutation per reproduction
    selection_strength = 0.2   # Strength of selection pressure
    resource_abundance = 0.5   # Base resource availability
    metabolic_rate = 0.1       # Energy consumption rate
    max_generations = 500      # Simulation length
end

# --------------------------
# Agent Definition
# --------------------------
@kwdef mutable struct MyAgent <: AbstractAgent
    id::Int                     # Unique identifier
    pos::NTuple{2,Float64}      # Position in 2D space
    energy::Float64 = 1.0       # Energy reserves
    trait::Float64 = 0.5        # Evolving phenotypic trait (0-1)
    genome::Float64 = 0.5       # Genetic value (subject to mutation)
end

# --------------------------
# World Setup
# --------------------------
function create_world(params)
    # Initialize 2D grid world with resources
    world = World(params.world_size, 
                agent=MyAgent, 
                resource=params.resource_abundance)
    return world
end

# --------------------------
# Evolutionary Processes
# --------------------------

# Movement rule
function movement_rule!(agent::MyAgent, world)
    # Random walk with momentum influenced by trait
    new_pos = agent.pos .+ (randn(2) .* (1 - agent.trait))
    agent.pos = clamp_pos(new_pos, world)
end

# Resource collection
function collect_resources!(agent::MyAgent, world)
    resource = get_resource(world, agent.pos)
    agent.energy += resource * agent.trait - params.metabolic_rate
    set_resource!(world, agent.pos, resource * 0.8)  # Deplete resource
end

# Fitness function (customizable selection)
function calculate_fitness(agent::MyAgent)
    # Stabilizing selection around optimal trait value 0.7
    optimal_trait = 0.7
    fitness = exp(-params.selection_strength * (agent.trait - optimal_trait)^2)
    return fitness
end

# Reproduction with mutation
function reproduce!(parent::MyAgent, world)
    if rand() < params.mutation_rate
        child_genome = parent.genome + randn() * 0.1
    else
        child_genome = parent.genome
    end
    
    child = MyAgent(
        id = get_new_id(world),
        pos = parent.pos,
        energy = parent.energy * 0.5,
        trait = clamp(child_genome, 0.0, 1.0),
        genome = child_genome
    )
    
    parent.energy *= 0.5  # Parent invests energy in offspring
    return child
end

# --------------------------
# Simulation Loop
# --------------------------
function run_simulation(params)
    # Initialize world and population
    world = create_world(params)
    initialize_population!(world, params.population_size)
    
    # Data collection
    trait_history = Float64[]
    population_history = Int[]
    
    for gen in 1:params.max_generations
        # Agent behaviors
        for agent in get_agents(world)
            movement_rule!(agent, world)
            collect_resources!(agent, world)
        end
        
        # Selection and reproduction
        fitness_scores = calculate_fitness.(get_agents(world))
        selected_ids = sample(
            get_ids(world), 
            Weights(fitness_scores), 
            length(get_agents(world))
        )
        
        # Create new generation
        new_agents = [reproduce!(get_agent(world, id), world) for id in selected_ids]
        update_population!(world, new_agents)
        
        # Record statistics
        push!(trait_history, mean([a.trait for a in get_agents(world)]))
        push!(population_history, length(get_agents(world)))
        
        # Check for extinction
        if isempty(get_agents(world))
            println("Population went extinct at generation $gen")
            break
        end
    end
    
    return trait_history, population_history
end

# --------------------------
# Execution and Visualization
# --------------------------
# Create parameter set
params = ModelParams(
    population_size = 50,
    mutation_rate = 0.05,
    selection_strength = 0.5,
    max_generations = 200
)

# Run simulation
trait_history, population_history = run_simulation(params)

# Plot results
p1 = plot(trait_history, 
        xlabel="Generation", 
        ylabel="Mean Trait Value", 
        title="Trait Evolution")
        
p2 = plot(population_history, 
        xlabel="Generation", 
        ylabel="Population Size", 
        title="Population Dynamics")
        
plot(p1, p2, layout=(2,1))