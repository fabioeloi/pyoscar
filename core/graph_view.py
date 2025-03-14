"""
GraphView Module

This module defines the GraphView class, which is the main container for
multiple graphs in the PyOSCAR visualization framework.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider, Button
import matplotlib.dates as mdates
from datetime import datetime
from .graph import Graph


class GraphView:
    """
    GraphView class for PyOSCAR visualization framework
    
    A GraphView is the main container for multiple graphs. It handles
    layout, interaction, zooming, and synchronization between graphs.
    
    Attributes:
        graphs (List[Graph]): List of graphs in this view
        linked_groups (Dict[int, List[Graph]]): Groups of graphs with linked x-axes
    """
    
    def __init__(self, title: str = "PyOSCAR Graph View"):
        """
        Initialize a new GraphView
        
        Args:
            title: The title for the figure window
        """
        self.title = title
        self.graphs = []
        self._graphs_by_name = {}
        self.linked_groups = {}
        
        # Figure and axes
        self.fig = None
        self.axes = []
        self.toolbar = None
        
        # Interaction state
        self.selecting = False
        self.selection_start = None
        self.selection_end = None
        self.current_time = None
        
        # History for navigation
        self.history = []
        self.history_position = -1
        
        # Default empty message
        self.empty_text = "No data to display"
        
    def add_graph(self, graph: Graph, group: int = 0) -> None:
        """
        Add a graph to this view
        
        Args:
            graph: The Graph to add
            group: The link group for synchronizing x-axes (0 means no sync)
        """
        self.graphs.append(graph)
        self._graphs_by_name[graph.name] = graph
        
        # Add to link group if specified
        if group > 0:
            if group not in self.linked_groups:
                self.linked_groups[group] = []
            self.linked_groups[group].append(graph)
            
    def remove_graph(self, graph_name: str) -> bool:
        """
        Remove a graph from this view
        
        Args:
            graph_name: The name of the graph to remove
            
        Returns:
            True if the graph was found and removed, False otherwise
        """
        if graph_name in self._graphs_by_name:
            graph = self._graphs_by_name[graph_name]
            self.graphs.remove(graph)
            del self._graphs_by_name[graph_name]
            
            # Remove from link groups
            for group in self.linked_groups.values():
                if graph in group:
                    group.remove(graph)
                    
            return True
        return False
    
    def get_graph(self, graph_name: str) -> Optional[Graph]:
        """
        Get a graph by name
        
        Args:
            graph_name: The name of the graph to get
            
        Returns:
            The Graph with the given name, or None if not found
        """
        return self._graphs_by_name.get(graph_name)
    
    def set_x_bounds(self, min_x: float, max_x: float, group: int = 0) -> None:
        """
        Set the x-axis bounds for all graphs or a specific link group
        
        Args:
            min_x: Minimum x value
            max_x: Maximum x value
            group: The link group to set bounds for (0 means all graphs)
        """
        if group > 0 and group in self.linked_groups:
            # Set bounds for a specific link group
            for graph in self.linked_groups[group]:
                graph.set_x_bounds(min_x, max_x)
        else:
            # Set bounds for all graphs
            for graph in self.graphs:
                graph.set_x_bounds(min_x, max_x)
                
        # Save to history if not already there
        if not self.history or (self.history[-1][0] != min_x or self.history[-1][1] != max_x):
            self.history.append((min_x, max_x))
            self.history_position = len(self.history) - 1
                
        # Update display if already shown
        if self.fig is not None:
            self.update_display()
    
    def reset_bounds(self) -> None:
        """Reset the bounds of all graphs based on their data"""
        # First, reset each graph's bounds
        for graph in self.graphs:
            graph.reset_bounds()
            
        # Then synchronize linked groups
        for group in self.linked_groups.values():
            if not group:
                continue
                
            # Find the overall min and max for this group
            min_x = min(graph.min_x() for graph in group)
            max_x = max(graph.max_x() for graph in group)
            
            # Set the same bounds for all graphs in this group
            for graph in group:
                graph.set_x_bounds(min_x, max_x)
                
        # Save to history
        if not self.history:
            self.history_position = 0
            if self.graphs:
                self.history.append((self.graphs[0].min_x(), self.graphs[0].max_x()))
                
        # Update display if already shown
        if self.fig is not None:
            self.update_display()
    
    def show(self, figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Show the graph view
        
        Args:
            figsize: The size of the figure (width, height) in inches
        """
        # Clear any existing figure
        if self.fig is not None:
            plt.close(self.fig)
            
        # Create new figure
        self.fig = plt.figure(figsize=figsize)
        self.fig.canvas.manager.set_window_title(self.title)
        
        # If no graphs, show empty message
        if not self.graphs:
            plt.figtext(0.5, 0.5, self.empty_text, ha='center', va='center', fontsize=14)
            plt.tight_layout()
            plt.show()
            return
            
        # Create grid for graphs based on heights
        visible_graphs = [g for g in self.graphs if g.visible]
        if not visible_graphs:
            plt.figtext(0.5, 0.5, self.empty_text, ha='center', va='center', fontsize=14)
            plt.tight_layout()
            plt.show()
            return
            
        # Calculate grid heights based on graph heights
        total_height = sum(g.height for g in visible_graphs)
        heights = [g.height / total_height for g in visible_graphs]
        
        # Create grid with adjustable heights
        gs = GridSpec(len(visible_graphs), 1, height_ratios=heights, hspace=0.05)
        
        # Create axes for each graph
        self.axes = []
        for i, graph in enumerate(visible_graphs):
            ax = plt.subplot(gs[i, 0])
            self.axes.append(ax)
            
            # Connect x-axes for linked groups
            if i > 0:
                ax.sharex(self.axes[0])
                
            # Set up interaction
            self._setup_interaction(ax)
            
        # Render each graph
        for i, graph in enumerate(visible_graphs):
            graph.render(self.fig, self.axes[i])
            
        # Add navigation toolbar
        self._add_navigation()
            
        # Show the figure
        plt.tight_layout()
        plt.show()
        
    def update_display(self) -> None:
        """Update the display after changes to data or bounds"""
        if self.fig is None:
            return
            
        visible_graphs = [g for g in self.graphs if g.visible]
        
        # Update each graph
        for i, graph in enumerate(visible_graphs):
            if i < len(self.axes):
                # Clear the axis
                self.axes[i].clear()
                
                # Render the graph
                graph.render(self.fig, self.axes[i])
                
        # Redraw the figure
        self.fig.canvas.draw_idle()
        
    def _setup_interaction(self, ax: plt.Axes) -> None:
        """
        Set up interaction handlers for the given axis
        
        Args:
            ax: The matplotlib Axes to set up interaction for
        """
        # Mouse events
        ax.figure.canvas.mpl_connect('button_press_event', self._on_press)
        ax.figure.canvas.mpl_connect('button_release_event', self._on_release)
        ax.figure.canvas.mpl_connect('motion_notify_event', self._on_motion)
        ax.figure.canvas.mpl_connect('scroll_event', self._on_scroll)
        
    def _add_navigation(self) -> None:
        """Add navigation buttons to the figure"""
        # Add a small subplot for navigation controls
        nav_ax = self.fig.add_axes([0.01, 0.01, 0.1, 0.05])
        btn_back = Button(nav_ax, 'Back')
        btn_back.on_clicked(self._on_back)
        
        nav_ax = self.fig.add_axes([0.12, 0.01, 0.1, 0.05])
        btn_forward = Button(nav_ax, 'Forward')
        btn_forward.on_clicked(self._on_forward)
        
        nav_ax = self.fig.add_axes([0.23, 0.01, 0.1, 0.05])
        btn_reset = Button(nav_ax, 'Reset')
        btn_reset.on_clicked(self._on_reset)
        
    def _on_press(self, event) -> None:
        """
        Handle mouse press events
        
        Args:
            event: The matplotlib mouse event
        """
        if event.inaxes is None:
            return
            
        # Start selection
        self.selecting = True
        self.selection_start = event.xdata
        
    def _on_release(self, event) -> None:
        """
        Handle mouse release events
        
        Args:
            event: The matplotlib mouse event
        """
        if not self.selecting:
            return
            
        self.selecting = False
        
        # If we have a valid selection, zoom to it
        if event.inaxes is not None and self.selection_start is not None:
            self.selection_end = event.xdata
            
            # Make sure start < end
            start, end = sorted([self.selection_start, self.selection_end])
            
            # Only zoom if selection is large enough
            if abs(end - start) > (self.graphs[0].max_x() - self.graphs[0].min_x()) * 0.01:
                self.set_x_bounds(start, end)
                
        self.selection_start = None
        self.selection_end = None
        
    def _on_motion(self, event) -> None:
        """
        Handle mouse motion events
        
        Args:
            event: The matplotlib mouse event
        """
        if event.inaxes is None:
            return
            
        # Update current time
        self.current_time = event.xdata
        
        # Update all graphs
        for graph in self.graphs:
            graph.current_time = self.current_time
            
        # Draw selection rectangle if selecting
        if self.selecting and self.selection_start is not None:
            # Clear previous selection rectangle
            self.update_display()
            
            # Draw new rectangle
            for ax in self.axes:
                ax.axvspan(self.selection_start, event.xdata, alpha=0.2, color='blue')
                
            self.fig.canvas.draw_idle()
            
    def _on_scroll(self, event) -> None:
        """
        Handle mouse scroll events
        
        Args:
            event: The matplotlib mouse event
        """
        if event.inaxes is None:
            return
            
        # Zoom in/out around the cursor position
        if not self.graphs:
            return
            
        # Get current bounds
        min_x = self.graphs[0].min_x()
        max_x = self.graphs[0].max_x()
        range_x = max_x - min_x
        
        # Scale factor
        scale = 0.1
        
        # Zoom in/out
        if event.button == 'up':  # Zoom in
            new_range = range_x * (1 - scale)
        else:  # Zoom out
            new_range = range_x * (1 + scale)
            
        # Calculate new bounds centered on cursor
        center = event.xdata
        new_min = center - new_range / 2
        new_max = center + new_range / 2
        
        # Apply new bounds
        self.set_x_bounds(new_min, new_max)
        
    def _on_back(self, event) -> None:
        """
        Handle back button clicks
        
        Args:
            event: The matplotlib button event
        """
        if self.history_position > 0:
            self.history_position -= 1
            min_x, max_x = self.history[self.history_position]
            
            # Apply without adding to history
            for graph in self.graphs:
                graph.set_x_bounds(min_x, max_x)
                
            self.update_display()
            
    def _on_forward(self, event) -> None:
        """
        Handle forward button clicks
        
        Args:
            event: The matplotlib button event
        """
        if self.history_position < len(self.history) - 1:
            self.history_position += 1
            min_x, max_x = self.history[self.history_position]
            
            # Apply without adding to history
            for graph in self.graphs:
                graph.set_x_bounds(min_x, max_x)
                
            self.update_display()
            
    def _on_reset(self, event) -> None:
        """
        Handle reset button clicks
        
        Args:
            event: The matplotlib button event
        """
        self.reset_bounds()
        
    def deselect_all(self) -> None:
        """Deselect all graphs"""
        for graph in self.graphs:
            graph.deselect()
            
    def __getitem__(self, graph_name: str) -> Graph:
        """
        Get a graph by name using dictionary-like syntax
        
        Args:
            graph_name: The name of the graph to get
            
        Returns:
            The Graph with the given name
            
        Raises:
            KeyError: If no graph with the given name exists
        """
        if graph_name in self._graphs_by_name:
            return self._graphs_by_name[graph_name]
        raise KeyError(f"No graph named '{graph_name}' found")
        
    def __str__(self) -> str:
        return f"GraphView({len(self.graphs)} graphs)"
