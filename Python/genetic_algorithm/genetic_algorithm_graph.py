import pandas as pd
import plotly.graph_objects as go

# File location
file_path = "Python/genetic_algorithm/genetic_algorithm_data.csv"

# Load the data from the CSV
data = pd.read_csv(file_path)

# Extract data for plotting
generations = data["Generation"]
best_fitness = data["Best_Fitness"]
median_fitness = data["Median_Fitness"]
worst_fitness = data["Worst_Fitness"]

# Create a Plotly figure
fig = go.Figure()

# Add traces for each fitness type
fig.add_trace(go.Scatter(
    x=generations, y=best_fitness,
    mode='lines+markers', name='Best Fitness',
    line=dict(color='green', width=2)
))

fig.add_trace(go.Scatter(
    x=generations, y=median_fitness,
    mode='lines+markers', name='Median Fitness',
    line=dict(color='blue', width=2)
))

fig.add_trace(go.Scatter(
    x=generations, y=worst_fitness,
    mode='lines+markers', name='Worst Fitness',
    line=dict(color='red', width=2)
))

# Customise the layout
fig.update_layout(
    title="Genetic Algorithm Fitness Over Generations",
    xaxis_title="Generation",
    yaxis_title="Fitness Value",
    template="plotly_white",
    legend_title="Fitness Type",
    font=dict(family="Arial", size=12),
    yaxis=dict(tickformat="~s")  # Format y-axis to handle large numbers
)

# Show the plot
fig.show()