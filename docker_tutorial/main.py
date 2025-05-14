from CP.cp_model import cp_solver
from SAT.sat_model import sat_solver

if __name__ == '__main__':
    options = {'cp': cp_solver, 'sat': sat_solver}
    mod = input('CP or SAT: ').lower()
    funct_to_use = options.get(mod, lambda: print('option not valid'))
    funct_to_use()
