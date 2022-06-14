

periods = [1,2,3]
demand = {1:300,2:400,3:500}
locations = ['LA','NY']
labor_hours = {'LA':1.5,'NY':2.0}
production_cost = {'LA':400,'NY':350}
labor_hours_availability = 420 # hour/period/location
inventory_cost = 100 #$/period
initial_inventory = 200

from gurobipy import Model,GRB


model = Model("Airco") 


model.setParam('outputFlag',True)
model.setParam('timeLimit',60)


x = model.addVars(locations,periods, name="x")
y = model.addVars(periods, name="y")

total_production_cost = sum(production_cost[i] * x[i,j] for i in locations for j in periods)
total_inventory_cost  = inventory_cost * sum(y[j] for j in periods)

total_cost = total_production_cost + total_inventory_cost 

model.setObjective(total_cost, GRB.MINIMIZE)

# Capacity constraints
model.addConstrs( (labor_hours[i] * x[i,j] <= labor_hours_availability 
                  for i in locations for j in periods), "const_max_labor_hours")

# Inventory constraints
j_first = periods[0]
model.addConstr(sum(x[i,j_first] for i in locations) + initial_inventory == demand[j_first] + y[j_first], "const_flow_conservation_first_period")

model.addConstrs( (sum(x[i,j] for i in locations) + y[j-1] == demand[j] + y[j] for j in periods[1:-1]), "const_flow_conservation_intermediate_periods")

j_last = periods[-1]
model.addConstr(sum(x[i,j_last] for i in locations) + y[j_last-1] == demand[j_last], "const_flow_conservation_last_period")

        
# Solve the model
model.optimize()


#------------------------------------------------------------------------------
# Print solution
if model.status == GRB.Status.OPTIMAL:
    print('\nOptimal solution found in {}s'.format(round(model.Runtime,2)))
    print('\nThe total cost is {}'.format(model.objVal))
    print('\nThe optimal solution is:')
    x_sol = model.getAttr('x', x) # get the optimal solution
    for i in locations:
        print('\nLocation {}'.format(i))
        for j in periods:
            print('Produce {} air conditioners in month {}'.format(x_sol[i,j],j))
        
else:
    print('No solution! Optimization status is {}'.format(model.status))
    print('See http://www.gurobi.com/documentation/8.0/refman/optimization_status_codes.html for status code.')
#------------------------------------------------------------------------------
    
model.write('Airco.lp')