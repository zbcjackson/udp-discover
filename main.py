# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from Node import Node
from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from time import sleep

node = Node()
if __name__ == '__main__':
    node.start()

    console = Console()
    console.clear()

    while True:
        table = Table()
        table.add_column("Node ID", no_wrap=True)
        table.add_column("Address", no_wrap=True)
        for (node_id, addr) in node.nodes.items():
            table.add_row(node_id, addr)
        table_centered = Align.center(table)
        console.print(table)
        sleep(1)
