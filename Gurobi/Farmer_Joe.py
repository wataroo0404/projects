from gurobipy import GRB,Model

m = Model('Farmer_Joe')
m.setParam('OutputFlag', True)

x = m.addVar(name='x')
y = m.addVar(name='y')

m.addConstr(x + y <= 7, name='max num of acres avaiable')
m.addConstr(10*x + 4*y <= 40, name='max num of hours avaiable')
m.addConstr(10*y >= 30, name='min bushel of corn')

m.setObjective(25*4*x + 10*3*y, GRB.MAXIMIZE)
m.write("Farmer_Joe.lp")
m.optimize()

status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'}
status = m.status

print('\nThe optimization status is {}'.format(status_code[status]))
if status == 2:
	print('Optimal Solution:')
	print('Acres of wheat = {}'.format(x.x))
	print('Acres of corn = {}'.format(y.x))
	print('Revenue = ${}'.format(m.objVal))
