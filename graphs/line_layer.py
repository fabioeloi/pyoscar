"""
Line Layer Module

This module defines the LineLayer class, which implements line-based 
visualization in the PyOSCAR framework.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors

from ..core.layer import Layer, LayerPosition


class LineLayer(Layer):
    """
    LineLayer for visualizing line-based data
    
    This layer draws lines based on X and Y data points, with various
    styling options.
    
    Attributes:
        color (str): Color of the line
        line_width (float): Width of the line in points
        line_style (str): Style of the line ('-', '--', '-.', ':', etc.)
        marker (str): Marker style for data points ('', 'o', '.', etc.)
        marker_size (float): Size of markers
        alpha (float): Transparency of the line (0.0-1.0)
        fill (bool): Whether to fill under the line
        fill_color (str): Color for fill
        fill_alpha (float): Transparency for fill
        antialias (bool): Whether to use antialiasing
    """
    
    def __init__(self, name: str, position: LayerPosition = LayerPosition.Center):
        """
        Initialize a new LineLayer
        
        Args:
            name: A unique name for this layer
            position: The position of this layer within its parent graph
        """
        super().__init__(name, position)
        
        # Line style properties
        self.color = 'blue'
        self.line_width = 1.5
        self.line_style = '-'
        self.marker = ''
        self.marker_size = 4.0
        self.alpha = 1.0
        self.fill = False
        self.fill_color = None
        self.fill_alpha = 0.2
        self.antialias = True
        
        # Data management
        self.x_data = None
        self.y_data = None
        self.data_series = {}  # For multiple lines
        
        # Interactive elements
        self.highlight_point = None
        self.highlight_color = 'red'
        self.highlight_size = 8.0
        
    def add_data(self, x: np.ndarray, y: np.ndarray, series_name: str = 'default') -> None:
        """
        Add data to this layer
        
        Args:
            x: Array of x values
            y: Array of y values
            series_name: Name for this data series (for multiple lines)
        """
        if series_name == 'default':
            self.x_data = np.array(x)
            self.y_data = np.array(y)
        else:
            self.data_series[series_name] = {
                'x': np.array(x),
                'y': np.array(y),
                'color': mcolors.to_rgba(self.color),
                'line_width': self.line_width,
                'line_style': self.line_style,
                'marker': self.marker,
                'marker_size': self.marker_size,
                'alpha': self.alpha,
                'fill': self.fill,
                'fill_color': self.fill_color if self.fill_color else self.color,
                'fill_alpha': self.fill_alpha
            }
            
    def set_style(self, series_name: str = 'default', **kwargs) -> None:
        """
        Set style properties for a data series
        
        Args:
            series_name: Name of the data series to style
            **kwargs: Style properties to set (color, line_width, etc.)
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
            # Ensure we're only drawing points within the current view
            mask = (self.x_data >= x_range[0]) & (self.x_data <= x_range[1])
            if not np.any(mask):
                return
                
            x = self.x_data[mask]
            y = self.y_data[mask]
            
            # Draw line
            line = ax.plot(x, y, 
                       color=self.color, 
                       linewidth=self.line_width,
                       linestyle=self.line_style,
                       marker=self.marker,
                       markersize=self.marker_size,
                       alpha=self.alpha,
                       antialiased=self.antialias)[0]
                       
            # Fill under line if requested
            if self.fill:
                fill_color = self.fill_color if self.fill_color else self.color
                ax.fill_between(x, y, y_range[0], color=fill_color, alpha=self.fill_alpha)
                
            # Draw highlighted point if any
            if self.highlight_point is not None:
                idx = self.highlight_point
                if 0 <= idx < len(self.x_data):
                    ax.plot(self.x_data[idx], self.y_data[idx], 
                         'o', color=self.highlight_color, 
                         markersize=self.highlight_size)
                         
        # Draw additional data series
        for name, series in self.data_series.items():
            if 'x' not in series or 'y' not in series:
                continue
                
            x = series['x']
            y = series['y']
            
            if len(x) == 0 or len(y) == 0:
                continue
                
            # Ensure we're only drawing points within the current view
            mask = (x >= x_range[0]) & (x <= x_range[1])
            if not np.any(mask):
                continue
                
            x = x[mask]
            y = y[mask]
            
            # Draw line
            line = ax.plot(x, y, 
                       color=series['color'], 
                       linewidth=series['line_width'],
                       linestyle=series['line_style'],
                       marker=series['marker'],
                       markersize=series['marker_size'],
                       alpha=series['alpha'],
                       antialiased=self.antialias)[0]
                       
            # Fill under line if requested
            if series['fill']:
                ax.fill_between(x, y, y_range[0], 
                             color=series['fill_color'], 
                             alpha=series['fill_alpha'])
    
    def highlight(self, x: float, y: float) -> bool:
        """
        Highlight the nearest point to the given coordinates
        
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
            
        # Find the closest point
        distances = np.sqrt((self.x_data - x)**2 + (self.y_data - y)**2)
        idx = np.argmin(distances)
        
        # Only highlight if within a reasonable distance
        if distances[idx] > (self.max_x() - self.min_x()) * 0.05:
            return False
            
        self.highlight_point = idx
        self.highlighted = True
        return True
    
    def unhighlight(self) -> None:
        """Remove highlighting from this layer"""
        self.highlight_point = None
        self.highlighted = False
