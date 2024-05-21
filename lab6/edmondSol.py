import sys
import time
from collections import deque

def parse():
    # Extract the first line of the input file [int] (4 entries in first line)
    N, M, C, P = map(int, sys.stdin.readline().strip().split())

    # Extract the rest of the lines
    all_lines_of_ints = [list(map(int, line.strip().split())) for line in sys.stdin]
    
    # Extract paths/edges [tuple] (start_idx, end_idx, max_flow)
    paths = [(line[0], line[1], line[2]) for line in all_lines_of_ints[:M]]
    
    # Extract delete_idx [list] (order of paths idx to delete)
    delete_idx = [line[0] for line in all_lines_of_ints[M:]]

    return N, M, C, P, paths, delete_idx

# Breadth-first search
def bfs(capacity, source, sink, parent):
    # Init visited list
    visited = [False] * len(capacity)
    # Init queue with source node
    queue = deque([source])
    # Mark source node as visited
    visited[source] = True
    
    # While the queue is not empty
    while queue:
        # Pop the first node in the queue
        u = queue.popleft()

        # Check all the nodes connected to u
        for v, cap in enumerate(capacity[u]):
            # If the node is not visited and there is capacity
            if not visited[v] and cap > 0:
                # Add the node to the queue
                queue.append(v)
                visited[v] = True
                # Set the parent of the node
                parent[v] = u
                # If the sink is reached
                if v == sink:
                    return True
    return False

# Edmonds-Karp algorithm
def edmonds_karp(N, source, sink, capacity):
    # Init parent list
    parent = [-1] * N
    max_flow = 0

    # While a path from source to sink has not been found
    while bfs(capacity, source, sink, parent):
        path_flow = float('Inf')
        s = sink

        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow

def network_flow_deletion(N, C, paths, delete_idx):
    # node index for source and sink
    source = 0
    sink = N - 1

    # Square matrix size N to store the capacity of the edges (undirected graph)
    capacity = [[0] * N for _ in range(N)]
    for u, v, c in paths:
        capacity[u][v] += c
        capacity[v][u] += c

    # Calculate the initial max flow
    initial_max_flow = edmonds_karp(N, source, sink, [row[:] for row in capacity])
    if initial_max_flow < C:
        return 0, initial_max_flow

    # Init Binary search
    low, high = 0, len(delete_idx)
    last_valid_max_flow = initial_max_flow
    last_deletions = 0

    # Binary search for the minimum number of deletions
    while low <= high:
        mid = (low + high) // 2
        
        # Copy the capacity matrix to avoid modifying the original
        temp_capacity = [row[:] for row in capacity]
        # Delete the first mid paths
        for idx in delete_idx[:mid]:
            u, v, c = paths[idx]
            temp_capacity[u][v] -= c
            temp_capacity[v][u] -= c

        # Calculate the max flow after deleting the first mid paths
        current_max_flow = edmonds_karp(N, source, sink, temp_capacity)

        # Update the last valid max flow and deletions
        if current_max_flow >= C:
            last_valid_max_flow = current_max_flow
            last_deletions = mid
            low = mid + 1
        else:
            high = mid - 1

    return last_deletions, last_valid_max_flow

def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')
    #print(f"Runtime written to file: {runtime}")

def main():
    N, _, C, _, paths, delete_idx = parse()
    
    start = time.time()
    deletions, final_flow = network_flow_deletion(N, C, paths, delete_idx)
    stop = time.time()

    write_to_output_file(start, stop)

    print(deletions, final_flow)
    
if __name__ == "__main__": 
    main()
