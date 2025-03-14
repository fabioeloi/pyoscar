"""
Multi-Graph Dashboard Example

This example demonstrates how to create a dashboard with multiple
synchronized graphs, similar to OSCAR's multi-graph displays.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pyoscar.core import GraphView
from pyoscar.graphs import LineGraph, BarGraph, SummaryGraph

def main():
    # Create a graph view to hold our dashboard
    view = GraphView("Sleep Analysis Dashboard")
    
    # Generate sample time-series data (simulating a night of sleep data)
    # Create a 8-hour time range with readings every minute
    start_time = datetime(2025, 3, 10, 22, 0, 0)  # 10:00 PM
    end_time = datetime(2025, 3, 11, 6, 0, 0)     # 6:00 AM
    
    # Create time points (convert to matplotlib date format)
    timestamps = [start_time + timedelta(minutes=i) for i in range(0, 8*60)]
    x_time = mdates.date2num(timestamps)
    
    # Generate oxygen saturation data (95-100% with some dips)
    np.random.seed(42)  # For reproducible results
    oxygen = 97 + np.random.normal(0, 0.8, len(x_time))
    
    # Create some artificial dips in oxygen (simulating sleep apnea events)
    event_times = [60, 120, 210, 300, 390]  # Events at these minute marks
    for event in event_times:
        # Create a dip lasting about 2 minutes
        for i in range(event, event+2):
            if i < len(oxygen):
                oxygen[i] = 91 + np.random.normal(0, 1)
    
    # Create heart rate data (ranging from 55-80 BPM)
    heart_rate = 65 + 10 * np.sin(np.linspace(0, 8*np.pi, len(x_time))) + np.random.normal(0, 2, len(x_time))
    
    # Generate 'events' data (for bar chart)
    # We'll count apnea events in 1-hour windows
    hourly_bins = np.zeros(8)
    for event in event_times:
        hour = event // 60
        if hour < 8:
            hourly_bins[hour] += 1
    
    hour_labels = ["10 PM", "11 PM", "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM"]
    hour_x = np.arange(8)
    
    # Create the oxygen saturation line graph
    oxygen_graph = LineGraph("Oxygen", "Oxygen Saturation", "%")
    oxygen_graph.add_data(x_time, oxygen)
    oxygen_graph.set_line_style(color="blue", line_width=1.5)
    oxygen_graph.set_x_label("Time")
    oxygen_graph.set_y_label("SpO2 (%)")
    
    # Configure to show time properly
    oxygen_graph.x_axis_layer.is_time_axis = True
    oxygen_graph.x_axis_layer.time_format = "%H:%M"
    
    # Add to the view
    view.add_graph(oxygen_graph)
    
    # Create the heart rate line graph
    heart_graph = LineGraph("Heart Rate", "Heart Rate", "BPM")
    heart_graph.add_data(x_time, heart_rate)
    heart_graph.set_line_style(color="red", line_width=1.5)
    heart_graph.set_x_label("Time")
    heart_graph.set_y_label("Heart Rate (BPM)")
    
    # Configure to show time properly
    heart_graph.x_axis_layer.is_time_axis = True
    heart_graph.x_axis_layer.time_format = "%H:%M"
    
    # Add to the view
    view.add_graph(heart_graph)
    
    # Create a bar graph for events
    events_graph = BarGraph("Events", "Apnea Events Per Hour", "Count")
    events_graph.add_data(hour_x, hourly_bins)
    events_graph.set_categories(hour_labels)
    events_graph.set_bar_style(color="purple", alpha=0.7)
    events_graph.set_x_label("Hour")
    events_graph.set_y_label("Event Count")
    
    # Add to the view
    view.add_graph(events_graph)
    
    # Create a summary graph for oxygen statistics by hour
    oxygen_summary = SummaryGraph("Oxygen Summary", "Oxygen Statistics By Hour", "%")
    
    # Calculate hourly stats for oxygen readings
    for i, hour in enumerate(hour_labels):
        start_idx = i * 60
        end_idx = start_idx + 60
        if end_idx <= len(oxygen):
            hourly_oxygen = oxygen[start_idx:end_idx]
            oxygen_summary.add_data_point(hour, hourly_oxygen)
    
    oxygen_summary.set_color_scheme("blue")
    oxygen_summary.set_x_label("Hour")
    oxygen_summary.set_y_label("Oxygen (%)")
    
    # Add to the view
    view.add_graph(oxygen_summary)
    
    # Render the dashboard with synchronized x-axes for the time series
    fig = plt.figure(figsize=(12, 10))
    
    # Create a 2x2 grid of subplots
    gs = fig.add_gridspec(2, 2, height_ratios=[2, 1])
    
    # Create axes for each graph
    ax1 = fig.add_subplot(gs[0, 0])  # Oxygen (top left)
    ax2 = fig.add_subplot(gs[0, 1])  # Heart rate (top right)
    ax3 = fig.add_subplot(gs[1, 0])  # Events (bottom left)
    ax4 = fig.add_subplot(gs[1, 1])  # Oxygen summary (bottom right)
    
    axes = [ax1, ax2, ax3, ax4]
    
    # Render all graphs
    view.render(fig, axes)
    
    # Make sure time-series graphs have synchronized x-axes
    ax1.get_shared_x_axes().join(ax1, ax2)
    
    # Set title for the dashboard
    fig.suptitle("Sleep Analysis Dashboard", fontsize=16)
    
    # Show the dashboard
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Make room for suptitle
    plt.show()

if __name__ == "__main__":
    main()
