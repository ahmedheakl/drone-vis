"""Connect to your drone and run your CV models
Usage
------------------
    
    $ dronevis [--options]
Get data about the arguments
    $ dronevis -help
Or just run the following to the default
    
    $ dronevis
    
    
Version
------------------
 - dronevis v0.2.0
"""
from termcolor import colored
from pyfiglet import Figlet
from rich import print as rprint
from rich.console import Console
from dronevis.drone_connect.drone import Drone
from dronevis.utils.parser import parse, print_available_control
import sys


def print_navdata(navdata):
    "Print the navdata as RAW text"
    print(navdata["navdata_demo"]["battery_percentage"])



def main() -> None:
    args = parse()
    drone = Drone()
    console = Console()
    print(colored(Figlet(font="big").renderText("DRONE VIS"), "green"))
    rprint("[violet]Welcome to DroneVis CLI")
    rprint(
        "DroneVis is a full-compatible library for [green]controlling your drone [white]and\nrunning your favourite [green]computer vision algorithms in real-time[white]"
    )
    if args.mode == "cli":
        while True:
            console.print("Connecting to your drone ...", style="bold black on white")
            print_available_control()
            rprint("Please [yellow]choose a control id [white]from the table.\n[green]To exit press 'q'")
            index = input("> ")
            if index == "q":
                # TODO: handle drone stopping
                # drone.stop()
                sys.exit()
            print("")
            
    else:
        raise NotImplementedError(colored("Drone tests are NOT yet implemented", "yellow"))


