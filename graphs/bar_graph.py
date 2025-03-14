"""
Bar Graph Module

This module defines the BarGraph class, which provides a simplified
interface for creating bar chart visualizations.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np

from ..core.graph import Graph
from ..core.layer import LayerPosition
from .bar_layer import BarLayer
from .axis_layer import XAxisLayer, YAxisLayer


class BarGraph(Graph):
    """
    BarGraph for visualizing bar chart data
    
    This graph is a specialized Graph that uses BarLayer for rendering
    data as bars. It provides a simplified interface for creating bar charts.
    
    Attributes:
        main_layer (BarLayer): The main bar layer for this graph
        x_axis_layer (XAxisLayer): X-axis layer for this graph
        y_axis_layer (YAxisLayer): Y-axis layer for this graph
    """
    
    def __init__(self, name: str, title: str = "", units: str = "", min_height: int = 100):
        """
        Initialize a new BarGraph
        
        Args:
            name: A unique name for this graph
            title: The title to display for this graph
            units: The units for the y-axis
            min_height: Minimum pixel height for this graph
        """
        super().__init__(name, title, units, min_height)
        
        # Create and add the main bar layer
        self.main_layer = BarLayer(f"{name}_main_layer", LayerPosition.Center)
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
            x: Array of x values (categories)
            y: Array of y values (bar heights)
            series_name: Name for this data series (for multiple bar series)
        """
        self.main_layer.add_data(x, y, series_name)
        self.reset_bounds()
        
    def set_bar_style(self, series_name: str = 'default', **kwargs) -> None:
        """
        Set bar style properties
        
        Args:
            series_name: Name of the data series to style
            **kwargs: Style properties to set (color, edge_color, etc.)
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
        
    def set_horizontal(self, horizontal: bool = True) -> None:
        """
        Set whether to use horizontal bars
        
        Args:
            horizontal: If True, bars will be drawn horizontally
        """
        self.main_layer.horizontal = horizontal
        
    def set_bar_width(self, width: float) -> None:
        """
        Set the relative width of bars
        
        Args:
            width: Relative width (0.0-1.0) of bars
        """
        self.main_layer.bar_width = width
        
    def set_categories(self, categories: List[str]) -> None:
        """
        Set category labels for the x-axis
        
        Args:
            categories: List of category names
        """
        # Use integer indices for x data and override ticks with labels
        x = np.arange(len(categories))
        if self.main_layer.x_data is not None and len(self.main_layer.y_data) > 0:
            # If we already have y data, create new x data with correct length
            y = self.main_layer.y_data
            if len(categories) != len(y):
                x = np.arange(len(y))
                # Truncate or extend categories as needed
                if len(categories) > len(y):
                    categories = categories[:len(y)]
                else:
                    categories = categories + [""] * (len(y) - len(categories))
            self.main_layer.x_data = x
            
        # Set the tick positions and labels
        self.x_axis_layer.major_ticks = x
        ax = plt.gca()
        if ax:
            ax.set_xticklabels(categories)
        else:
            # Store for later use when axis is available
            self._categories = categories
