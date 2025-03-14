"""
Line Graph Module

This module defines the LineGraph class, which provides a simplified
interface for creating line-based visualizations.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np

from ..core.graph import Graph
from ..core.layer import LayerPosition
from .line_layer import LineLayer
from .axis_layer import XAxisLayer, YAxisLayer


class LineGraph(Graph):
    """
    LineGraph for visualizing line-based data
    
    This graph is a specialized Graph that uses LineLayer for rendering
    data as lines. It provides a simplified interface for creating line charts.
    
    Attributes:
        main_layer (LineLayer): The main line layer for this graph
        x_axis_layer (XAxisLayer): X-axis layer for this graph
        y_axis_layer (YAxisLayer): Y-axis layer for this graph
    """
    
    def __init__(self, name: str, title: str = "", units: str = "", min_height: int = 100):
        """
        Initialize a new LineGraph
        
        Args:
            name: A unique name for this graph
            title: The title to display for this graph
            units: The units for the y-axis
            min_height: Minimum pixel height for this graph
        """
        super().__init__(name, title, units, min_height)
        
        # Create and add the main line layer
        self.main_layer = LineLayer(f"{name}_main_layer", LayerPosition.Center)
        self.add_layer(self.main_layer, LayerPosition.Center, order=10)
        
        # Create and add axis layers
        self.x_axis_layer = XAxisLayer(f"{name}_x_axis", LayerPosition.Bottom)
        self.y_axis_layer = YAxisLayer(f"{name}_y_axis", LayerPosition.Left)
        
        self.add_layer(self.x_axis_layer, LayerPosition.Bottom, order=1)
        self.add_layer(self.y_axis_layer, LayerPosition.Left, order=1)
        
    def add_data(self, x: np.ndarray, y: np.ndarray, series_name: str = 'default') -> None:
        """
        Add data to this graph
        
        Args:
            x: Array of x values
            y: Array of y values
            series_name: Name for this data series (for multiple lines)
        """
        self.main_layer.add_data(x, y, series_name)
        self.reset_bounds()
        
    def set_line_style(self, series_name: str = 'default', **kwargs) -> None:
        """
        Set line style properties
        
        Args:
            series_name: Name of the data series to style
            **kwargs: Style properties to set (color, line_width, etc.)
        """
        self.main_layer.set_style(series_name, **kwargs)
        
    def set_x_label(self, label: str) -> None:
        """
        Set the x-axis label
        
        Args:
            label: The label for the x-axis
        """
        self.x_axis_layer.label = label
        
    def set_y_label(self, label: str) -> None:
        """
        Set the y-axis label
        
        Args:
            label: The label for the y-axis
        """
        self.y_axis_layer.label = label
        
    def set_x_tick_format(self, format_str: str) -> None:
        """
        Set the format string for x-axis tick labels
        
        Args:
            format_str: Format string for tick labels (e.g., '%.2f')
        """
        self.x_axis_layer.tick_format = format_str
        
    def set_y_tick_format(self, format_str: str) -> None:
        """
        Set the format string for y-axis tick labels
        
        Args:
            format_str: Format string for tick labels (e.g., '%.2f')
        """
        self.y_axis_layer.tick_format = format_str
        
    def set_time_x_axis(self, format_str: str = '%H:%M:%S') -> None:
        """
        Configure the x-axis for time display
        
        Args:
            format_str: Format string for time display (e.g., '%H:%M:%S')
        """
        self.x_axis_layer.time_format = format_str
        self.x_axis_layer.is_time_axis = True
        
    def set_date_x_axis(self, format_str: str = '%Y-%m-%d') -> None:
        """
        Configure the x-axis for date display
        
        Args:
            format_str: Format string for date display (e.g., '%Y-%m-%d')
        """
        self.x_axis_layer.time_format = format_str
        self.x_axis_layer.is_date_axis = True
