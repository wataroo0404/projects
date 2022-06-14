from gurobipy import GRB,Model

m = Model('Cheesecake')
m.setParam('OutputFlag', True)

x = m.addVar(name='A')
y = m.addVar(name='B')
z = m.addVar(name='C')

m.addConstr(4*x + 13*y + 8*z >= 55, name='min protein')
m.addConstr(2*x + 50*y + 120*z >= 400 , name='min calcium')
m.addConstr(x <= 4)
m.addConstr(y <= 2)
m.addConstr(z <= 5)

m.setObjective(3*x + 10*y + 8*z, GRB.MINIMIZE)
m.write("Diet.lp")
m.optimize()

status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'}
status = m.status

print('\nThe optimization status is {}'.format(status_code[status]))
if status == 2:
	print('Optimal Solution:')
	print('Servings of Oatmeal = {}'.format(x.x))
	print('Servings of Eggs = {}'.format(y.x))
	print('Servings of Milk = {}'.format(z.x))
	print('Minimum Cost = ${}'.format(m.objVal))
