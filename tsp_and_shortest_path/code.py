import math 
import pandas as pd, numpy as np 


df = pd.read_csv('data.csv')
points = df.reset_index(drop=True).values



def find_dist(node_i, node_j):
	#manhattan
	return abs(points[node_i][0] - points[node_j][0]) + abs(points[node_i][1] - points[node_j][1])
	#chebyshev
	#return max(abs(points[node_i][0] - points[node_j][0]) , abs(points[node_j][1] - points[node_j][1]))

def find_cost(cost_list):
	total = 0 
	for i in range(len(cost_list)-1):
		total += find_dist(cost_list[i], cost_list[i+1])
	return total


node = -1 
cost = math.inf 

for i in range(len(points)):
	if i == 0:
		continue
	new_cost = find_dist(0, i)
	if new_cost < cost:
		cost = new_cost
		node = i 

path = [0, node, 0]

print(str(path) + ", cost = " + str(find_cost(path)))

visited = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0]
visited[node] = 1

while 0 in visited:
	cost = math.inf
	arc_ind = -1 
	node = -1 
	for i in range(len(path)-1):
		for n in range(len(visited)):
			if visited[n] == 1:
				continue
			else:
				cost = find_dist(path[i],n) + find_dist(n, path[i+1]) - find_dist(path[i],path[i+1])
				if new_cost < cost:
					cost = new_cost
					arc_ind = i
					node = n 
	path.insert(arc_ind + 1, node)
	visited[node] = 1 
	print(str(path) + ", cost = " + str(find_cost(path)))




