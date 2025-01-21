import pandas as pd
import plotly.graph_objects as go

# File location
file_path = "Python/lotka-volterra/lotka-volterra_data.csv"

# Load the data from the CSV
data = pd.read_csv(file_path)
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Time"], y=data["Prey"], mode="lines", name="Prey"))
fig.add_trace(go.Scatter(x=data["Time"], y=data["Predator"], mode="lines", name="Predator"))
fig.update_layout(title="Lotka-Volterra Model", xaxis_title="Time", yaxis_title="Population")
fig.show()