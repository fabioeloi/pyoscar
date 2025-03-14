"""
Axis Layer Module

This module defines the XAxisLayer and YAxisLayer classes, which implement
axis visualizations in the PyOSCAR framework.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.ticker as ticker

from ..core.layer import Layer, LayerPosition


class XAxisLayer(Layer):
    """
    XAxisLayer for visualizing the X axis
    
    This layer handles the rendering and configuration of the X axis.
    
    Attributes:
        label (str): Label for the axis
        tick_format (str): Format string for tick labels
        grid (bool): Whether to show grid lines
        major_ticks (List[float]): Positions for major ticks
        minor_ticks (List[float]): Positions for minor ticks
        is_time_axis (bool): Whether this is a time axis
        is_date_axis (bool): Whether this is a date axis
        time_format (str): Format string for time/date display
    """
    
    def __init__(self, name: str, position: LayerPosition = LayerPosition.Bottom):
        """
        Initialize a new XAxisLayer
        
        Args:
            name: A unique name for this layer
            position: The position of this layer within its parent graph
        """
        super().__init__(name, position)
        
        # Axis properties
        self.label = ""
        self.tick_format = None
        self.grid = True
        self.major_ticks = None
        self.minor_ticks = None
        
        # Time/date axis properties
        self.is_time_axis = False
        self.is_date_axis = False
        self.time_format = '%H:%M:%S'
        
        # Fixed height for axis
        self.min_height = 30
        self.fixed_height = True
        
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
        
        # Set up x-axis label
        if self.label:
            ax.set_xlabel(self.label)
        
        # Set up grid
        ax.grid(self.grid, axis='x', linestyle='--', alpha=0.7)
        
        # Set up tick format
        if self.tick_format:
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(self.tick_format))
            
        # Set up custom ticks if specified
        if self.major_ticks is not None:
            ax.set_xticks(self.major_ticks)
            
        if self.minor_ticks is not None:
            ax.set_xticks(self.minor_ticks, minor=True)
            
        # Handle time axis
        if self.is_time_axis:
            formatter = mdates.DateFormatter(self.time_format)
            ax.xaxis.set_major_formatter(formatter)
            
            # Auto-rotate tick labels for better readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
        # Handle date axis
        if self.is_date_axis:
            formatter = mdates.DateFormatter(self.time_format)
            ax.xaxis.set_major_formatter(formatter)
            
            # Determine appropriate date locator based on range
            range_days = (x_range[1] - x_range[0]) / (24 * 60 * 60 * 1000)
            
            if range_days <= 1:
                ax.xaxis.set_major_locator(mdates.HourLocator())
            elif range_days <= 7:
                ax.xaxis.set_major_locator(mdates.DayLocator())
            elif range_days <= 60:
                ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            else:
                ax.xaxis.set_major_locator(mdates.MonthLocator())
                
            # Auto-rotate tick labels for better readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


class YAxisLayer(Layer):
    """
    YAxisLayer for visualizing the Y axis
    
    This layer handles the rendering and configuration of the Y axis.
    
    Attributes:
        label (str): Label for the axis
        tick_format (str): Format string for tick labels
        grid (bool): Whether to show grid lines
        major_ticks (List[float]): Positions for major ticks
        minor_ticks (List[float]): Positions for minor ticks
    """
    
    def __init__(self, name: str, position: LayerPosition = LayerPosition.Left):
        """
        Initialize a new YAxisLayer
        
        Args:
            name: A unique name for this layer
            position: The position of this layer within its parent graph
        """
        super().__init__(name, position)
        
        # Axis properties
        self.label = ""
        self.tick_format = None
        self.grid = True
        self.major_ticks = None
        self.minor_ticks = None
        
        # Fixed width for axis
        self.min_width = 50
        self.fixed_height = False
        
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
        
        # Set up y-axis label
        if self.label:
            ax.set_ylabel(self.label)
        
        # Set up grid
        ax.grid(self.grid, axis='y', linestyle='--', alpha=0.7)
        
        # Set up tick format
        if self.tick_format:
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(self.tick_format))
            
        # Set up custom ticks if specified
        if self.major_ticks is not None:
            ax.set_yticks(self.major_ticks)
            
        if self.minor_ticks is not None:
            ax.set_yticks(self.minor_ticks, minor=True)
