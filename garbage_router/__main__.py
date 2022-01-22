from garbage_router.cmdargs import args
from garbage_router.data_io import read_data
from garbage_router.gui import main

nodes = read_data(args().input)
main(nodes, args().a, args().b)