import sys
import time
from collections import defaultdict, deque

def parse():
    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0])  # num nodes
    M = int(first_line[1])  # num edges
    C = int(first_line[2])  # num students
    P = int(first_line[3])  # num paths

    all_lines_of_ints = []
    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        all_lines_of_ints.append(line_of_ints)

    paths = [(all_lines_of_ints[i][0], all_lines_of_ints[i][1], all_lines_of_ints[i][2]) for i in range(M)]
    delete_idx = [line[0] for line in all_lines_of_ints[M:]]

    return N, M, C, P, paths, delete_idx

class PreflowPush:
    def __init__(self, N):
        self.N = N
        self.adj = [[] for _ in range(N)]
        self.capacity = defaultdict(lambda: defaultdict(int))
        self.flow = defaultdict(lambda: defaultdict(int))
        self.excess = [0] * N
        self.height = [0] * N
        self.source = 0
        self.sink = N - 1
        self.active_nodes = deque()

    def add_edge(self, u, v, cap):
        self.capacity[u][v] += cap
        self.adj[u].append(v)
        self.adj[v].append(u)

    def initialize_preflow(self):
        self.height = [0] * self.N
        self.excess = [0] * self.N
        self.flow = defaultdict(lambda: defaultdict(int))
        self.active_nodes.clear()
        self.height[self.source] = self.N
        for v in self.adj[self.source]:
            self.flow[self.source][v] = self.capacity[self.source][v]
            self.flow[v][self.source] = -self.capacity[self.source][v]
            self.excess[v] = self.capacity[self.source][v]
            self.capacity[self.source][v] = 0
            if v != self.sink:
                self.active_nodes.append(v)
        print("Initial preflow:", dict(self.flow))
        print("Initial excess:", self.excess)
        print("Initial heights:", self.height)

    def push(self, u, v):
        delta = min(self.excess[u], self.capacity[u][v])
        self.capacity[u][v] -= delta
        self.capacity[v][u] += delta
        self.flow[u][v] += delta
        self.flow[v][u] -= delta
        self.excess[u] -= delta
        self.excess[v] += delta
        if self.excess[v] > 0 and v != self.source and v != self.sink and v not in self.active_nodes:
            self.active_nodes.appendleft(v)

    def relabel(self, u):
        min_height = float('inf')
        for v in self.adj[u]:
            if self.capacity[u][v] > 0:
                min_height = min(min_height, self.height[v])
        if min_height < float('inf'):
            self.height[u] = min_height + 1

    def discharge(self, u):
        while self.excess[u] > 0:
            for v in self.adj[u]:
                if self.capacity[u][v] > 0 and self.height[u] == self.height[v] + 1:
                    self.push(u, v)
                    if self.excess[u] == 0:
                        break
            else:
                old_height = self.height[u]
                self.relabel(u)
                if self.height[u] == old_height:
                    break

    def max_flow(self):
        self.initialize_preflow()
        while self.active_nodes:
            u = self.active_nodes.popleft()
            self.discharge(u)
        return sum(self.flow[self.source][v] for v in self.adj[self.source])

def network_flow_deletion(N, C, paths, delete_idx):
    def rebuild_preflow_push(preflow_push):
        temp_preflow_push = PreflowPush(N)
        for i, (u_, v_, c_) in enumerate(paths):
            if preflow_push.capacity[u_][v_] > 0:
                temp_preflow_push.add_edge(u_, v_, preflow_push.capacity[u_][v_])
        return temp_preflow_push

    preflow_push = PreflowPush(N)
    for u, v, c in paths:
        preflow_push.add_edge(u, v, c)
    
    initial_max_flow = preflow_push.max_flow()
    print(f"Initial max flow: {initial_max_flow}")
    if initial_max_flow < C:
        return 0, initial_max_flow

    deletions = 0
    for idx in delete_idx:
        u, v, c = paths[idx]
        preflow_push.capacity[u][v] -= c
        print(f"Deleting edge {u}-{v} with capacity {c}")

        # Rebuild the PreflowPush instance with the updated capacities
        temp_preflow_push = rebuild_preflow_push(preflow_push)
        current_max_flow = temp_preflow_push.max_flow()

        if current_max_flow >= C:
            deletions += 1
            print(f"Edge {u}-{v} deleted, current max flow: {current_max_flow}")
        else:
            preflow_push.capacity[u][v] += c
            print(f"Restoring edge {u}-{v} with capacity {c}, current max flow: {current_max_flow}")
            break
    
    final_max_flow = preflow_push.max_flow()
    
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
