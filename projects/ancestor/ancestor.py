from collections import deque

class Graph:

    def __init__(self):
        self.vertices = {}

    def __repr__(self):
        return str(self.vertices)

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id] if vertex_id in self.vertices else set()

    def dft_ancestor(self, starting_vertex):
        visited = set()
        stack = deque()
        stack.append([starting_vertex, 0])
        ancestor = [-1, -1]
        while len(stack) > 0:
            currNode = stack.pop()
            if currNode[0] not in visited:
                visited.add(currNode[0])
                
                if len(self.get_neighbors(currNode[0])) == 0:
                    if(currNode[1] > ancestor[1]):
                        ancestor = currNode
                    elif(currNode[1] == ancestor[1] and currNode[0] < ancestor[0]):
                        ancestor = currNode
                else:
                    for neighbor in self.get_neighbors(currNode[0]):
                        stack.append([neighbor, currNode[1] + 1])

        if ancestor[0] == starting_vertex:
            return -1
            
        return ancestor[0]
        

def earliest_ancestor(ancestors, starting_node):
    graph = Graph()
    #Add Vertices and Edges
    for a in ancestors:
        p,c = a[0], a[1]
        graph.add_vertex(p)
        graph.add_vertex(c)
        graph.add_edge(c, p) #We want the edges to go "up", back to the ancestor


    return graph.dft_ancestor(starting_node)

