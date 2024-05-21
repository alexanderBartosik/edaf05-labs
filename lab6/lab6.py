import sys
import time
from collections import deque, defaultdict

'''
Extract the input files of lab 6

returns: 
N, M, C, P  - ints
paths       - list of tuples (start_idx, end_idx, max_flow)
delete_idx  - list of ints order of paths idx to delete
'''
def parse():
    # Extract the first line of the input file (4 entries in first line)
    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0]) # num nodes
    E = int(first_line[1]) # num edges
    C = int(first_line[2]) # num students
    P = int(first_line[3]) # num paths

    # Extact the rest of the lines
    all_lines_of_ints = []
    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        all_lines_of_ints.append(line_of_ints)
    
    # Extract paths/edges (start_idx, end_idx, max_flow)
    paths = [(all_lines_of_ints[i][0], all_lines_of_ints[i][1], all_lines_of_ints[i][2]) for i in range(P)]
    # Extract delete_idx (order of paths idx to delete)
    delete_idx = [line[0] for line in all_lines_of_ints[E:]]

    return N, E, C, P, paths, delete_idx

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = defaultdict(list)
        self.capacity = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, cap):
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.capacity[u][v] += cap
        self.capacity[v][u] += cap

    def preflow_push_max_flow(self, source, sink):
        n = self.n
        capacity = self.capacity
        height = [0] * n
        excess = [0] * n
        flow = defaultdict(lambda: defaultdict(int))
        seen = [0] * n  # Keeps track of the next neighbor to consider

        def push(u, v):
            send = min(excess[u], capacity[u][v] - flow[u][v])
            flow[u][v] += send
            flow[v][u] -= send
            excess[u] -= send
            excess[v] += send

        def relabel(u):
            min_height = float('inf')
            for v in self.adj[u]:
                if capacity[u][v] - flow[u][v] > 0:
                    min_height = min(min_height, height[v])
            relabeled_height = min_height +1
            height[u] = relabeled_height
            if relabeled_height > 2*n - 1:
                print(f'relabeled height: {relabeled_height}, max: {2*n - 1}.')

        def discharge(u):
            while excess[u] > 0:
                if seen[u] < len(self.adj[u]):
                    v = self.adj[u][seen[u]]
                    if capacity[u][v] - flow[u][v] > 0 and height[u] > height[v]:
                        push(u, v)
                    else:
                        seen[u] += 1
                else:
                    relabel(u)
                    seen[u] = 0

        height[source] = n
        excess[source] = float('inf')
        for v in self.adj[source]:
            push(source, v)

        active = [i for i in range(n) if i != source and i != sink and excess[i] > 0]
        while active:
            u = active.pop(0)
            old_height = height[u]
            discharge(u)
            if height[u] > old_height:
                active.insert(0, u)

        return sum(flow[source][v] for v in self.adj[source])

def maximum_flow_after_deletions(N, C, E, P, paths, D):
    graph = Graph(N)
    for start_idx, end_idx, weight in paths:
        graph.add_edge(start_idx, end_idx, weight)
    
    # Calculate initial maximum flow
    initial_flow = graph.preflow_push_max_flow(0, N-1)
    
    if initial_flow < C:
        return 0, initial_flow
    
    paths_deleted = 0
    for path_idx in D:
        start_idx, end_idx, weight = paths[path_idx]
        graph.capacity[start_idx][end_idx] -= weight
        graph.capacity[end_idx][start_idx] -= weight
        
        # Recompute max flow after deletion
        current_flow = graph.preflow_push_max_flow(0, N-1)
        if current_flow < C:
            graph.capacity[start_idx][end_idx] += weight
            graph.capacity[end_idx][start_idx] += weight
            break
        paths_deleted += 1

    resulting_flow = graph.preflow_push_max_flow(0, N-1)
    return paths_deleted, resulting_flow


def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')


def main():
    N, E, C, P, paths, delete_idx = parse()
    
    start = time.time()
    deletions, final_flow = maximum_flow_after_deletions(N, C, E, P, paths, delete_idx)
    stop = time.time()

    write_to_output_file(start, stop)

    #final output
    print(deletions, final_flow)
    
if __name__ == "__main__": 
    main()