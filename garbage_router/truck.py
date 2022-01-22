from dataclasses import dataclass, field
from .cmdargs import args
from .enums import PROCESSABLE, RESULTS, NodeType
from .waste import Waste
from .node import Node
from .data_io import read_data

POWER = 5

@dataclass
class Truck:
    contents: list[Waste] = field(default_factory=list)

    def processable(self, at: Node) -> int:
        if at.type == NodeType.WASTE:
            return at.plastic_amt
        return sum(waste.amount for waste in self.contents
                   if PROCESSABLE[at.type] == waste.status)

    def done(self) -> bool:
        """If not all waste is """
        return len(self.contents) == len(read_data()['waste']) \
            and all(waste.done for waste in self.contents)

    def desirability(self, cur_node: Node, next_node: Node) -> float:
        dist = cur_node.dist(next_node)
        weight = self.processable(next_node)
        loss = dist * next_node.risk * weight

        return weight / (dist + loss + 1)

    def update(self, node: Node) -> None:
        for waste in self.contents:
            if PROCESSABLE[node.type] == waste.status:
                waste.status = RESULTS[node.type]
