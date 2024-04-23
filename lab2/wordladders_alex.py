import sys
from collections import deque


def parse():
    wordlist = []
    queries = []

    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0])
    Q = int(first_line[1])

    for _ in range(N):
        wordlist.append(sys.stdin.readline().strip())
    
    for _ in range(Q):
        line = sys.stdin.readline().strip().split()
        queries.append((line[0],line[1]))

    return wordlist, queries



def create_adjacency_list(words):
    adjacency_list = {word: [] for word in words}
    
    def get_letter_count(word, start):
        count = {}
        for letter in word[start:]: #slice from start to end
            if letter in count:
                count[letter] += 1
            else:
                count[letter] = 1
        return count

    last_four_counts = {word: get_letter_count(word,1) for word in words}
    all_counts = {word: get_letter_count(word,0) for word in words}
    

    for u in words:
        for v in words:
            if u != v:
                # Get letter counts for both words
                u_count = last_four_counts[u]
                v_count = all_counts[v]
                # Check if all letters in u's last four are in v's last four in at least the same number
                if all(v_count.get(letter, 0) >= count for letter, count in u_count.items()):
                    adjacency_list[u].append(v)

    return adjacency_list


from collections import deque

def bfs(G, s, t):
    #queue with the start node and a step count of 0
    q = deque([(s, 0)])
    visited = set()
    visited.add(s)    

    while q:
        v, steps = q.popleft() #first element from the queue with the current step count

        if v == t: 
            return steps

        #go through each neighbor of the current node
        for w in G[v]:
            if w not in visited: #neighbor has not been visited yet
                visited.add(w)
                q.append((w, steps + 1)) #add to queue with, increment step count
    
    #target not found
    return -1

def process_queries(queries, graph):
    for query in queries:
        steps = bfs(graph, query[0],query[1])

        if steps == -1:
            print("Impossible")
        else:
            print(steps)

    return queries

def main():
    #print("===============START===============\n")
    wordlist, queries = parse()
    #print(wordlist, "\n", queries,"\n")

    graph = create_adjacency_list(wordlist)
    #print(graph)

    process_queries(queries, graph)

if __name__ == "__main__":
    main()