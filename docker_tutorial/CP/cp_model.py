import glob

import os
import os.path as pt

from CP.cp_utils import visualize_solution
from CP.instance_solver import solve_instance
from minizinc import Model, Solver

from CP.parameters import *


def cp_solver():
    solver = Solver.lookup('gecode')
    model = Model(DEFAULT_MODEL_FILE)

    # Define a new instance for each input file
    for instance_file in sorted(glob.glob(pt.join(DEFAULT_INSTANCES_DIR, '*'))):
        solve_instance(instance_file, solver, model)

    for file in os.listdir(DEFAULT_CP_OUTPUT_DIR):
        if 'out-' in file:
            with open(pt.join(DEFAULT_CP_OUTPUT_DIR, file)) as fin:
                print(file)
                visualize_solution(pt.join(DEFAULT_CP_OUTPUT_DIR, file))
