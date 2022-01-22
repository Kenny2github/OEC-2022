from random import choices
from .node import Node
from .truck import Truck

NUM_ANTS = 4

def run_ant(nodes: list[Node],
            pheromones: dict[tuple[Node, Node], float]) -> list[Node]:
    ant = Truck()
    # must visit all waste notes
    unvisited = {node for node in nodes if node.type == 'waste'}
    prev_node = nodes[0]
    path: list[Node] = []
    while not ant.done() and unvisited:
        path.append(prev_node)
        unvisited.discard(prev_node)
        weights = [ant.desirability(prev_node, node)
                   * pheromones[prev_node, node]
                   for node in nodes
                   if node != prev_node]
        prev_node, = choices([node for node in nodes
                              if node != prev_node], weights)
    return path
