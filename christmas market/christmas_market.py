from gurobipy import *

def solve(stands,
          temperature,
          amount,
          alcohol_content,
          sugar,
          calorific_value,
          price,
          cup_type,
          persons,
          budget,
          min_wine_total,
          environment,
          max_wine_per_stand):
    model = Model("Christmas ")

    model.modelSense = GRB.MAXIMIZE

    # variable x
    x = {}
    for p in persons:
        for s in stands:
            x[p, s] = model.addVar(name="x_%s_%s" % (p, s), lb=0, vtype=GRB.INTEGER)

    # TODO: Add potential additional variables.

    # variable y: whether person p visits the wine stand s
    #y = {}
    #for p in persons:
    #    for s in stands:
    #        y[p, s] = model.addVar(name="y_%s_%s" % (p, s), vtype=GRB.BINARY)

    model.setObjective(quicksum(x[p, s]*alcohol_content[s]/price[s] for s in stands for p in persons))

    model.update()

    # TODO: Add all contraints

    #x=0 => y=0; x>0 => y=1 
    #model.addConstrs(y[p, s] <= x[p, s] for p in persons for s in stands)
    
    #budget constraint
    model.addConstrs(quicksum(x[p, s]*price[s] for s in stands) <= budget[p] for p in persons)

    #every person p wants to drink at every stand s maximum max_wine_per_stand[p,s] cups hot wine
    model.addConstrs(x[p, s] <= max_wine_per_stand[p, s] for p in persons for s in stands)

    #Every person needs at least min_wine_total[p] cups of hot wine to enjoy the evening.
    model.addConstrs(quicksum(x[p, s] for s in stands) >= min_wine_total[p] for p in persons)

    #Some of the people, namely those for whom environment[p] takes the value True, 
    #can only drink their wine from an environmentally friendly drinking vessel, made of glass or ceramic. 
    #These people therefore only want to drink hot wine at a stand if it comes from such a vessel. 
    #(This is not covered by max_wine_per_stand.)
    model.addConstrs(x[p, s] == 0 for p in persons for s in stands 
                   if environment[p] and cup_type[s] != 'glass' and cup_type[s] != 'ceramic')

    model.optimize()

    # print solution
    if model.status == GRB.OPTIMAL:
        print('\n objective: %g\n' % model.ObjVal)
        for p in persons:
            for s in stands:
                if x[p, s].x >= 1:
                    print('%s drinks %i cups at %s' % (p, x[p, s].x, s))

    return model
