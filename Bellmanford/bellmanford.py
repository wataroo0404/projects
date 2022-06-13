import xlrd 
import pprint
from math import log
from collections import defaultdict

class Graph:

	def __init__(self, vertices):
		self.vertices = vertices
		self.graph = [] 

	def addEdge(self,u,v,w):
		self.graph.append([u,v,w])

	def printSol(self, dist):
		print("Vertex   Distance from Source")
		for i in range(self.vertices):
			# +1 is needed because of index start 0 
			print("%d \t\t %d" % (i+1, dist[i]))

	def BellmanFord(self, source):
		dist = [float("Inf")] * self.vertices
		dist[source] = 0
	
		for i in range(self.vertices - 1):
			path_list = []
			for u,v,w in self.graph:
				if dist[u] != float("Inf") and dist[u] + w < dist[v]:
					dist[v] = dist[u] + w 
					path_list.append(v+1)
					#print(path_list)
	
		for u,v,w in self.graph:
			if dist[u] != float("Inf") and dist[u] + w < dist[v]:
				print("Negative cycle detected")
				return 
		
		self.printSol(dist)
	
book = xlrd.open_workbook('distance.xlsx')
sheet = book.sheet_by_name('Table 1')
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
sheet2 = book.sheet_by_name('Table 2')
data2 = [[sheet2.cell_value(r, c) for c in range(sheet2.ncols)] for r in range(sheet2.nrows)]

for i in range(15):
   for j in range(15):
       if data[i][j] == '-':
           data[i][j] = 0
for i in range(15):
   for j in range(15):
       if data2[i][j] == '-':
           data2[i][j] = 0

pp = pprint.PrettyPrinter(indent=1)
#pp.pprint(data2)

print("algorithm run for table 1")
g = Graph(15)

for i in range(15):
	for j in range(15):
		if data[i][j] != 0:
			g.addEdge(i,j,data[i][j])

#input source vetrex into this function 
g.BellmanFord(0)

print()
print("algorithm run for table 2")
h = Graph(15)

for i in range(15):
	for j in range(15):
		if data2[i][j] != 0:
			h.addEdge(i,j,data2[i][j])

#input source vetrex into this function 
h.BellmanFord(13)
