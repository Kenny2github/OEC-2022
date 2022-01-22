from QoR import validator
from garbage_router.ant_pathfinding import run_rounds
from garbage_router.cmdargs import args
from garbage_router.data_io import read_data, write_data

if args().draw:
    from garbage_router.gui import main
    main(args().a, args().b)
else:
    nodes = read_data()['nodes']
    path, qor = run_rounds(nodes)
    write_data(path)
    validator(args().input[:-4], args().output[:-4], args().a, args().b)