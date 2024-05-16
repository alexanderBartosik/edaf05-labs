import sys
import time
from collections import deque

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
    M = int(first_line[1]) # num edges
    C = int(first_line[2]) # num students
    P = int(first_line[3]) # num paths

    # Extract the rest of the lines
    all_lines_of_ints = []
    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        all_lines_of_ints.append(line_of_ints)
    
    # Extract paths/edges (start_idx, end_idx, max_flow)
    paths = [(all_lines_of_ints[i][0], all_lines_of_ints[i][1], all_lines_of_ints[i][2]) for i in range(M)]
    # Extract delete_idx (order of paths idx to delete)
    delete_idx = [line[0] for line in all_lines_of_ints[M:]]

    return N, M, C, P, paths, delete_idx

def bfs(capacity, source, sink, parent):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()

        for v, cap in enumerate(capacity[u]):
            if not visited[v] and cap > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False

def edmonds_karp(N, source, sink, capacity):
    parent = [-1] * N
    max_flow = 0

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
    source = 0
    sink = N - 1

    capacity = [[0] * N for _ in range(N)]
    for u, v, c in paths:
        capacity[u][v] += c
        capacity[v][u] += c

    initial_max_flow = edmonds_karp(N, source, sink, [row[:] for row in capacity])
    if initial_max_flow < C:
        return 0, initial_max_flow

    deletions = 0
    for idx in delete_idx:
        u, v, c = paths[idx]
        capacity[u][v] -= c
        capacity[v][u] -= c

        if edmonds_karp(N, source, sink, [row[:] for row in capacity]) >= C:
            deletions += 1
        else:
            capacity[u][v] += c
            capacity[v][u] += c
            break

    final_max_flow = edmonds_karp(N, source, sink, [row[:] for row in capacity])
    return deletions, final_max_flow

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
