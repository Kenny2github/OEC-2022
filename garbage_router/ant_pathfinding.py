from random import choices

from garbage_router.enums import NodeType
from garbage_router.waste import Waste
from .node import Node
from .truck import Truck

NUM_ANTS = 4

def run_ant(nodes: list[Node],
            pheromones: dict[tuple[Node, Node], float]) -> list[Node]:
    ant = Truck()
    nodes = nodes[:]
    # must visit all waste notes
    unvisited = {node for node in nodes if node.type == 'waste'}
    prev_node = nodes[0]
    path: list[Node] = []
    while not ant.done():
        path.append(prev_node)
        if prev_node.type == NodeType.WASTE:
            unvisited.discard(prev_node)
            ant.contents.append(Waste(prev_node.plastic_amt))
            nodes.remove(prev_node) # don't visit the same waste node twice
        ant.update(prev_node)
        weights = [ant.desirability(prev_node, node)
                   * pheromones[prev_node, node]
                   for node in nodes
                   if node != prev_node]
        min_weight = min(weights)
        weights = [weight - min_weight for weight in weights]
        prev_node, = choices([node for node in nodes
                              if node != prev_node], weights)
    return path
