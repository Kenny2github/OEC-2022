from dataclasses import dataclass
from .node import Node
from .data_io import read_data

@dataclass
class Truck:
    unprocessed: int = 0
    locally_sorted: int = 0
    regionally_sorted: int = 0
    recycled: int = 0

    def processable(self, at: Node) -> int:
        """Return the value of one of the attributes of the truck,
        based on what type of node ``at`` is.
        """
        return getattr(self, {
            'local_sorting_facility': 'unprocessed',
            'regional_sorting_facility': 'locally_sorted',
            'regional_recycling_facility': 'regionally_sorted'
        }[at.type])

    def done(self) -> bool:
        """If not all waste is """
        return self.recycled >= read_data()['total_waste']

    def desirability(self, cur_node: Node, next_node: Node) -> float:
        dist = cur_node.dist(next_node)
        if next_node.type == 'waste':
            return 1 / dist
        loss = dist * next_node.risk
        return self.processable(next_node) / (dist * loss)