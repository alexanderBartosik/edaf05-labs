import sys
import time
from collections import defaultdict, deque

def parse():
    # N - num nodes, M - num edges, C - num students, P - num paths
    N, M, C, P = map(int, sys.stdin.readline().strip().split())

    # Extract edges (start_idx, end_idx, max_flow)
    all_lines_of_ints = [list(map(int, line.strip().split())) for line in sys.stdin]
    paths = [(all_lines_of_ints[i][0], all_lines_of_ints[i][1], all_lines_of_ints[i][2]) for i in range(M)]
    
    # Extract delete_idx (order of paths idx to delete)
    delete_idx = [line[0] for line in all_lines_of_ints[M:]]

    return N, M, C, P, paths, delete_idx

def testParsed(N, M, C, P, paths, delete_idx):
    print('N, M, C, P: ', N, M, C, P)
    print('paths: ', paths)
    print('delete order: ', delete_idx)

class FlowNetwork:
    def __init__(self, n):
        self.n = n
        self.capacity = defaultdict(lambda: defaultdict(int)) # dict that creates a new dict if key not found
        self.flow = defaultdict(lambda: defaultdict(int))
        self.height = [0] * n
        self.excess = [0] * n
        self.adj = defaultdict(list)

    def add_edge(self, u, v, capacity):
        self.capacity[u][v] = capacity
        self.capacity[v][u] = capacity  # undirected graph
        self.adj[u].append(v)
        self.adj[v].append(u)

    def initialize_preflow(self, source):
        self.height[source] = self.n
        for v in self.adj[source]:
            self.flow[source][v] = self.capacity[source][v]
            self.flow[v][source] = -self.capacity[source][v]
            self.excess[v] = self.capacity[source][v]
            self.excess[source] -= self.capacity[source][v]

    def push(self, u, v):
        delta = min(self.excess[u], self.capacity[u][v] - self.flow[u][v])
        self.flow[u][v] += delta
        self.flow[v][u] -= delta
        self.excess[u] -= delta
        self.excess[v] += delta

    def relabel(self, u):
        min_height = float('inf')
        for v in self.adj[u]:
            if self.capacity[u][v] - self.flow[u][v] > 0:
                min_height = min(min_height, self.height[v])
        self.height[u] = min_height + 1

    def discharge(self, u):
        while self.excess[u] > 0:
            for v in self.adj[u]:
                if self.capacity[u][v] - self.flow[u][v] > 0 and self.height[u] > self.height[v]:
                    self.push(u, v)
                    if self.excess[u] == 0:
                        break
            else:
                self.relabel(u)

    def max_flow(self, source, sink):
        self.initialize_preflow(source)
        active = [i for i in range(self.n) if i != source and i != sink and self.excess[i] > 0]
        while active:
            u = active.pop(0)
            old_height = self.height[u]
            self.discharge(u)
            if self.height[u] > old_height:
                active.insert(0, u)
        return self.excess[sink]

def calcFinalResults(N, M, C, P, paths, delete_idx):
    source, sink = 0, N - 1
    flow_network = FlowNetwork(N)
    
    for u, v, cap in paths:
        flow_network.add_edge(u, v, cap)
    
    initial_max_flow = flow_network.max_flow(source, sink)
    
    deletions = 0
    for idx in delete_idx:
        u, v, _ = paths[idx]
        flow_network.capacity[u][v] = 0
        flow_network.capacity[v][u] = 0
        
        new_max_flow = flow_network.max_flow(source, sink)
        if new_max_flow >= C:
            deletions += 1
            initial_max_flow = new_max_flow
        else:
            break
    
    return deletions, initial_max_flow
def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')

def main():
    N, M, C, P, paths, delete_idx = parse()

    #testParsed(N, M, C, P, paths, delete_idx)

    start = time.time()
    deletions, final_flow = calcFinalResults(N, M, C, P, paths, delete_idx)
    stop = time.time()

    write_to_output_file(start, stop)

    print(deletions, final_flow)

if __name__ == "__main__":
    main()
