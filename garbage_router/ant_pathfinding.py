from math import erf
from random import choices
from .qor import validator
from .enums import NodeType
from .waste import Waste
from .node import Node
from .truck import Truck

NUM_ANTS = 1000
ROUNDS = 10

def run_ant(nodes: list[Node],
            pheromones: dict[tuple[Node, Node], float]) -> list[Node]:
    ant = Truck()
    nodes = nodes[:]
    # must visit all waste notes
    unvisited = {node for node in nodes if node.type == NodeType.WASTE}
    prev_node = nodes[0]
    path: list[Node] = []
    while 1:
        path.append(prev_node)
        if prev_node.type == NodeType.WASTE:
            unvisited.discard(prev_node)
            ant.contents.append(Waste(prev_node.plastic_amt))
            nodes.remove(prev_node) # don't visit the same waste node twice
        ant.update(prev_node)
        if ant.done():
            break
        #print('\n', ant.contents, 'getting weights-------------------------------')
        weights = [ant.desirability(prev_node, node)
                   * pheromones[prev_node, node]
                   for node in nodes
                   if node != prev_node]
        #print('\t', weights)
        min_weight = min(weights)
        weights = [weight - min_weight for weight in weights]
        #max_weight = max(weights)
        #weights = [erf(weight / max_weight) for weight in weights]
        #print('\t\t', weights)
        prev_node, = choices([node for node in nodes
                              if node != prev_node], weights)
    return path

def run_ants(nodes: list[Node], pheromones: dict[tuple[Node, Node], float],
             round_number: int, a: float, b: float) -> tuple[list[Node], list[float]]:
    paths = [run_ant(nodes, pheromones) for _ in range(max(1, NUM_ANTS // round_number))]
    map_nodes = [node.to_csv_row() for node in nodes]
    qors = [validator(
        map_nodes, [node.to_csv_row() for node in path],
        a, b
    ) for path in paths]
    return paths, qors

def qor_to_scaling(qor: float, worst: float) -> float:
    # bigger qor is worse
    # better qor => greater scaling
    return 2 - qor / worst

def run_rounds(nodes: list[Node], a: float, b: float) -> tuple[list[Node], float]:
    pheromones: dict[tuple[Node, Node], float] = {}
    for node1 in nodes:
        for node2 in nodes:
            pheromones[node1, node2] = 1.0
    prev_qbest = 0.0
    old_best = None
    for i in range(1, ROUNDS + 1):
        print('Round', i)
        paths, qors = run_ants(nodes, pheromones, i * len(nodes), a, b)
        if not paths:
            break
        qworst = max(qors)
        qbest = min(qors)
        old_best = paths[qors.index(qbest)]
        if qbest == prev_qbest:
            print('Converged to QoR of', qbest)
            break
        prev_qbest = qbest
        for path, qor in zip(paths, qors):
            if qor < 0:
                continue # something went wrong
            for j in range(len(path) - 1):
                pheromones[path[j], path[j+1]] *= qor_to_scaling(qor, qworst)
    return old_best, qbest
