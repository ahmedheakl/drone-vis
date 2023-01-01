import argparse
from rich_argparse import RichHelpFormatter
from dronevis import __version__
from rich.console import Console
from rich.table import Table
import sys
from dronevis.drone_connect import Drone, DemoDrone
from typing import Union, Callable, Dict
from rich import print as rprint
from rich.console import Console


class DroneCli:
    """Encapsulate all CLI needed methods"""

    def parse(self) -> argparse.Namespace:
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

        args = parser.parse_args()
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

    def not_implemeneted(self) -> None:
        """Dummy method from not implemented methods

        Raises:
            NotImplementedError: main exception error
        """
        raise NotImplementedError("Not implemented yet")

    def index_to_control(self, drone: Union[Drone, DemoDrone]) -> Dict[str, Callable]:
        """Get a list a with keys as commands index and values
        as commands methods

        Args:
            drone (Union[Drone, DemoDrone]): drone instance

        Returns:
            Dict[str, Callable]: a dictionary mapping from index to control methods
        """
        assert drone, "You provided a Null instance of the drone"
        assert isinstance(
            drone, (Drone, DemoDrone)
        ), "Please provide a valid drone instance"

        def cli_exit():
            drone.stop()
            sys.exit()

        available_commands = {
            "q": cli_exit,
            "1": drone.up,
            "2": drone.down,
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
            "14": self.not_implemeneted,
        }

        return available_commands

    def __call__(
        self,
        args: argparse.Namespace,
        drone: Union[Drone, DemoDrone],
    ) -> None:
        """Main loop for drone connection and control

        Args:
            args (argparse.NameSpace): args from user input
            drone (Union[Drone, DemoDrone]): drone instance

        Raises:
            NotImplementedError: drone testing is not implemented
        """
        assert isinstance(drone, (Drone, DemoDrone))

        # get commands
        available_commands = self.index_to_control(drone)

        # get console instance for pretty output
        console = Console()
        console.print("Connecting to your drone ...", style="bold black on black")

        # connect to drone
        drone.connect()
        # sleep(0.2)

        if args.mode == "cli":
            while True:
                self.print_available_control()
                rprint(
                    "Please [yellow]choose a control id [white]from the table.\n[green]To exit press 'q'"
                )

                # loop till the user provides a valid input
                while True:
                    index = input("> ")
                    if index not in available_commands.keys():
                        rprint("[red]Please a valid control id or press 'q' to exit")
                        continue
                    break

                command = available_commands[index]
                command()

                print("")

        else:
            raise NotImplementedError()
