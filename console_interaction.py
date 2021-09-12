import os

from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt


class ConsoleInteraction:

    def __init__(self):
        self.console = Console()
        self.prompt = Prompt

    @staticmethod
    def display_title():
        panel = Panel.fit("Welcome to [bold red]PanBox Password Manager[/bold red]")
        os.system('clear')
        print(panel)

    def greetings(self):
        options = ["Select a option bellow:",
                   "[bold]1)[/bold] Login",
                   "[bold]2)[/bold] Create New Account",
                   "[bold]q)[/bold] Exit"]

        while True:
            ConsoleInteraction.display_title()
            print('\n'.join(options))
            selected = self.prompt.ask("Make your choice", choices=['1', '2', 'q'])
            return selected


    def main_menu(self):
        """ TODO """
