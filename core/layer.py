"""
Layer Module

This module defines the Layer class, which is a fundamental building block
for graphs in PyOSCAR. Layers represent different visual components that
can be stacked in a graph.
"""

from enum import Enum
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import matplotlib.pyplot as plt


class LayerPosition(Enum):
    """Enum defining possible layer positions within a graph"""
    Top = 0
    Bottom = 1
    Left = 2
    Right = 3
    Center = 4


class Layer:
    """
    Base Layer class for PyOSCAR visualization framework
    
    A Layer is a fundamental component that can be added to a Graph.
    Each Layer represents a distinct visual element that can be drawn
    on the graph, such as lines, bars, or other visual components.
    
    Attributes:
        name (str): A unique name for this layer
        visible (bool): Whether the layer is currently visible
        position (LayerPosition): The position of the layer within its parent graph
        min_height (int): Minimum height for this layer
        min_width (int): Minimum width for this layer
        movable (bool): Whether the user can move this layer
        selectable (bool): Whether the user can select this layer
        order (int): Z-order for this layer
        show_controls (bool): Whether to show controls for this layer
        fixed_height (bool): Whether this layer has a fixed height
        offset_x (int): Horizontal offset for this layer
        offset_y (int): Vertical offset for this layer
    """
    
    def __init__(self, name: str, position: LayerPosition = LayerPosition.Center):
        """
        Initialize a new Layer
        
        Args:
            name: A unique name for this layer
            position: The position of this layer within its parent graph
        """
        self.name = name
        self.visible = True
        self.position = position
        self.min_height = 0
        self.min_width = 0
        self.movable = False
        self.selectable = True
        self.order = 0
        self.show_controls = False
        self.fixed_height = False
        self.offset_x = 0
        self.offset_y = 0
        
        # Data storage
        self._data = {}
        
        # Interaction state
        self.selected = False
        self.highlighted = False
        
    def add_data(self, key: str, data: Any) -> None:
        """
        Add data to this layer
        
        Args:
            key: A unique key for this data
            data: The data to add
        """
        self._data[key] = data
        
    def get_data(self, key: str) -> Any:
        """
        Get data from this layer
        
        Args:
            key: The key for the data to retrieve
            
        Returns:
            The data associated with the given key
        """
        return self._data.get(key)
    
    def min_x(self) -> float:
        """
        Get the minimum X value in this layer's data
        
        Returns:
            The minimum X value, or 0 if no data exists
        """
        return 0
    
    def max_x(self) -> float:
        """
        Get the maximum X value in this layer's data
        
        Returns:
            The maximum X value, or 0 if no data exists
        """
        return 0
    
    def min_y(self) -> float:
        """
        Get the minimum Y value in this layer's data
        
        Returns:
            The minimum Y value, or 0 if no data exists
        """
        return 0
    
    def max_y(self) -> float:
        """
        Get the maximum Y value in this layer's data
        
        Returns:
            The maximum Y value, or 0 if no data exists
        """
        return 0
    
    def render(self, ax: plt.Axes, x_range: Tuple[float, float], y_range: Tuple[float, float]) -> None:
        """
        Render this layer to the given matplotlib Axes
        
        Args:
            ax: The matplotlib Axes to render to
            x_range: The (min, max) range of the x-axis
            y_range: The (min, max) range of the y-axis
        """
        # Base implementation does nothing, to be overridden by subclasses
        pass
    
    def select(self, x: float, y: float) -> bool:
        """
        Select this layer at the given coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if selection was successful, False otherwise
        """
        self.selected = True
        return True
    
    def deselect(self) -> None:
        """Deselect this layer"""
        self.selected = False
        
    def highlight(self, x: float, y: float) -> bool:
        """
        Highlight this layer at the given coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if highlighting was successful, False otherwise
        """
        self.highlighted = True
        return True
    
    def unhighlight(self) -> None:
        """Remove highlighting from this layer"""
        self.highlighted = False
    
    def __str__(self) -> str:
        return f"Layer({self.name})"
