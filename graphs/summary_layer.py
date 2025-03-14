"""
Summary Layer Module

This module defines the SummaryLayer class, which implements summary
visualization in the PyOSCAR framework, similar to OSCAR's summary charts.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

from ..core.layer import Layer, LayerPosition


class SummaryLayer(Layer):
    """
    SummaryLayer for visualizing summary statistics
    
    This layer displays statistical summaries of data, such as min/max,
    percentiles, and average values in a compact visual form.
    
    Attributes:
        color_scheme (str): Color scheme for the summary ('default', 'blue', 'red', etc.)
        show_median (bool): Whether to show the median line
        show_mean (bool): Whether to show the mean line
        show_percentiles (bool): Whether to show percentile ranges
        show_minmax (bool): Whether to show min/max values
        percentile_ranges (List[Tuple[float, float]]): List of percentile ranges to display
    """
    
    def __init__(self, name: str, position: LayerPosition = LayerPosition.Center):
        """
        Initialize a new SummaryLayer
        
        Args:
            name: A unique name for this layer
            position: The position of this layer within its parent graph
        """
        super().__init__(name, position)
        
        # Summary style properties
        self.color_scheme = 'default'
        self.show_median = True
        self.show_mean = True
        self.show_percentiles = True
        self.show_minmax = True
        self.percentile_ranges = [(25, 75), (10, 90), (5, 95)]  # Default percentile ranges
        
        # Data management
        self.data_points = {}  # Each point has x position and statistics
        self.labels = []  # X-axis labels
        
        # Interactive elements
        self.highlight_point = None
        self.highlight_color = 'red'
        
    def add_data_point(self, x_label: str, values: np.ndarray) -> None:
        """
        Add a data point with statistics to this layer
        
        Args:
            x_label: Label for this data point on the x-axis
            values: Array of values for calculating statistics
        """
        if len(values) == 0:
            # Skip empty data points
            return
            
        # Calculate statistics
        stats = {
            'min': np.min(values),
            'max': np.max(values),
            'mean': np.mean(values),
            'median': np.median(values),
            'percentiles': {}
        }
        
        # Calculate percentiles
        for low, high in self.percentile_ranges:
            stats['percentiles'][(low, high)] = (
                np.percentile(values, low),
                np.percentile(values, high)
            )
            
        # Add to data points
        self.data_points[x_label] = stats
        
        # Update labels list
        if x_label not in self.labels:
            self.labels.append(x_label)
            
    def clear_data(self) -> None:
        """Clear all data from this layer"""
        self.data_points = {}
        self.labels = []
                    
    def min_x(self) -> float:
        """
        Get the minimum X value in this layer's data
        
        Returns:
            The minimum X value, or 0 if no data exists
        """
        if not self.labels:
            return 0.0
        return 0.0  # Summary always starts at 0
    
    def max_x(self) -> float:
        """
        Get the maximum X value in this layer's data
        
        Returns:
            The maximum X value, or 0 if no data exists
        """
        if not self.labels:
            return 0.0
        return len(self.labels)  # One unit per label
    
    def min_y(self) -> float:
        """
        Get the minimum Y value in this layer's data
        
        Returns:
            The minimum Y value, or 0 if no data exists
        """
        min_val = float('inf')
        
        for stats in self.data_points.values():
            if 'min' in stats:
                min_val = min(min_val, stats['min'])
                
        return 0.0 if min_val == float('inf') else min_val
    
    def max_y(self) -> float:
        """
        Get the maximum Y value in this layer's data
        
        Returns:
            The maximum Y value, or 0 if no data exists
        """
        max_val = float('-inf')
        
        for stats in self.data_points.values():
            if 'max' in stats:
                max_val = max(max_val, stats['max'])
                
        return 0.0 if max_val == float('-inf') else max_val
    
    def _get_colors(self):
        """
        Get colors for different elements based on the color scheme
        
        Returns:
            Dictionary of colors for different elements
        """
        if self.color_scheme == 'blue':
            return {
                'box': 'skyblue',
                'median': 'navy',
                'mean': 'darkblue',
                'whisker': 'steelblue',
                'outlier': 'blue',
                'highlight': 'red'
            }
        elif self.color_scheme == 'red':
            return {
                'box': 'salmon',
                'median': 'darkred',
                'mean': 'firebrick',
                'whisker': 'indianred',
                'outlier': 'red',
                'highlight': 'blue'
            }
        elif self.color_scheme == 'green':
            return {
                'box': 'lightgreen',
                'median': 'darkgreen',
                'mean': 'forestgreen',
                'whisker': 'seagreen',
                'outlier': 'green',
                'highlight': 'red'
            }
        else:  # default
            return {
                'box': 'lightblue',
                'median': 'black',
                'mean': 'darkblue',
                'whisker': 'gray',
                'outlier': 'red',
                'highlight': 'red'
            }
    
    def render(self, ax: plt.Axes, x_range: Tuple[float, float], y_range: Tuple[float, float]) -> None:
        """
        Render this layer to the given matplotlib Axes
        
        Args:
            ax: The matplotlib Axes to render to
            x_range: The (min, max) range of the x-axis
            y_range: The (min, max) range of the y-axis
        """
        if not self.visible or not self.data_points:
            return
            
        # Get colors for different elements
        colors = self._get_colors()
        
        # Calculate the width of each box
        box_width = 0.6
            
        # Draw each data point
        for i, label in enumerate(self.labels):
            if label not in self.data_points:
                continue
                
            x_pos = i + 0.5  # Center of the box
            stats = self.data_points[label]
            
            # Only draw points within the current view
            if x_pos < x_range[0] or x_pos > x_range[1]:
                continue
                
            # Draw min-max whiskers if requested
            if self.show_minmax:
                min_val = stats['min']
                max_val = stats['max']
                
                # Draw whisker lines
                ax.plot([x_pos, x_pos], [min_val, max_val], 
                     color=colors['whisker'], linestyle='-', linewidth=1)
                
                # Draw caps on whiskers
                cap_width = box_width * 0.3
                ax.plot([x_pos - cap_width/2, x_pos + cap_width/2], 
                     [min_val, min_val], color=colors['whisker'], linewidth=1)
                ax.plot([x_pos - cap_width/2, x_pos + cap_width/2], 
                     [max_val, max_val], color=colors['whisker'], linewidth=1)
            
            # Draw percentile boxes if requested
            if self.show_percentiles:
                # Draw from widest to narrowest
                sorted_ranges = sorted(self.percentile_ranges, 
                                    key=lambda x: x[1] - x[0], 
                                    reverse=True)
                
                for i, (low, high) in enumerate(sorted_ranges):
                    if (low, high) not in stats['percentiles']:
                        continue
                        
                    low_val, high_val = stats['percentiles'][(low, high)]
                    
                    # Scale width based on percentile range
                    width = box_width * (1.0 - i * 0.15)
                    
                    # Draw box
                    rect = Rectangle((x_pos - width/2, low_val), 
                                  width, high_val - low_val,
                                  facecolor=colors['box'],
                                  edgecolor=colors['whisker'],
                                  alpha=0.7 - i * 0.15,
                                  linewidth=1)
                    ax.add_patch(rect)
            
            # Draw median line if requested
            if self.show_median and 'median' in stats:
                median = stats['median']
                ax.plot([x_pos - box_width/2, x_pos + box_width/2], 
                     [median, median], 
                     color=colors['median'], linewidth=2)
                
            # Draw mean if requested
            if self.show_mean and 'mean' in stats:
                mean = stats['mean']
                ax.plot(x_pos, mean, 'o', 
                     color=colors['mean'], markersize=6)
                
            # Highlight if this is the highlighted point
            if self.highlight_point is not None and label == self.highlight_point:
                # Draw highlight box around this summary
                rect = Rectangle((x_pos - box_width/1.5, stats['min']), 
                              box_width * 1.3, stats['max'] - stats['min'],
                              facecolor='none',
                              edgecolor=colors['highlight'],
                              linewidth=2,
                              linestyle='--')
                ax.add_patch(rect)
                
        # Set up x-axis ticks and labels
        ax.set_xticks([i + 0.5 for i in range(len(self.labels))])
        ax.set_xticklabels(self.labels)
    
    def highlight(self, x: float, y: float) -> bool:
        """
        Highlight the summary at the given coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if highlighting was successful, False otherwise
        """
        if not self.labels:
            return False
            
        # Convert x to an index
        idx = int(x)
        if idx < 0 or idx >= len(self.labels):
            return False
            
        # Get the label at this index
        label = self.labels[idx]
        
        self.highlight_point = label
        self.highlighted = True
        return True
    
    def unhighlight(self) -> None:
        """Remove highlighting from this layer"""
        self.highlight_point = None
        self.highlighted = False
