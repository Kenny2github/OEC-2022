from __future__ import annotations
from functools import cache
from csv import reader, writer
from typing import TypedDict
from .enums import NodeType
from .waste import Waste
from .cmdargs import args
from .node import Node

class ReadData(TypedDict):
    nodes: list[Node]
    waste: list[Waste]

@cache
def read_data(path: str) -> list[Node]:
    nodes: list[Node] = []
    with open(path) as infile:
        for row in reader(infile):
            nodes.append(Node.from_csv_row(row))
    return nodes

def write_data(path: list[Node]):
    with open(args().output, 'w', newline='') as outfile:
        csv_writer = writer(outfile)
        for node in path:
            csv_writer.writerow(node.to_csv_row())