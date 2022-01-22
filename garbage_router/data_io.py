from __future__ import annotations
from functools import cache
from csv import reader, writer
from typing import TypedDict
from garbage_router.enums import NodeType

from garbage_router.waste import Waste
from .cmdargs import args
from .node import Node

class ReadData(TypedDict):
    nodes: list[Node]
    waste: list[Waste]

@cache
def read_data() -> ReadData:
    nodes: list[Node] = []
    with open(args().input) as infile:
        for row in reader(infile):
            nodes.append(Node.from_csv_row(row))
    waste: list[Waste] = [Waste(node.plastic_amt) for node in nodes
                          if node.type == NodeType.WASTE]
    return ReadData(
        nodes=nodes,
        waste=waste,
    )

def write_data(path: list[Node]):
    with open(args().output, 'w', newline='') as outfile:
        csv_writer = writer(outfile)
        for node in path:
            csv_writer.writerow((node.id, node.lat, node.long,
                                 node.type.value, node.plastic_amt, node.risk))