"""
Graph Module

This module defines the Graph class, which represents a single graph
with multiple layers in the PyOSCAR visualization framework.
"""

from typing import Dict, List, Tuple, Optional, Union, Any
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from .layer import Layer, LayerPosition


class Graph:
    """
    Graph class for PyOSCAR visualization framework
    
    A Graph represents a single visualization area that can contain
    multiple layers. It handles layout, scaling, and coordinate transformations
    for its layers.
    
    Attributes:
        name (str): A unique name for this graph
        title (str): The title displayed for this graph
        units (str): The units for the y-axis
        visible (bool): Whether the graph is currently visible
        min_height (int): Minimum pixel height for this graph
        max_height (int): Maximum pixel height for this graph
        layers (List[Layer]): Layers contained in this graph
    """
    
    def __init__(self, name: str, title: str = "", units: str = "", min_height: int = 100):
        """
        Initialize a new Graph
        
        Args:
            name: A unique name for this graph
            title: The title to display for this graph
            units: The units for the y-axis
            min_height: Minimum pixel height for this graph
        """
        self.name = name
        self.title = title
        self.units = units
        self.visible = True
        self.min_height = min_height
        self.max_height = 1000
        self.height = min_height
        self.show_title = True
        
        # Data ranges
        self._min_x = None
        self._max_x = None
        self._min_y = None
        self._max_y = None
        
        # Layers
        self.layers = []
        self._layers_by_name = {}
        
        # For time-based data
        self.current_time = None
        
    def add_layer(self, layer: Layer, position: LayerPosition = LayerPosition.Center, 
                 order: int = 0, movable: bool = False) -> None:
        """
        Add a layer to this graph
        
        Args:
            layer: The Layer to add
            position: The position of the layer within the graph
            order: Z-order for rendering (higher numbers are on top)
            movable: Whether the layer can be moved by the user
        """
        layer.position = position
        layer.order = order
        layer.movable = movable
        
        self.layers.append(layer)
        self._layers_by_name[layer.name] = layer
        
        # Sort layers by order
        self.layers.sort(key=lambda l: l.order)
        
    def remove_layer(self, layer_name: str) -> bool:
        """
        Remove a layer from this graph
        
        Args:
            layer_name: The name of the layer to remove
            
        Returns:
            True if the layer was found and removed, False otherwise
        """
        if layer_name in self._layers_by_name:
            layer = self._layers_by_name[layer_name]
            self.layers.remove(layer)
            del self._layers_by_name[layer_name]
            return True
        return False
    
    def get_layer(self, layer_name: str) -> Optional[Layer]:
        """
        Get a layer by name
        
        Args:
            layer_name: The name of the layer to get
            
        Returns:
            The Layer with the given name, or None if not found
        """
        return self._layers_by_name.get(layer_name)
    
    def reset_bounds(self) -> None:
        """Reset the bounds of this graph based on the data in its layers"""
        self._min_x = None
        self._max_x = None
        self._min_y = None
        self._max_y = None
        
        for layer in self.layers:
            if not layer.visible:
                continue
                
            if self._min_x is None or layer.min_x() < self._min_x:
                self._min_x = layer.min_x()
            if self._max_x is None or layer.max_x() > self._max_x:
                self._max_x = layer.max_x()
            if self._min_y is None or layer.min_y() < self._min_y:
                self._min_y = layer.min_y()
            if self._max_y is None or layer.max_y() > self._max_y:
                self._max_y = layer.max_y()
                
        # Default values if no data
        if self._min_x is None:
            self._min_x = 0
        if self._max_x is None:
            self._max_x = 1
        if self._min_y is None:
            self._min_y = 0
        if self._max_y is None:
            self._max_y = 1
            
        # Add a small margin to the y-axis
        y_range = self._max_y - self._min_y
        if y_range == 0:
            y_range = 1
        self._min_y -= y_range * 0.05
        self._max_y += y_range * 0.05
        
    def set_x_bounds(self, min_x: float, max_x: float) -> None:
        """
        Set the x-axis bounds
        
        Args:
            min_x: Minimum x value
            max_x: Maximum x value
        """
        self._min_x = min_x
        self._max_x = max_x
        
    def set_y_bounds(self, min_y: float, max_y: float) -> None:
        """
        Set the y-axis bounds
        
        Args:
            min_y: Minimum y value
            max_y: Maximum y value
        """
        self._min_y = min_y
        self._max_y = max_y
        
    def min_x(self) -> float:
        """
        Get the minimum x value
        
        Returns:
            The minimum x value
        """
        if self._min_x is None:
            self.reset_bounds()
        return self._min_x
    
    def max_x(self) -> float:
        """
        Get the maximum x value
        
        Returns:
            The maximum x value
        """
        if self._max_x is None:
            self.reset_bounds()
        return self._max_x
    
    def min_y(self) -> float:
        """
        Get the minimum y value
        
        Returns:
            The minimum y value
        """
        if self._min_y is None:
            self.reset_bounds()
        return self._min_y
    
    def max_y(self) -> float:
        """
        Get the maximum y value
        
        Returns:
            The maximum y value
        """
        if self._max_y is None:
            self.reset_bounds()
        return self._max_y
    
    def is_empty(self) -> bool:
        """
        Check if this graph has any data
        
        Returns:
            True if the graph is empty (has no data), False otherwise
        """
        for layer in self.layers:
            if layer.visible and not isinstance(layer._data, dict) or len(layer._data) > 0:
                return False
        return True
    
    def deselect(self) -> None:
        """Deselect all layers in this graph"""
        for layer in self.layers:
            layer.deselect()
            layer.unhighlight()
    
    def is_selected(self) -> bool:
        """
        Check if any layer in this graph is selected
        
        Returns:
            True if any layer is selected, False otherwise
        """
        for layer in self.layers:
            if layer.selected or layer.highlighted:
                return True
        return False
    
    def render(self, fig: Figure, ax: plt.Axes) -> None:
        """
        Render this graph to the given matplotlib Figure and Axes
        
        Args:
            fig: The matplotlib Figure to render to
            ax: The matplotlib Axes to render to
        """
        if not self.visible:
            return
        
        # Set axis labels
        if self.show_title:
            ax.set_title(self.title)
        ax.set_ylabel(self.units)
        
        # Set axis limits
        ax.set_xlim(self.min_x(), self.max_x())
        ax.set_ylim(self.min_y(), self.max_y())
        
        # Render each layer
        for layer in self.layers:
            if layer.visible:
                layer.render(ax, (self.min_x(), self.max_x()), (self.min_y(), self.max_y()))
                
    def __str__(self) -> str:
        return f"Graph({self.name}, {len(self.layers)} layers)"
