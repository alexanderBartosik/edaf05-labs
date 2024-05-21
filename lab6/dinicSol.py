import sys
import time
from collections import deque, defaultdict

def parse():
    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0])
    M = int(first_line[1])
    C = int(first_line[2])
    P = int(first_line[3])

    all_lines_of_ints = []
    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        all_lines_of_ints.append(line_of_ints)
    
    paths = [(all_lines_of_ints[i][0], all_lines_of_ints[i][1], all_lines_of_ints[i][2]) for i in range(M)]
    delete_idx = [line[0] for line in all_lines_of_ints[M:]]

    return N, M, C, P, paths, delete_idx

class Dinic:
    def __init__(self, N):
        self.N = N
        self.adj = [[] for _ in range(N)]
        self.level = [-1] * N
        self.ptr = [0] * N

    def add_edge(self, u, v, cap):
        self.adj[u].append([v, len(self.adj[v]), cap])
        self.adj[v].append([u, len(self.adj[u])-1, 0])

    def reset_graph(self, paths):
        self.adj = [[] for _ in range(self.N)]
        for u, v, c in paths:
            self.add_edge(u, v, c)
            self.add_edge(v, u, c)

    def bfs(self, source, sink):
        self.level = [-1] * self.N
        queue = deque([source])
        self.level[source] = 0
        while queue:
            u = queue.popleft()
            for v, rev, cap in self.adj[u]:
                if self.level[v] == -1 and cap > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
                    if v == sink:
                        return True
        return False

    def dfs(self, u, sink, flow):
        if u == sink:
            return flow
        while self.ptr[u] < len(self.adj[u]):
            v, rev, cap = self.adj[u][self.ptr[u]]
            if self.level[v] == self.level[u] + 1 and cap > 0:
                pushed = self.dfs(v, sink, min(flow, cap))
                if pushed:
                    self.adj[u][self.ptr[u]][2] -= pushed
                    self.adj[v][rev][2] += pushed
                    return pushed
            self.ptr[u] += 1
        return 0

    def max_flow(self, source, sink):
        total_flow = 0
        while self.bfs(source, sink):
            self.ptr = [0] * self.N
            flow = self.dfs(source, sink, float('Inf'))
            while flow:
                total_flow += flow
                flow = self.dfs(source, sink, float('Inf'))
        return total_flow

def network_flow_deletion(N, C, paths, delete_idx):
    source = 0
    sink = N - 1

    dinic = Dinic(N)
    dinic.reset_graph(paths)

    initial_max_flow = dinic.max_flow(source, sink)
    if initial_max_flow < C:
        return 0, initial_max_flow

    left, right = 0, len(delete_idx)
    while left < right:
        mid = (left + right) // 2
        temp_paths = paths[:]
        for i in range(mid + 1):
            idx = delete_idx[i]
            u, v, c = paths[idx]
            temp_paths[idx] = (u, v, 0)
        
        dinic.reset_graph(temp_paths)
        if dinic.max_flow(source, sink) >= C:
            left = mid + 1
        else:
            right = mid

    deletions = left
    for i in range(left):
        idx = delete_idx[i]
        u, v, c = paths[idx]
        paths[idx] = (u, v, 0)

    dinic.reset_graph(paths)
    final_max_flow = dinic.max_flow(source, sink)
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

    print(deletions, final_flow)
    
if __name__ == "__main__": 
    main()
