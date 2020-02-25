# File: consones.py
# Authors: Zack Fitzsimmons (zfitzsim@holycross.edu),
#          Martin Lackner (lackner@dbai.tuwien.ac.at)


from pysat.solvers import Glucose3
import itertools


# permute columns such that all rows
# have the consecutive ones property
def solve_sat(matrix):
    def leftof(x, y):
        return x * num_cols + y + 1
    STEP = 5

    g = Glucose3()
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    if num_cols <= 10:
        cols = range(num_cols)
    else:
        cols = range(10)
    while True:
        # transitivity
        for x, y, z in itertools.combinations(cols, 3):
            # leftof(x,y) and leftof(y,z) imples leftof(x,z) =
            # not leftof(x,y) or not leftof(y,z) or leftof(x,z) =
            g.add_clause([-leftof(x, y), -leftof(y, z), leftof(x, z)])
        # totality
        for x, y in itertools.combinations(cols, 2):
            g.add_clause([-leftof(x, y), -leftof(y, x)])
            g.add_clause([leftof(x, y), leftof(y, x)])
        constraints = set()
        for i in range(num_rows):
            ones = []
            zeros = []
            for j in cols:
                if matrix[i][j] == 1:
                    ones.append(j)
                if matrix[i][j] == 0:
                    zeros.append(j)
            for x, y in itertools.combinations(ones, 2):
                for z in zeros:
                    # NOT(leftof(x,z) and leftof(z,y)) =
                    constraints.add((-leftof(x, z), -leftof(z, y)))
                    # NOT(leftof(y,z) and leftof(z,x)) =
                    constraints.add((-leftof(y, z), -leftof(z, x)))
        for c in constraints:
            g.add_clause(c)

        if not g.solve():
            return None
        if len(cols) == num_cols:
            break
        cols = range(min(num_cols, len(cols)+STEP))

    pos = [0] * len(cols)
    model = g.get_model()
    for x in cols:
        for y in cols:
            if leftof(x, y) in model:
                pos[x] += 1
    return [a[1] for a in sorted(zip(pos, cols), reverse=True)]
