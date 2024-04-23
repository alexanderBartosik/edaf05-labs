import sys


def parse():
    wordlist = []
    queries = {}

    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0])
    Q = int(first_line[1])

    for _ in range(N):
        wordlist.append(sys.stdin.readline().strip())
    
    for _ in range(Q):
        line = sys.stdin.readline().strip().split()
        queries[line[0]] = line[1]

    return wordlist, queries


#hash table! array av noder som innehåller linked-list av noder den är kopplad till
#4 last letters in s exist in t, s->t
#doubles

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
    
    # Determine the directed edges
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


def bfs(adjacencylist, node_from, node_to):
    return 0


def main():
    print("===============MAIN===============\n")
    wordlist, queries = parse()
    print(wordlist, "\n", queries,"\n")

    graph = create_adjacency_list(wordlist)
    print(graph)

if __name__ == "__main__":
    main()