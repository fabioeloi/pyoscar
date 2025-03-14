"""
Time Series Example

This example demonstrates how to work with time series data in PyOSCAR,
similar to how OSCAR handles CPAP time series data.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path so we can import PyOSCAR modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import from the local modules
from core import GraphView
from graphs import LineGraph, SummaryGraph

def main():
    # Create a graph view for time series visualization
    view = GraphView("Time Series Demo")
    
    # Generate a time series dataset
    # Create a 24-hour period with readings every 5 minutes
    start_time = datetime(2025, 3, 1, 0, 0, 0)
    end_time = datetime(2025, 3, 1, 23, 59, 59)
    
    # Create timestamp array
    time_delta = timedelta(minutes=5)
    timestamps = []
    current = start_time
    
    while current <= end_time:
        timestamps.append(current)
        current += time_delta
    
    # Convert to matplotlib date format
    x_time = mdates.date2num(timestamps)
    
    # Generate synthetic data mimicking different physiological signals
    
    # 1. Generate a respiratory rate signal (breaths per minute)
    # Normal breathing is around 12-20 breaths per minute
    # We'll simulate changes throughout the day
    np.random.seed(42)  # For reproducible results
    
    # Base respiratory rate following a daily pattern
    hours = np.array([(t - start_time).total_seconds() / 3600 for t in timestamps])
    resp_base = 15 + 3 * np.sin(2 * np.pi * hours / 24)  # Daily cycle
    
    # Add random variations
    resp_rate = resp_base + np.random.normal(0, 1, len(timestamps))
    
    # 2. Generate an oxygen saturation signal (percentage)
    # Normal SpO2 is 95-100%
    oxygen_base = 97 + np.random.normal(0, 0.5, len(timestamps))
    
    # Add some dips during certain periods (simulating events)
    for i in range(len(timestamps)):
        # Add more significant dips during "sleep" hours (11 PM - 6 AM)
        hour = timestamps[i].hour
        if 23 <= hour or hour < 6:
            # Randomly add some desaturation events
            if np.random.random() < 0.05:  # 5% chance of an event
                # Create a desaturation event lasting a few readings
                event_length = np.random.randint(2, 5)
                dip_amount = np.random.uniform(3, 8)  # How much O2 drops
                
                for j in range(i, min(i + event_length, len(timestamps))):
                    oxygen_base[j] = max(oxygen_base[j] - dip_amount, 85)
    
    # 3. Generate a pulse rate signal (beats per minute)
    # Heart rate varies throughout the day
    pulse_base = 70 + 15 * np.sin(2 * np.pi * hours / 24 + np.pi)  # Inverse of resp pattern
    pulse_rate = pulse_base + np.random.normal(0, 3, len(timestamps))
    
    # Create a line graph for respiratory rate
    resp_graph = LineGraph("Respiratory Rate", "Respiratory Rate Over 24 Hours", "breaths/min")
    resp_graph.add_data(x_time, resp_rate)
    resp_graph.set_line_style(color="green", line_width=1.5)
    
    # Set up axes
    resp_graph.set_x_label("Time")
    resp_graph.set_y_label("Breaths per Minute")
    resp_graph.x_axis_layer.is_time_axis = True
    resp_graph.x_axis_layer.time_format = "%H:%M"
    
    # Add to view
    view.add_graph(resp_graph)
    
    # Create a line graph for oxygen saturation
    oxygen_graph = LineGraph("Oxygen Saturation", "SpO2 Over 24 Hours", "%")
    oxygen_graph.add_data(x_time, oxygen_base)
    oxygen_graph.set_line_style(color="blue", line_width=1.5)
    
    # Set up axes
    oxygen_graph.set_x_label("Time")
    oxygen_graph.set_y_label("SpO2 (%)")
    oxygen_graph.x_axis_layer.is_time_axis = True
    oxygen_graph.x_axis_layer.time_format = "%H:%M"
    
    # Add to view
    view.add_graph(oxygen_graph)
    
    # Create a line graph for pulse rate
    pulse_graph = LineGraph("Pulse Rate", "Pulse Rate Over 24 Hours", "bpm")
    pulse_graph.add_data(x_time, pulse_rate)
    pulse_graph.set_line_style(color="red", line_width=1.5)
    
    # Set up axes
    pulse_graph.set_x_label("Time")
    pulse_graph.set_y_label("Pulse (BPM)")
    pulse_graph.x_axis_layer.is_time_axis = True
    pulse_graph.x_axis_layer.time_format = "%H:%M"
    
    # Add to view
    view.add_graph(pulse_graph)
    
    # Create hourly summary for oxygen saturation
    oxygen_summary = SummaryGraph("Hourly SpO2", "Hourly Oxygen Saturation Statistics", "%")
    
    # Group data by hour and add to summary
    hourly_data = {}
    for i, timestamp in enumerate(timestamps):
        hour = timestamp.hour
        if hour not in hourly_data:
            hourly_data[hour] = []
        hourly_data[hour].append(oxygen_base[i])
    
    # Add hourly data to summary graph
    for hour in sorted(hourly_data.keys()):
        # Format hour as AM/PM
        hour_label = f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}"
        oxygen_summary.add_data_point(hour_label, np.array(hourly_data[hour]))
    
    # Configure summary graph
    oxygen_summary.set_color_scheme("blue")
    oxygen_summary.set_x_label("Hour")
    oxygen_summary.set_y_label("SpO2 (%)")
    
    # Add to view
    view.add_graph(oxygen_summary)
    
    # Render the graphs
    fig = plt.figure(figsize=(12, 10))
    
    # Create a grid with specific height ratios
    gs = fig.add_gridspec(4, 1, height_ratios=[2, 2, 2, 3])
    
    # Create axes for each graph
    ax1 = fig.add_subplot(gs[0])  # Respiratory rate
    ax2 = fig.add_subplot(gs[1])  # Oxygen
    ax3 = fig.add_subplot(gs[2])  # Pulse
    ax4 = fig.add_subplot(gs[3])  # Oxygen summary
    
    axes = [ax1, ax2, ax3, ax4]
    
    # Synchronize the x-axes of the time series graphs
    ax1.get_shared_x_axes().join(ax1, ax2, ax3)
    
    # Render graphs
    view.render(fig, axes)
    
    # Add title
    fig.suptitle("24-Hour Physiological Data Visualization", fontsize=16)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

if __name__ == "__main__":
    main()
    print("Time series visualization complete!")
