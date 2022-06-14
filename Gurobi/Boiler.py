from gurobipy import GRB,Model

boilers = [1,2,3,4]
turbines = [1,2,3]

boiler_production_lb = {1:400, 2:500, 3:300, 4:240}
boiler_production_ub = {1:900, 2:700, 3:600, 4:800}
boiler_steam_cost = {1:9, 2:7, 3:8, 4:6}
boiler_fixed_cost = {1:160, 2:200, 3:190, 4:250}

turbine_processing_lb = {1:100, 2:400, 3:300}
turbine_processing_ub = {1:700, 2:800, 3:600}
turbine_processing_cost = {1:9, 2:4, 3:6}
turbine_power_output = {1:7, 2:3, 3:6}

model = Model("Boilers")
x = model.addVars(boilers, vtype = GRB.BINARY, name = "x")
y = model.addVars(turbines, vtype = GRB.BINARY, name = "y")

a = model.addVars(boilers, name = "a")
b = model.addVars(turbines, name = "b")

model.setObjective(x.prod(boiler_fixed_cost) + a.prod(boiler_steam_cost) + b.prod(turbine_processing_cost), GRB.MINIMIZE)

model.addConstr(b.prod(turbine_power_output) >= 9000)
model.addConstr(a.sum() == b.sum())

model.addConstrs(boiler_production_lb[i] * x[i] <= a[i] for i in boilers)
model.addConstrs(boiler_production_ub[i] * x[i] >= a[i] for i in boilers)
model.addConstrs(turbine_processing_lb[j] * y[j] <= b[j] for j in turbines)
model.addConstrs(turbine_processing_ub[j] * y[j] >= b[j] for j in turbines)


# Solve the model
model.optimize()

#------------------------------------------------------------------------------
# Print solution
if model.status == GRB.Status.OPTIMAL:
    print('\nOptimal solution found in {}s'.format(round(model.Runtime,2)))
    print('\nThe total cost is {}'.format(model.objVal))
    print('\nThe optimal solution is:')
    x_sol = model.getAttr('x', x) # get the optimal solution
    for i in boilers:
        print("Boiler {} produce {} steam".format(i, a[i]))
    for j in turbines:
    	print("turbines {} process {} steam".format(j, b[j]))
        
        
else:
    print('No solution! Optimization status is {}'.format(model.status))
    print('See http://www.gurobi.com/documentation/8.0/refman/optimization_status_codes.html for status code.')
#------------------------------------------------------------------------------
    
model.write('Boiler.lp')