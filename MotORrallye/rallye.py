from gurobipy import *

def solve(stations: list, distances: list, slick_routes: list, offroad_routes: list, tyres: dict):
    # TODO: add a function that computes the costs for each route on the track. The costs are the duration in minutes, possibly multiplied with a factor that represents the better or worse performance of a certain tyre type
    # HINT: You are allowed to change the input of the function.
    def costs(source, target, tyre): 
        if source == 5:
            is5 = 5
        else:
            is5 = 0

        if tyre == 'all_purpose':
            cost = distances[source][target] * tyres[tyre]
        elif tyre == 'slick':
            if (source, target) in slick_routes or (target, source) in slick_routes:
                cost = distances[source][target] * tyres[tyre]
            else:
                cost = distances[source][target]
        elif tyre == 'offroad':
            if (source, target) in offroad_routes or (target, source) in offroad_routes:
                cost = distances[source][target] * tyres[tyre]
            elif (source, target) in slick_routes or (target, source) in slick_routes:
                cost = distances[source][target] * 2
            else:
                cost = distances[source][target]

        return cost + is5

    model = Model("MotORrallye")
    model.modelSense = GRB.MINIMIZE

    # you might want to use this, but you don't have to
    tyre_types = tyres.keys()

    # VARIABLES
    x = {}
    for i in stations:
        for j in stations:
            if i != j:
                for t in tyre_types:
                    x[i, j, t] = model.addVar(vtype="B", name=f"x_{i}_{j}_{t}")

    y = {}
    for t in tyre_types:
        y[t] = model.addVar(vtype="B", name=f"y_{t}")

    # the Miller, Tucker, Zemlin counting variables
    r = {}
    for i in stations:
        r[i] = model.addVar(vtype=GRB.INTEGER, lb=1, ub=len(stations), name='r_i')
    r[0] = 1 
    r[5] = 5
    # TODO: add the r variables

    # TODO: add potential additional variables

    model.update()

    # TODO: add objective function, if you have not used the obj attribute 
    model.setObjective(quicksum(x[i,j,t]*costs(i,j,t) for i in stations for j in stations for t in tyre_types if i != j))

    # CONSTRAINTS

    # TODO: add all the constraints

    model.addConstrs(x[i,j,'all_purpose'] == 0 for i in stations for j in stations if i != j if (i, j) in offroad_routes or (j, i) in offroad_routes)

    model.addConstrs(x[i,j,'slick'] == 0 for i in stations for j in stations if i != j if (i, j) in offroad_routes or (j, i) in offroad_routes)

    model.addConstrs(quicksum(x[i,j,t] for j in stations for t in tyre_types if i != j) == 1 for i in stations)

    model.addConstrs(quicksum(x[i,j,t] for i in stations for t in tyre_types if i != j) == 1 for j in stations)

    model.addConstrs(quicksum(x[i,j,t] for i in stations for j in stations if i != j) == len(stations)*y[t] for t in tyre_types)

    model.addConstrs(r[i] + 1 <= r[j] + 1000*(1-x[i,j,t]) for t in tyre_types for i in stations for j in stations if i != j if j != 0)

    model.optimize()

    if model.status == GRB.OPTIMAL:
        print('\nObjective: %g\n' % model.ObjVal)
        for i in stations:
            for j in stations:
                if i != j:
                    for t in tyre_types:
                        if model.getVarByName(f"x_{i}_{j}_{t}").x == 1:
                            print(f"Used route between {i} and {j} with tyre {t}")
    
    return model