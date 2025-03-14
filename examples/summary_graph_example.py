"""
Summary Graph Example

This example demonstrates how to create and use a SummaryGraph
for visualizing statistical summaries similar to OSCAR's summary charts.
"""

import numpy as np
import matplotlib.pyplot as plt
from pyoscar.core import GraphView
from pyoscar.graphs import SummaryGraph

def main():
    # Create a graph view to hold our graphs
    view = GraphView("Summary Statistics Example")
    
    # Create a summary graph
    summary_graph = SummaryGraph("Blood Pressure", "Blood Pressure Readings by Patient", "mmHg")
    
    # Generate some sample data (simulating blood pressure readings for different patients)
    np.random.seed(42)  # For reproducible results
    
    # Generate data for 5 patients with different distributions
    patient_data = {
        "Patient A": 120 + np.random.normal(0, 5, 20),  # Normal around 120 with low variance
        "Patient B": 135 + np.random.normal(0, 8, 25),  # Higher BP with more variance
        "Patient C": 110 + np.random.normal(0, 3, 15),  # Lower BP with less variance 
        "Patient D": 145 + np.random.normal(0, 12, 30), # High BP with high variance
        "Patient E": 125 + np.random.normal(0, 7, 22)   # Moderate BP with moderate variance
    }
    
    # Add each patient's data to the summary graph
    for patient, data in patient_data.items():
        summary_graph.add_data_point(patient, data)
    
    # Configure the summary graph
    summary_graph.set_color_scheme("blue")
    summary_graph.set_percentile_ranges([(25, 75), (10, 90)])  # Show 25-75 and 10-90 percentile ranges
    
    # Set axis labels
    summary_graph.set_x_label("Patient")
    summary_graph.set_y_label("Systolic Blood Pressure (mmHg)")
    
    # Add the graph to the view
    view.add_graph(summary_graph)
    
    # Create a second summary graph for comparison
    summary_graph2 = SummaryGraph("Heart Rate", "Heart Rate Readings by Patient", "bpm")
    
    # Generate heart rate data for the same patients
    heart_rate_data = {
        "Patient A": 72 + np.random.normal(0, 4, 20),
        "Patient B": 80 + np.random.normal(0, 6, 25),
        "Patient C": 68 + np.random.normal(0, 3, 15),
        "Patient D": 88 + np.random.normal(0, 8, 30),
        "Patient E": 75 + np.random.normal(0, 5, 22)
    }
    
    # Add heart rate data to the second summary graph
    for patient, data in heart_rate_data.items():
        summary_graph2.add_data_point(patient, data)
    
    # Configure the second summary graph
    summary_graph2.set_color_scheme("red")
    summary_graph2.set_percentile_ranges([(25, 75), (5, 95)])
    
    # Set axis labels
    summary_graph2.set_x_label("Patient")
    summary_graph2.set_y_label("Heart Rate (bpm)")
    
    # Add the second graph to the view
    view.add_graph(summary_graph2)
    
    # Render the view
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    view.render(fig, axes)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
