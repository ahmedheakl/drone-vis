"""implementation for dronevis CLI"""
import argparse
import logging
from typing import Callable, Dict, Optional, Sequence
import sys

from rich_argparse import RichHelpFormatter
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from dronevis import __version__
from dronevis.abstract.base_drone import BaseDrone


_LOG = logging.getLogger(__name__)


class DroneCli:
    """Encapsulate all CLI needed methods"""

    def parse(self, arguments: Optional[Sequence[str]] = None) -> argparse.Namespace:
        """Argument parser to get user inputs

        Returns:
            argparse.Namespace: namespace with all user input arguments
        """
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
            "--drone",
            type=str,
            default="demo",
            choices=["demo", "real"],
            help="whether to use a demo drone or a real drone",
        )
        parser.add_argument(
            "--log-level",
            dest="logger_level",
            type=str,
            choices=["debug", "info", "warning", "error", "critical"],
            default="info",
            help="Level for logger",
        )

        args = parser.parse_args(arguments)
        return args

    def print_available_control(self) -> None:
        """Print all drone available control, and mark them
        as either implemented with a green check mark or not implemented
        with a red X.
        """
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
            "Land",
            "Hover",
            "Reset",
            "Emergency",
            "Flip",
        ]

        for i, control in enumerate(controls, start=1):
            valid = "✅" if i < 14 else "❌"
            table.add_row(f"{i}", control, valid)

        console = Console()
        console.print(table)

    def _not_implemeneted(self) -> None:
        """Dummy method from not implemented methods

        Raises:
            NotImplementedError: main exception error
        """
        raise NotImplementedError("Not implemented yet")

    def index_to_control(self, drone: BaseDrone) -> Dict[str, Callable]:
        """Get a list a with keys as commands index and values
        as commands methods

        Args:
            drone (BaseDrone): Drone instance

        Returns:
            Dict[str, Callable]: A dictionary mapping from index to control methods
        """
        assert isinstance(drone, BaseDrone), "Please provide a valid drone instance"

        def cli_exit():
            drone.stop()
            sys.exit()

        available_commands = {
            "q": cli_exit,
            "1": drone.upward,
            "2": drone.downward,
            "3": drone.right,
            "4": drone.left,
            "5": drone.forward,
            "6": drone.backward,
            "7": drone.rotate_left,
            "8": drone.rotate_right,
            "9": drone.takeoff,
            "10": drone.land,
            "11": drone.hover,
            "12": drone.reset,
            "13": drone.emergency,
            "14": self._not_implemeneted,
        }

        return available_commands

    def __call__(
        self,
        args: argparse.Namespace,
        drone: BaseDrone,
    ) -> None:
        """Main loop for drone connection and control

        Args:
            args (argparse.NameSpace): Args from user input
            drone (BaseDrone): Drone instance

        Raises:
            NotImplementedError: Drone testing is not implemented
        """
        assert isinstance(
            drone, BaseDrone
        ), "Provided drone must implement the base drone interface"

        # get commands
        available_commands = self.index_to_control(drone)

        # get console instance for pretty output
        console = Console()
        console.print("Connecting to your drone ...", style="bold black on yellow")

        # connect to drone
        drone.connect()
        # sleep(0.2)

        if args.mode == "cli":
            while True:
                self.print_available_control()
                rprint(
                    "Please [yellow]choose a control id [white]from the table.\n"
                    + "[green]To exit press 'q'"
                )

                # loop till the user provides a valid input
                while True:
                    index = input("> ")
                    if index not in available_commands:
                        rprint("[red]Please a valid control id or press 'q' to exit")
                        continue
                    break

                command = available_commands[index]
                command()

                print("")

        else:
            raise NotImplementedError("Drone tests are not implemented yet")
