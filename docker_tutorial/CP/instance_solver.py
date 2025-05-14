from minizinc import Instance

import os
import os.path as pt

import json
import datetime

from CP.cp_utils import dump_statistics
from CP.parameters import *


def solve_instance(instance_file, solver, model):
    instance = Instance(solver, model)
    with open(instance_file) as fin:
        instance_data = json.load(fin)

    # Populate instance parameters
    for key, value in instance_data.items():
        instance[key] = value

    print(f'solving instance: {pt.basename(instance_file)}')

    result = instance.solve(timeout=datetime.timedelta(minutes=5),
                                        optimisation_level=5, free_search=True)

    dump_statistics(result.statistics, result.status)
    print()

    # Dump results and statistics on file
    os.makedirs(DEFAULT_CP_OUTPUT_DIR, exist_ok=True)
    output_basename = (f'out-{pt.splitext(pt.basename(instance_file))[0]}'
                       '.txt')
    stats_basename = (f'stats-{pt.splitext(pt.basename(instance_file))[0]}'
                      '.txt')
    with open(pt.join(DEFAULT_CP_OUTPUT_DIR, output_basename), 'w') as fout:
        fout.write(str(result))

    with open(pt.join(DEFAULT_CP_OUTPUT_DIR, stats_basename), 'w') as fout:
        dump_statistics(result.statistics, result.status, fout)
