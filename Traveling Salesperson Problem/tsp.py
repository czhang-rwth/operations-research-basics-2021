from gurobipy import *
import itertools
import math

# nodes is a dict of the form {0: (1,2), 1: (3,8), ...} which means that node 0 has coordinates (1,2), node 1 has coordinates (3,8) and so on
def solve(nodes: dict):
    # TODO: Add a function that computes the euclidian distance between two points x and y. The distances are the costs in the objective function.
    # HINT: You are allowed to change the input of the function.
    def euclidian(x, y):
        return ((x[0] - y[0])**2 + (x[1] - y[1])**2)**0.5

    model = Model("Traveling Salesperson Problem")
    model.modelSense = GRB.MINIMIZE

    # Store all identifiers of nodes in a list
    node_ids = list(nodes.keys())
    # TODO: Create a list which contains all possible pairs of nodes once. If you have nodes 0 and 1, the list should contain either the pair (0, 1) or the pair (1, 0) but not both
    # HINT: itertools combinations
    node_pairs = itertools.combinations(node_ids, 2)

    # VARIABLES
    x = {}
    for (i, j) in node_pairs:
        x[i, j] = model.addVar(vtype="B", name=f"x_{i}_{j}", obj=euclidian(nodes[i], nodes[j]))

    # TODO: Add potential additional variables.

    model.update()

    # TODO: Add all the constraints
    model.addConstrs(quicksum(x[i] for i in list(x) if i[0] == v or i[1] == v) == 2 for v in node_ids)

    subsets = {}
    n = 0
    for i in range(1, len(node_ids)):
        for j in itertools.combinations(node_ids, i):
            subsets[n] = list(j)
            n += 1

    model.addConstrs(quicksum(x[i] for i in list(x) if (not i[0] in subsets[num] and i[1] in subsets[num]) 
                                                    or (i[0] in subsets[num] and not i[1] in subsets[num])) >= 2 for num in subsets.keys())

    model.optimize()

    if model.status == GRB.OPTIMAL:
        print('\nObjective: %g\n' % model.ObjVal)
        for (i, j) in node_pairs:
            if model.getVarByName(f"x_{i}_{j}").x == 1:
                print(f"Used road between {i} and {j}")
    
    return model