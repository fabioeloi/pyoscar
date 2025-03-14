# PyOSCAR

A Python port of OSCAR's data visualization capabilities, designed for general-purpose data visualization.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## Overview

PyOSCAR is inspired by the OSCAR (Open Source CPAP Analysis Reporter) project's excellent visualization system, but reimagined as a Python library that can be used for any type of data visualization. This library provides a flexible, customizable framework for creating interactive graphs and visualizations.

## Features

- **Modular Graph Framework**: Support for multiple layers and customizable components
- **Multiple Chart Types**:
  - Line charts with customizable styles and markers
  - Bar charts with vertical/horizontal orientations
  - Summary charts for statistical visualization
  - Extensible system for custom chart types
- **Advanced Visualization Features**:
  - Interactive zooming and panning
  - Multiple synchronized graphs
  - Customizable axes and scales
  - Time series support with proper formatting
- **Statistical Features**:
  - Summary statistics visualization
  - Percentile ranges display
  - Min/max/mean/median indicators
- **Flexible and Extensible**:
  - Easy to add new visualization types
  - Customizable styling and appearance
  - Event handling system for interactivity

## Installation

### Using pip

```bash
pip install pyoscar
```

### From source

```bash
git clone https://github.com/fabioeloi/pyoscar.git
cd pyoscar
pip install -e .
```

## Quick Start

### Simple Line Graph

```python
from pyoscar.core import GraphView
from pyoscar.graphs import LineGraph
import numpy as np

# Create sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a graph view
view = GraphView("Simple Example")

# Create and configure a line graph
graph = LineGraph("Sine Wave", "Simple Sine Wave", "Amplitude")
graph.add_data(x, y)
graph.set_line_style(color="blue", line_width=2)

# Add graph to view and display
view.add_graph(graph)
view.show()
```

### Multi-Graph Dashboard

```python
# Create a view with multiple graphs
view = GraphView("Dashboard")

# Add a line graph
line_graph = LineGraph("Temperature", "Temperature Over Time", "°C")
line_graph.add_data(time_data, temp_data)
view.add_graph(line_graph)

# Add a bar graph
bar_graph = BarGraph("Energy", "Energy by Hour", "kWh")
bar_graph.add_data(hours, energy_data)
view.add_graph(bar_graph)

# Add a summary graph
summary = SummaryGraph("Statistics", "Daily Statistics")
summary.add_data_series(categories, values)
view.add_graph(summary)

# Display the dashboard
view.show()
```

## Documentation

For detailed documentation and examples, visit our [documentation](https://github.com/fabioeloi/pyoscar/wiki).

### Examples

The `examples` directory contains several example scripts demonstrating different features:

- `simple_demo.py`: Basic usage demonstration
- `line_graph_example.py`: Advanced line graph features
- `bar_graph_example.py`: Bar chart capabilities
- `summary_graph_example.py`: Statistical visualization
- `time_series_example.py`: Time series data handling
- `multi_graph_dashboard.py`: Complex dashboard creation

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming community for all contributors.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [OSCAR](https://www.sleepfiles.com/OSCAR/) project
- Built with [Matplotlib](https://matplotlib.org/) and [NumPy](https://numpy.org/)

## Contact

- GitHub Issues: For bug reports and feature requests
- Email: [fabioeloi@gmail.com](mailto:fabioeloi@gmail.com)
