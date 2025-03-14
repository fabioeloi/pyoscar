"""
PyOSCAR Simple Demo

This script demonstrates a basic visualization using the PyOSCAR library.
It creates a simple dashboard with a line graph and a bar graph.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to the path so we can import PyOSCAR modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import from the local modules
from core import GraphView
from graphs import LineGraph, BarGraph

def main():
    # Create a graph view
    view = GraphView("PyOSCAR Demo")
    
    # Create a line graph
    line_graph = LineGraph("Temperature", "Temperature Over Time", "°C")
    
    # Generate some sample data
    x = np.linspace(0, 10, 100)
    y = 25 + 5 * np.sin(x) + np.random.normal(0, 0.5, len(x))
    
    # Add data to the graph
    line_graph.add_data(x, y)
    
    # Style the line
    line_graph.set_line_style(color="blue", line_width=2)
    
    # Set axis labels
    line_graph.set_x_label("Time (hours)")
    line_graph.set_y_label("Temperature (°C)")
    
    # Add the graph to the view
    view.add_graph(line_graph)
    
    # Create a bar graph
    bar_graph = BarGraph("Energy", "Energy Consumption", "kWh")
    
    # Create some bar data
    categories = ["Morning", "Afternoon", "Evening", "Night"]
    values = [45, 60, 75, 30]
    
    # Add data to the bar graph
    bar_graph.add_data(np.arange(len(categories)), values)
    bar_graph.set_categories(categories)
    
    # Style the bars
    bar_graph.set_bar_style(color="green", alpha=0.7)
    
    # Set axis labels
    bar_graph.set_x_label("Time of Day")
    bar_graph.set_y_label("Energy (kWh)")
    
    # Add the bar graph to the view
    view.add_graph(bar_graph)
    
    # Render the view
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    view.render(fig, axes)
    
    # Add a title to the figure
    fig.suptitle("PyOSCAR Visualization Demo", fontsize=16)
    
    # Add some spacing
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
    print("Demo completed successfully!")
