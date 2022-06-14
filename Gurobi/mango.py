from gurobipy import GRB,Model

mango_type = [1,2]


model = Model("Mango")
x = model.addVars(mango_type, name = "x") #mango of type i sold to retail
y = model.addVar(name = "y") # total mangoes sold to retail
z = model.addVar(name = "z") # Total revenue from selling to retail
y = x[1] + x[2]

#a = 1000-x[1]
#b = 1000-x[2]
#c = 2.2*(1000-x[1]) + 3.1*(700-x[2])

model.setObjective(2.2*(1000-x[1]) + 3.1*(700-x[2]) + z , GRB.MAXIMIZE)

model.addConstrs(x[i] >= 0 for i in mango_type)
model.addConstr(y >= 0)
model.addConstr(z >= 0)
model.addConstr(x[1] <= 1000)
model.addConstr(x[2] <= 700)
model.addConstr(y == x[1] + x[2])
model.addConstr(x[2] >= 0.6*y)
model.addConstr(z <= 3.05*y - 50)
model.addConstr(z <= 3*y)
model.addConstr(z <= 2.5*y + 600)
# Solve the model
model.optimize()

#------------------------------------------------------------------------------
# Print solution
if model.status == GRB.Status.OPTIMAL:
    print('\nOptimal solution found in {}s'.format(round(model.Runtime,2)))
    print('\nThe total revenue is {}'.format(model.objVal))
    print('\nThe optimal solution is:')
    x_sol = model.getAttr('x', x) # get the optimal solution
    for i in mango_type:
        print("mango type {} sell {} units to retail ".format(i, x[i]))
    #print("\n total mangoes to sell to retail {}".format(y))
    print("\n total revenue from selling to retail {}".format(z))
    #print("\n total mango type 1 sold to local {}".format(a))
    #print("\n total mango type 2 sold to local {}".format(b))
    #print("\n total revenue from selling to local {}".format(c))
    

else:
    print('No solution! Optimization status is {}'.format(model.status))
    print('See http://www.gurobi.com/documentation/8.0/refman/optimization_status_codes.html for status code.')
#------------------------------------------------------------------------------
    
model.write('mango.lp')