from collections import deque



# Breadth-first search
def bfs(G, s, t):
    q = deque([s])
    visited = set(s)
    visited.add(s) # Mark the start node as visited
    queue = deque([s])
    while queue:
        v = queue.popleft()
        for w in G[v]:
            if w not in visited:
                visited.add(w)
                queue.append(w)
                if w == t:
                    return True
    return False


def parseGraph():
    G = {}
    while True:
        try:
            line = input().split()
            if len(line) == 1:
                break
            if line[0] not in G:
                G[line[0]] = []
            if line[1] not in G:
                G[line[1]] = []
            G[line[0]].append(line[1])
            G[line[1]].append(line[0])
        except EOFError:
            break
    return G

G = parseGraph()
bfs(G, 'start', 'to')
