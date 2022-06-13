from gurobipy import GRB,Model

#period
t = [i+1 for i in range(26)]
print(t)

r = {1:50,2:60,3:70,4:70,5:70,6:70,
        7:70,8:70,9:70,10:70,11:60,12:50,13:50,
        14:50,15:50,16:60,17:70,18:70,19:70,20:70,
        21:70,22:80,23:80,24:80,25:80,26:80}

#print(r[1])

C = {1:200,2:200,3:200,4:200,5:200,6:200,7:0,
          8:220,9:220,10:220,11:220,12:220,13:220,14:160,
          15:50,16:250,17:250,18:250,19:250,20:250,
          21:250,22:100,23:230,24:230,25:230,26:150}

initial_inventory = 100
ending_inventoy = 150

h = 1 #holding cost
K = 300 #setup cost



model = Model("lot_release")

Q = model.addVars(t, name = "Q")
x = model.addVars(t, vtype = GRB.BINARY, name = "x")
I = model.addVars(t, name = "I")

x_sum = sum(x[t] for t in t)
I_sum = sum(I[t] for t in t)

cost = 300*x_sum + I_sum


model.setObjective(cost, GRB.MINIMIZE)


# Initial Inv
model.addConstr(I[1] == 100 + Q[1] - r[1])


i = 2
while i < 26:
	model.addConstr(I[i] == I[i-1] + Q[i] - r[i])
	i = i + 1

#ending Inv
model.addConstr(150 == I[25] + Q[26] - r[26])

model.addConstrs(I[t] >= 0 for t in t)

#max constrant 
model.addConstrs(Q[t] <= x[t]*250 for t in t)

#capcity constraint 
model.addConstrs(Q[t] <= C[t] for t in t)

model.optimize()


if model.status == GRB.Status.OPTIMAL:
	Q_list = []
	I_list = []
	for t in t:
		Q_list.append(round(Q[t].X))
		I_list.append(round(I[t].X))
	print()
	print("Lot Release\n", Q_list)
	print()
	print("Inventory\n", I_list)

#print(sum(I_list))
final_cost = 10*300 + sum(I_list)
print()
print("final cost is $", final_cost)

model.write('lot_release.lp')
