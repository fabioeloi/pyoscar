"""
Bar Graph Example

This example demonstrates how to create and use a BarGraph
for visualizing categorical data.
"""

import numpy as np
import matplotlib.pyplot as plt
from pyoscar.core import GraphView
from pyoscar.graphs import BarGraph

def main():
    # Create a graph view to hold our graphs
    view = GraphView("Bar Chart Example")
    
    # Create a bar graph
    bar_graph = BarGraph("Sales", "Monthly Sales Data", "$")
    
    # Define categories and data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales_data = [12500, 17800, 14300, 19500, 21200, 15800]
    
    # Add data to the graph
    x_positions = np.arange(len(months))
    bar_graph.add_data(x_positions, sales_data)
    
    # Set categories for x-axis
    bar_graph.set_categories(months)
    
    # Set bar style
    bar_graph.set_bar_style(color="skyblue", edge_color="navy", alpha=0.8)
    
    # Set axis labels
    bar_graph.set_x_label("Month")
    bar_graph.set_y_label("Sales ($)")
    
    # Add the graph to the view
    view.add_graph(bar_graph)
    
    # Create a second bar graph showing comparison data
    comparison_graph = BarGraph("Sales Comparison", "2022 vs 2023 Monthly Sales", "$")
    
    # Sample data for comparison
    sales_2022 = [11200, 16300, 13100, 18000, 19500, 14200]
    sales_2023 = sales_data  # Reuse the data from above
    
    # Add both datasets
    comparison_graph.add_data(x_positions, sales_2022, "2022")
    comparison_graph.add_data(x_positions + 0.3, sales_2023, "2023")  # Offset x positions for side-by-side bars
    
    # Set categories and bar width
    comparison_graph.set_categories(months)
    comparison_graph.set_bar_width(0.4)  # Narrower bars to fit side by side
    
    # Set different styles for each series
    comparison_graph.set_bar_style("2022", color="lightblue", edge_color="blue", alpha=0.7)
    comparison_graph.set_bar_style("2023", color="lightgreen", edge_color="green", alpha=0.7)
    
    # Set axis labels
    comparison_graph.set_x_label("Month")
    comparison_graph.set_y_label("Sales ($)")
    
    # Add the second graph to the view
    view.add_graph(comparison_graph)
    
    # Render the view
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    view.render(fig, axes)
    
    # Add a legend to the second graph
    handles = [
        plt.Rectangle((0,0), 1, 1, color="lightblue", edgecolor="blue"),
        plt.Rectangle((0,0), 1, 1, color="lightgreen", edgecolor="green")
    ]
    axes[1].legend(handles, ["2022", "2023"], loc="upper right")
    
    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
