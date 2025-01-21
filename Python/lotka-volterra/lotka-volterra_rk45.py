import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import os

ALPHA = 0.1        # Prey growth rate
BETA = 0.0005      # Predation rate
DELTA = 0.0001     # Predator reproduction rate
GAMMA = 0.05       # Predator death rate
X0 = 2500          # Initial prey population
Y0 = 100            # Initial predator population
T_SPAN = (0, 1000) # Time interval
T_STEPS = 50000   # Number of time steps

file_path = "Python/lotka-volterra/lotka-volterra_data.csv"  # File to save data

def lotka_volterra(t, z, alpha, beta, delta, gamma):
    # Calculate the rate of change for prey and predator populations
    x, y = z  # Prey (x) and predator (y) populations
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

def generate_lotka_volterra_data(file_path, alpha, beta, delta, gamma, x0, y0, t_span, t_steps):
    # Generate time points for integration
    t_eval = np.linspace(t_span[0], t_span[1], t_steps)
    
    # Solve the system of equations using RK45 method
    solution = solve_ivp(
        lotka_volterra, 
        t_span, 
        [x0, y0], 
        args=(alpha, beta, delta, gamma), 
        t_eval=t_eval,
        method='RK45'
    )
    
    # Extract results
    t = solution.t
    x = solution.y[0]  # Prey population
    y = solution.y[1]  # Predator population
    
    # Create and save DataFrame
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df = pd.DataFrame({'Time': t, 'Prey': x, 'Predator': y})
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    np.random.seed(42)
    generate_lotka_volterra_data(
        file_path,
        ALPHA, BETA, DELTA, GAMMA,
        X0, Y0,
        T_SPAN, T_STEPS
    )