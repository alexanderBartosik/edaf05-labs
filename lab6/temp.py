
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
