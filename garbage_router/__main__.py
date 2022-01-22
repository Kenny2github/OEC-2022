from garbage_router.ant_pathfinding import run_ant
from garbage_router.node import Node
from garbage_router.data_io import read_data, write_data

nodes = read_data()['nodes']
print(nodes)
pheromones: dict[tuple[Node, Node], float] = {}
for node1 in nodes:
    for node2 in nodes:
        pheromones[node1, node2] = 1.0

write_data(run_ant(nodes, pheromones))
