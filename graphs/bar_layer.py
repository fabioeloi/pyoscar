"""
Bar Layer Module

This module defines the BarLayer class, which implements bar chart
visualization in the PyOSCAR framework.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.colors as mcolors

from ..core.layer import Layer, LayerPosition


class BarLayer(Layer):
    """
    BarLayer for visualizing bar chart data
    
    This layer draws bars based on X and Y data points, with various
    styling options.
    
    Attributes:
        color (str): Color of the bars
        edge_color (str): Color of the bar edges
        edge_width (float): Width of the bar edges
        alpha (float): Transparency of the bars (0.0-1.0)
        bar_width (float): Width of the bars relative to x-spacing
        horizontal (bool): Whether to draw horizontal bars
    """
    
    def __init__(self, name: str, position: LayerPosition = LayerPosition.Center):
        """
        Initialize a new BarLayer
        
        Args:
            name: A unique name for this layer
            position: The position of this layer within its parent graph
        """
        super().__init__(name, position)
        
        # Bar style properties
        self.color = 'blue'
        self.edge_color = 'black'
        self.edge_width = 0.5
        self.alpha = 0.7
        self.bar_width = 0.8
        self.horizontal = False
        
        # Data management
        self.x_data = None
        self.y_data = None
        self.data_series = {}  # For multiple bar series
        
        # Interactive elements
        self.highlight_bar = None
        self.highlight_color = 'red'
        
    def add_data(self, x: np.ndarray, y: np.ndarray, series_name: str = 'default') -> None:
        """
        Add data to this layer
        
        Args:
            x: Array of x values (categories)
            y: Array of y values (bar heights)
            series_name: Name for this data series (for multiple bar series)
        """
        if series_name == 'default':
            self.x_data = np.array(x)
            self.y_data = np.array(y)
        else:
            self.data_series[series_name] = {
                'x': np.array(x),
                'y': np.array(y),
                'color': mcolors.to_rgba(self.color),
                'edge_color': self.edge_color,
                'edge_width': self.edge_width,
                'alpha': self.alpha
            }
            
    def set_style(self, series_name: str = 'default', **kwargs) -> None:
        """
        Set style properties for a data series
        
        Args:
            series_name: Name of the data series to style
            **kwargs: Style properties to set (color, edge_color, etc.)
        """
        if series_name == 'default':
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        elif series_name in self.data_series:
            for key, value in kwargs.items():
                if key in self.data_series[series_name]:
                    self.data_series[series_name][key] = value
                    
    def min_x(self) -> float:
        """
        Get the minimum X value in this layer's data
        
        Returns:
            The minimum X value, or 0 if no data exists
        """
        min_val = float('inf')
        
        if self.x_data is not None and len(self.x_data) > 0:
            min_val = min(min_val, np.min(self.x_data))
            
        for series in self.data_series.values():
            if 'x' in series and len(series['x']) > 0:
                min_val = min(min_val, np.min(series['x']))
                
        return 0.0 if min_val == float('inf') else min_val
    
    def max_x(self) -> float:
        """
        Get the maximum X value in this layer's data
        
        Returns:
            The maximum X value, or 0 if no data exists
        """
        max_val = float('-inf')
        
        if self.x_data is not None and len(self.x_data) > 0:
            max_val = max(max_val, np.max(self.x_data))
            
        for series in self.data_series.values():
            if 'x' in series and len(series['x']) > 0:
                max_val = max(max_val, np.max(series['x']))
                
        # Add a little padding for bar width
        if max_val != float('-inf'):
            if self.x_data is not None and len(self.x_data) > 1:
                dx = self.x_data[1] - self.x_data[0]
                max_val += dx * 0.5
                
        return 0.0 if max_val == float('-inf') else max_val
    
    def min_y(self) -> float:
        """
        Get the minimum Y value in this layer's data
        
        Returns:
            The minimum Y value, or 0 if no data exists
        """
        min_val = float('inf')
        
        if self.y_data is not None and len(self.y_data) > 0:
            min_val = min(min_val, np.min(self.y_data))
            
        for series in self.data_series.values():
            if 'y' in series and len(series['y']) > 0:
                min_val = min(min_val, np.min(series['y']))
                
        # For bar charts, often we want to start at 0
        if min_val > 0:
            return 0.0
                
        return 0.0 if min_val == float('inf') else min_val
    
    def max_y(self) -> float:
        """
        Get the maximum Y value in this layer's data
        
        Returns:
            The maximum Y value, or 0 if no data exists
        """
        max_val = float('-inf')
        
        if self.y_data is not None and len(self.y_data) > 0:
            max_val = max(max_val, np.max(self.y_data))
            
        for series in self.data_series.values():
            if 'y' in series and len(series['y']) > 0:
                max_val = max(max_val, np.max(series['y']))
                
        # Add a little padding at the top
        if max_val != float('-inf'):
            max_val *= 1.05
                
        return 0.0 if max_val == float('-inf') else max_val
    
    def render(self, ax: plt.Axes, x_range: Tuple[float, float], y_range: Tuple[float, float]) -> None:
        """
        Render this layer to the given matplotlib Axes
        
        Args:
            ax: The matplotlib Axes to render to
            x_range: The (min, max) range of the x-axis
            y_range: The (min, max) range of the y-axis
        """
        if not self.visible:
            return
            
        # Draw the default series
        if self.x_data is not None and self.y_data is not None and len(self.x_data) > 0 and len(self.y_data) > 0:
            # Ensure we're only drawing bars within the current view
            mask = (self.x_data >= x_range[0]) & (self.x_data <= x_range[1])
            if not np.any(mask):
                return
                
            x = self.x_data[mask]
            y = self.y_data[mask]
            
            # Calculate bar width if x values are numeric
            width = self.bar_width
            if len(x) > 1:
                dx = x[1] - x[0]
                width = dx * self.bar_width
            
            # Draw bars
            if self.horizontal:
                bars = ax.barh(x, y, height=width, 
                          color=self.color, 
                          edgecolor=self.edge_color,
                          linewidth=self.edge_width,
                          alpha=self.alpha)
            else:
                bars = ax.bar(x, y, width=width, 
                          color=self.color, 
                          edgecolor=self.edge_color,
                          linewidth=self.edge_width,
                          alpha=self.alpha)
                
            # Highlight bar if requested
            if self.highlight_bar is not None:
                idx = self.highlight_bar
                if 0 <= idx < len(bars):
                    bars[idx].set_color(self.highlight_color)
                         
        # Draw additional data series
        for name, series in self.data_series.items():
            if 'x' not in series or 'y' not in series:
                continue
                
            x = series['x']
            y = series['y']
            
            if len(x) == 0 or len(y) == 0:
                continue
                
            # Ensure we're only drawing bars within the current view
            mask = (x >= x_range[0]) & (x <= x_range[1])
            if not np.any(mask):
                continue
                
            x = x[mask]
            y = y[mask]
            
            # Calculate bar width if x values are numeric
            width = self.bar_width
            if len(x) > 1:
                dx = x[1] - x[0]
                width = dx * self.bar_width
            
            # Draw bars
            if self.horizontal:
                ax.barh(x, y, height=width, 
                     color=series['color'], 
                     edgecolor=series['edge_color'],
                     linewidth=series['edge_width'],
                     alpha=series['alpha'])
            else:
                ax.bar(x, y, width=width, 
                    color=series['color'], 
                    edgecolor=series['edge_color'],
                    linewidth=series['edge_width'],
                    alpha=series['alpha'])
    
    def highlight(self, x: float, y: float) -> bool:
        """
        Highlight the bar at the given coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if highlighting was successful, False otherwise
        """
        if self.x_data is None or self.y_data is None:
            return False
            
        if len(self.x_data) == 0:
            return False
            
        # Find the closest bar
        distances = np.abs(self.x_data - x)
        idx = np.argmin(distances)
        
        # Only highlight if within a reasonable distance
        width = self.bar_width
        if len(self.x_data) > 1:
            dx = self.x_data[1] - self.x_data[0]
            width = dx * self.bar_width
            
        if distances[idx] > width / 2:
            return False
            
        self.highlight_bar = idx
        self.highlighted = True
        return True
    
    def unhighlight(self) -> None:
        """Remove highlighting from this layer"""
        self.highlight_bar = None
        self.highlighted = False
