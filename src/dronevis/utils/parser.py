import argparse
from rich_argparse import RichHelpFormatter
from dronevis import __version__
from rich.console import Console
from rich.table import Table


def parse():
    parser = argparse.ArgumentParser(
        prog="DroneVis",
        description="Parse argument to run a drone test or full CLI",
        epilog="Enjoy the drone experience! \N{slightly smiling face}",
        formatter_class=RichHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Version: {__version__}",
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="cli",
        choices=["cli", "test"],
        help="whether to run full CLI or just run a simple drone test",
    )
    parser.add_argument(
        "-n",
        "--navdata",
        action="store_true",
        help="whether to acquire navigation data from the drone"
    )
    parser.add_argument(
        "-g",
        "--gps",
        action="store_true",
        help="whether to acquire GPS location from the drone"
    )
    
    args = parser.parse_args()
    return args

def print_available_control():
    table = Table()

    table.add_column("Control ID", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Status", justify="right", style="green")

    controls = [
        "Up",
        "Down",
        "Right",
        "Left",
        "Forward",
        "Backward",
        "Rotate Left",
        "Rotate Right",
        "Takeoff",
        "Hover",
        "Reset",
        "Emergency",
        "Flip",
    ]

    for i, control in enumerate(controls, start=1):
        valid = "✅" if i < 13 else "❌"
        table.add_row(f"{i}", control, valid)

    console = Console()
    console.print(table)
