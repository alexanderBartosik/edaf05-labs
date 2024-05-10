import sys
import time
from collections import deque, defaultdict
from copy import deepcopy

class MaxFlow:
    def __init__(self, N):
        self.size = N
        self.graph = defaultdict(lambda: defaultdict(int))
    
    def add_edge(self, u, v, capacity):
        self.graph[u][v] += capacity
        self.graph[v][u] += 0
    
    def remove_edge(self, u, v):
        if v in self.graph[u]:
            del self.graph[u][v]
        if u in self.graph[v]:
            del self.graph[v][u]
    
    # Breadth-first search
    def bfs(self, source, sink, parent):
        visited = [False] * self.size
        queue = deque([source])
        visited[source] = True
        
        while queue:
            current = queue.popleft()
            
            for neighbor, capacity in self.graph[current].items():
                if not visited[neighbor] and capacity > 0:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    parent[neighbor] = current
                    if neighbor == sink:
                        return True
        return False
    
    # Edmonds-Karp algorithm
    def edmonds_karp(self, source, sink):
        parent = [-1] * self.size
        max_flow = 0
        
        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            s = sink
            
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = u
            
            max_flow += path_flow
        
        return max_flow

def network_flow_deletion(N, C, paths, delete_idx):
    max_flow = MaxFlow(N)
    for u, v, capacity in paths:
        max_flow.add_edge(u, v, capacity)
        max_flow.add_edge(v, u, capacity)
    
    source, sink = paths[0][0], paths[-1][1]
    initial_max_flow = max_flow.edmonds_karp(source, sink)
    assert initial_max_flow >= C, "Initial flow is guaranteed to be at least C."

    deletions = 0
    for index in delete_idx:
        u, v, _ = paths[index]
        max_flow.remove_edge(u, v)
        max_flow.remove_edge(v, u)
        
        current_max_flow = max_flow.edmonds_karp(source, sink)
        if current_max_flow >= C:
            deletions += 1
        else:
            max_flow.add_edge(u, v, paths[index][2])
            max_flow.add_edge(v, u, paths[index][2])
    
    final_max_flow = max_flow.edmonds_karp(source, sink)
    return deletions, final_max_flow


# Extract the input files of lab 6
def parse():
    
    # Extract the first line of the input file (4 entries in first line)
    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0]) # num nodes
    M = int(first_line[1]) # num edges
    C = int(first_line[2]) # num students
    P = int(first_line[3]) # num paths

    # Extact the rest of the lines
    all_lines_of_ints = []
    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        all_lines_of_ints.append(line_of_ints)
    
    # Extract paths/edges (start_idx, end_idx, weight)
    paths = [(all_lines_of_ints[i][0], all_lines_of_ints[i][1], all_lines_of_ints[i][2]) for i in range(P)]
    # Extract delete_idx (order of paths idx to delete)
    delete_idx = [line[0] for line in all_lines_of_ints[M:]]

    return N, M, C, P, paths, delete_idx

def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')


def main():
    N, _, C, _, paths, delete_idx = parse()
    
    start = time.time()
    deletions, final_flow = network_flow_deletion(N, C, paths, delete_idx)
    stop = time.time()

    write_to_output_file(start, stop)

    #final output
    print(deletions, final_flow)
    
if __name__ == "__main__": 
    main()