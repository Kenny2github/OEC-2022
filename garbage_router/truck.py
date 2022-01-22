from dataclasses import dataclass, field
from .cmdargs import args
from .enums import PROCESSABLE, RESULTS, NodeType
from .waste import Waste
from .node import Node

POWER = 5

@dataclass
class Truck:
    contents: list[Waste] = field(default_factory=list)

    def processable(self, at: Node) -> int:
        if at.type == NodeType.WASTE:
            return at.plastic_amt
        return sum(waste.amount for waste in self.contents
                   if PROCESSABLE[at.type] == waste.status)

    def done(self, waste_count: int) -> bool:
        return len(self.contents) == waste_count \
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
