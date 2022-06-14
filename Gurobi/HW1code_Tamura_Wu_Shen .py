from gurobipy import GRB,Model

row = [1,2,3,4,5,6] #row of array
col = [1,2,3,4,5,6] #column of array
num = [1,2,3,4,5,6] #number possible

model = Model("Puzzle")
x = model.addVars(row,col,num, vtype = GRB.BINARY, name = "x")
y = model.addVars(row,col, name = "y")
k = model.addVars(row,col,num, name = "k")
sumval = model.addVar(vtype=GRB.CONTINUOUS, name = "sumval")


model.setObjective(0, GRB.MINIMIZE)

# Each cell must take one value

model.addConstrs((x.sum(i,j,'*') == 1
                 for i in row
                 for j in col))

# Each value appears once per row

model.addConstrs((x.sum(i,'*',k) == 1
                 for i in row
                 for k in num))

# Each value appears once per column

model.addConstrs((x.sum('*',j,k) == 1
                 for j in col
                 for k in num))


for i in row:
	for j in col:
		model.addConstr(y[i,j] == sum(k * x[i,j,k] for k in num) )



model.addConstr(y[1,1] + y[1,2] + y[1,3] + y[2,1] == sumval)
model.addConstr(y[2,2] + y[2,3] == sumval)
model.addConstr(y[1,4] + y[1,5] + y[2,5] == sumval)
model.addConstr(y[1,6] + y[2,6] == sumval)
model.addConstr(y[2,4] + y[3,4] == sumval)
model.addConstr(y[3,1] + y[4,1] == sumval)
model.addConstr(y[3,2] + y[3,3] + y[4,3] == sumval)
model.addConstr(y[4,4] + y[5,4] == sumval)
model.addConstr(y[3,5] + y[3,6] + y[4,5] == sumval)
model.addConstr(y[4,6] + y[5,5] + y[5,6] == sumval)
model.addConstr(y[4,2] + y[5,1] + y[5,2] == sumval)
model.addConstr(y[6,1] + y[6,2] == sumval)
model.addConstr(y[5,3] + y[6,3] == sumval)
model.addConstr(y[6,4] + y[6,5] + y[6,6] == sumval)


model.optimize()




if model.status == GRB.Status.OPTIMAL:
    for i in row:
    	print_list = []
    	for j in col:
    		print_list.append(round(y[i,j].X))
    	print(print_list)
    		




model.write('Puzzle.lp')


