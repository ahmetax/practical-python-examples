# Author: Ahmet Aksoy
# Date: 26.05.2026
# Python3.12 Ubuntu 24.04

"""
Poetry Package Management Example
Demonstrates how packages installed via Poetry (like 'rich') 
can be utilized within a managed virtual environment.
"""

import sys
from rich.console import Console
from rich.table import Table


def display_environment_info() -> None:
    """Uses the third-party 'rich' package to display system and environment parameters."""
    console = Console()
    
    # Construct a highly visual CLI output table
    table = Table(title="Poetry Managed Environment Metadata")
    
    table.add_column("Parameter", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="left", style="magenta")
    
    table.add_row("Python Executable Path", sys.executable)
    table.add_row("Python Version", sys.version.split()[0])
    table.add_row("Rich Library Status", "Successfully Resolved via Poetry")
    
    console.print(table)


if __name__ == "__main__":
    display_environment_info()