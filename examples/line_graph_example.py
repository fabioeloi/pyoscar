"""
Line Graph Example

This example demonstrates how to create and use a LineGraph
for visualizing time-series data.
"""

import numpy as np
import matplotlib.pyplot as plt
from pyoscar.core import GraphView
from pyoscar.graphs import LineGraph

def main():
    # Create a graph view to hold our graphs
    view = GraphView("Example View")
    
    # Create a line graph
    line_graph = LineGraph("Temperature", "Temperature Over Time", "°C")
    
    # Generate some sample data
    x = np.linspace(0, 10, 100)  # Time points
    y1 = 20 + 5 * np.sin(x)      # Temperature series 1
    y2 = 22 + 3 * np.cos(x)      # Temperature series 2
    
    # Add data to the graph
    line_graph.add_data(x, y1, "Sensor 1")
    line_graph.add_data(x, y2, "Sensor 2")
    
    # Set line styles
    line_graph.set_line_style("Sensor 1", color="red", line_width=2, marker='o', marker_size=4)
    line_graph.set_line_style("Sensor 2", color="blue", line_width=2, marker='s', marker_size=4)
    
    # Set axis labels
    line_graph.set_x_label("Time (s)")
    line_graph.set_y_label("Temperature (°C)")
    
    # Add the graph to the view
    view.add_graph(line_graph)
    
    # Add a second graph for demonstration
    line_graph2 = LineGraph("Humidity", "Humidity Over Time", "%")
    
    # Generate sample humidity data
    y3 = 60 + 10 * np.sin(x/2)  # Humidity data
    
    # Add data to the second graph
    line_graph2.add_data(x, y3, "Humidity")
    
    # Set line style
    line_graph2.set_line_style("Humidity", color="green", line_width=2)
    
    # Set axis labels
    line_graph2.set_x_label("Time (s)")
    line_graph2.set_y_label("Humidity (%)")
    
    # Add the second graph to the view
    view.add_graph(line_graph2)
    
    # Render the view
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    view.render(fig, axes)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
