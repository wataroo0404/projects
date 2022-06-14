from gurobipy import *
from helper_functions import *
from pprint import pprint
import math
import pandas as pd
import csv

model = Model("inital_model")

# index
#units i

#df = pd.read_csv("clustering_output.csv")
##saved_column = df.cluster
#df = df.sort_values("Cluster")
#max_cluster = max(df.Cluster)
#keys_dict = {}
#for i in range(0,max_cluster+1):
#    keys_dict[i] = []
#
#for i in range(0,len(df.Cluster)):
#    keys_dict[df.Cluster[i]].append(df.BusinessUnit[i])

##################################################################################
#put the cluster number in a

key1 = [2500439,
2500448,
2500471,
2500507,
2500542,
2500628,
2500709,
2500782,
2500880,
2501231,
2501431,
2501432,
2501474,
2501909,
2502221,
2502251,
2502323,
2502341]
#units k
key2 = key1
#districts j
districts = []
for i in range(1, math.ceil(len(key1)/3) + 1 ):
    districts.append(i)
#data
M = 80000
T = 365*0.575
distance = create_tuple_dict_units("unit_distances.csv","unit_durations.csv")[0]
distance2 = {}
for pair in distance:
    if pair[0] in key1 and pair[1] in key1:
        distance2[pair] = distance[pair]
distance = distance2
# makes nonexistent dij = 200
for unit1 in key1:
    for unit2 in key1:
        try:
            distance2[(unit1, unit2)]
        except KeyError:
            distance2[(unit1, unit2)] = 200
dictkeys = list(distance.keys())
list1 = []
list2 = []
for i in dictkeys:
    list1.append(i[0])
    list2.append(i[1])
list3 = list1 + list2
list1 = set(list1)
list2 = set(list2)
list3 = set(list3)
#decision vairables
x = model.addVars(list3, districts,  vtype = GRB.BINARY, name = "x" )
#Auxilary variables
y = model.addVars(districts,  vtype = GRB.CONTINUOUS, name = "y" )
z = model.addVars(list3, list3,  vtype = GRB.CONTINUOUS, name = "z" )
#Constraints
model.addConstrs( quicksum(x[i,j] for i in key1) <= 3 for j in districts )
model.addConstrs( quicksum(x[i,j] for j in districts) == 1 for i in key1 )
#model.addConstrs( z[i,k] == 0 for i in key1 for k in key2 if distance[(i,k)] >= 60 if i<k )
model.addConstrs( z[i,k] >= x[i,j] + x[k,j] - 1 for i in key1 for k in key2 for j in districts if i < k )
model.addConstrs( y[j] >= x[i,j] for i in key1 for j in districts)
#symmetry breaking
while_index = 1
while while_index < len(districts):
    model.addConstr( y[while_index] >=  y[while_index+1] )
    while_index+=1
#Objective
obj = M * quicksum(y[j] for j in districts) + T * quicksum(z[i,k] * distance[(i,k)] for i in key1 for k in key2 if i<k )
model.setObjective(obj, GRB.MINIMIZE)
model.optimize()
##################################
#print statement
if model.status == GRB.Status.OPTIMAL:
    print('\nOptimal solution found in {}s'.format(round(model.Runtime,2)))
    print('\nThe total cost is {}'.format(model.objVal))
    print('\nThe optimal solution is:')
    x_sol = model.getAttr('x', x) # get the optimal solution
    list_of_tups = []
    for v in model.getVars():
        if v.X != 0 and v.Varname[0] == "z":
            unit1 = int(v.Varname[2:9])
            unit2 = int(v.Varname[10:-1])
            list_of_tups.append((unit1, unit2))
    district_solution = (format_district_solution(list_of_tups))
    pprint(district_solution)
            # print("%s %f" % (v.Varname, v.X))
else:
    print('No solution! Optimization status is {}'.format(model.status))
    print('See http://www.gurobi.com/documentation/8.0/refman/optimization_status_codes.html for status code.')
model.write('inital_model.lp')
##### Create Tableau Output ####################################################################
print("\n\n############################################# Creating Tableau Output #############################################")
my_dict = {}
#Make dict of dicts
for unit in key1:
    my_dict[unit] = {"latitude": None,
    "longitude": None,
    "district": None,
    "division": None,
    "area": None}
#Write district assignments
for line in open("district_assignments.csv", "r"):
    line = line.split(',')
    unit = int(line[0].strip())
    district = int(line[1].strip())
    my_dict[unit]['district'] = district+182

count = 0
for line in open("Data.txt", "r"):
    if count == 0:
        count += 1
        continue
    else:
        mylist = line.split("\t")
        unit = int(mylist[0])
        if unit not in key1:
            continue
        else:
            lat = mylist[31].strip()
            lon = mylist[32].strip()
            try:
                lat = float(lat)
                lon = float(lon)
            except ValueError:
                lat = None
                lon = None
            my_dict[unit]["latitude"] = lat
            my_dict[unit]["longitude"] = lon
            count += 1
#pprint(my_dict)
df = pd.DataFrame(my_dict).transpose()
df = df[['latitude', 'longitude', 'district']]
df.index.name = "unit number"
df = df.sort_values(by=["district"])
df.to_csv(path_or_buf = "tableau_output_.csv")