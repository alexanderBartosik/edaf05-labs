import sys
import time

# Lab 3: Making Friends - Minimum Spanning Tree (MST)
# Authors: Eliot Montesino Petrén, Alexander Bartosik

# Parses the content of lab 3 input files
def parse():
    
    # Extract the first line of the input file (N: num vertices, M: num edges)
    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0])
    M = int(first_line[1])

    # Extract the rest of the lines (u: start_idx, v: stop_idx, w: weight)
    all_lines_of_ints = []
    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        all_lines_of_ints.append(line_of_ints)
    u = [line[0] for line in all_lines_of_ints]
    v = [line[1] for line in all_lines_of_ints]
    w = [line[2] for line in all_lines_of_ints]

    return N, M, u, v, w

# Kruskals algorithm for finding the minimum spanning tree (MST) of a graph
# Returns the MST as a list of edges
def kruskal(num_nodes, num_edges, start_index, stop_index, weight):
    # Sort the edges by weight
    edges = sorted(zip(weight, start_index, stop_index))

    # Create a dictionary to store the parent of each node
    parent = {i: i for i in range(1, num_nodes + 1)}

    # Create a dictionary to store the rank of each node
    rank = {i: 0 for i in range(1, num_nodes + 1)}

    # Create a list to store the edges in the minimum spanning tree
    mst = []

    # Define a function to find the parent of a node
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    # Define a function to union two sets
    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]:
                    rank[root2] += 1

    # Iterate over the edges
    for w, u, v in edges:
        # If the nodes are not in the same set, add the edge to the minimum spanning tree
        if find(u) != find(v):
            mst.append((u, v, w))
            union(u, v)

    return mst

def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')

def main():
    N, M, u, v, w = parse()

    start = time.time()
    mst = kruskal(N, M, u, v, w)
    stop = time.time()
    
    write_to_output_file(start, stop)
    
    # Print final result
    total_weight = sum([w for u, v, w in mst])
    print(total_weight)


if __name__ == '__main__':
    main()