import itertools
from gurobipy import *

nodes = {
    0: (1,5),
    1: (2,8),
    3: (4,2),
    4: (9,3),
    5: (8,5),
    6: (6,6),
    7: (7,4),
    8: (3,9),
    9: (10,1),
    10: (1,8),
    11: (3,8)
}

print(nodes.keys())
print(nodes[0])
print(nodes[0][1])

node_ids = list(nodes.keys())
x = {}
for (i, j) in itertools.combinations(node_ids, 2):
    x[i,j] = 1
print(x)
print(quicksum(x[i,j] for i, j in itertools.combinations(node_ids, 2)))
print(x[0, 4])
print(len(x))

print(type(nodes))
print(type(x))
print(type(itertools.combinations(node_ids, 2)))

x = list(x)
print(x)
y = list(itertools.combinations(node_ids, 2))
print(y)
print(y[3])
print( x == y)