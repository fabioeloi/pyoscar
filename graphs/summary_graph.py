"""
Summary Graph Module

This module defines the SummaryGraph class, which provides a simplified
interface for creating summary statistic visualizations.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np

from ..core.graph import Graph
from ..core.layer import LayerPosition
from .summary_layer import SummaryLayer
from .axis_layer import XAxisLayer, YAxisLayer


class SummaryGraph(Graph):
    """
    SummaryGraph for visualizing statistical summaries
    
    This graph is a specialized Graph that uses SummaryLayer for rendering
    statistical summaries. It provides a simplified interface for creating
    summary charts similar to those in OSCAR.
    
    Attributes:
        main_layer (SummaryLayer): The main summary layer for this graph
        x_axis_layer (XAxisLayer): X-axis layer for this graph
        y_axis_layer (YAxisLayer): Y-axis layer for this graph
    """
    
    def __init__(self, name: str, title: str = "", units: str = "", min_height: int = 150):
        """
        Initialize a new SummaryGraph
        
        Args:
            name: A unique name for this graph
            title: The title to display for this graph
            units: The units for the y-axis
            min_height: Minimum pixel height for this graph
        """
        super().__init__(name, title, units, min_height)
        
        # Create and add the main summary layer
        self.main_layer = SummaryLayer(f"{name}_main_layer", LayerPosition.Center)
        self.add_layer(self.main_layer, LayerPosition.Center, order=10)
        
        # Create and add axis layers
        self.x_axis_layer = XAxisLayer(f"{name}_x_axis", LayerPosition.Bottom)
        self.y_axis_layer = YAxisLayer(f"{name}_y_axis", LayerPosition.Left)
        
        self.add_layer(self.x_axis_layer, LayerPosition.Bottom, order=1)
        self.add_layer(self.y_axis_layer, LayerPosition.Left, order=1)
        
    def add_data_point(self, label: str, values: np.ndarray) -> None:
        """
        Add a data point with values for summary statistics
        
        Args:
            label: Label for this data point on the x-axis
            values: Array of values for calculating statistics
        """
        self.main_layer.add_data_point(label, values)
        self.reset_bounds()
        
    def add_data_series(self, labels: List[str], data_series: List[np.ndarray]) -> None:
        """
        Add multiple data points at once
        
        Args:
            labels: List of labels for data points
            data_series: List of arrays containing values for each data point
        """
        if len(labels) != len(data_series):
            raise ValueError("Labels and data series must have the same length")
            
        for label, values in zip(labels, data_series):
            self.add_data_point(label, values)
            
    def set_color_scheme(self, scheme: str) -> None:
        """
        Set the color scheme for the summary visualization
        
        Args:
            scheme: Color scheme name ('default', 'blue', 'red', 'green')
        """
        self.main_layer.color_scheme = scheme
        
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
        
    def set_percentile_ranges(self, ranges: List[Tuple[float, float]]) -> None:
        """
        Set the percentile ranges to display
        
        Args:
            ranges: List of (low, high) percentile pairs
        """
        self.main_layer.percentile_ranges = ranges
        
    def show_median(self, show: bool = True) -> None:
        """
        Set whether to show the median line
        
        Args:
            show: If True, show the median line
        """
        self.main_layer.show_median = show
        
    def show_mean(self, show: bool = True) -> None:
        """
        Set whether to show the mean point
        
        Args:
            show: If True, show the mean point
        """
        self.main_layer.show_mean = show
        
    def show_percentiles(self, show: bool = True) -> None:
        """
        Set whether to show percentile ranges
        
        Args:
            show: If True, show percentile ranges
        """
        self.main_layer.show_percentiles = show
        
    def show_minmax(self, show: bool = True) -> None:
        """
        Set whether to show min/max whiskers
        
        Args:
            show: If True, show min/max whiskers
        """
        self.main_layer.show_minmax = show
        
    def clear_data(self) -> None:
        """Clear all data points from this graph"""
        self.main_layer.clear_data()
        self.reset_bounds()
