from gurobipy import GRB,Model

m = Model('Markov-chain')
m.setParam('OutputFlag', True)

pi1 = m.addVar(name='pi1')
pi2 = m.addVar(name='pi2')
pi3 = m.addVar(name='pi3')
#pi4 = m.addVar(name='pi4')
#pi5 = m.addVar(name='pi5')
#pi6 = m.addVar(name='pi6')


m.addConstr(pi1 + pi2 + pi3 == 0)
m.addConstr(0.5*pi1 + (1/3)*pi2 + 0.5*pi3 == pi1)
m.addConstr(0.3*pi1 + (1/3)*pi2 + 0.5*pi3 == pi2)
m.addConstr(0.2*pi1 + (1/3)*pi2  == pi1)


m.setObjective(0, GRB.MINIMIZE)
m.write("Markov-chain.lp")
m.optimize()

print()
print(pi1.X)
print(pi2.X)
print(pi3.X)
#print(pi4.X)
#print(pi5.X)
#print(pi6.X)

