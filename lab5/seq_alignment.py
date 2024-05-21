import sys

def parse():
    letters = sys.stdin.readline().strip().split()
    letter_count = len(letters)
    scores = []

    for _ in range(letter_count): 
        row = [int(letter) for letter in sys.stdin.readline().strip().split()]
        scores.append(row)

    nbr_queries = int(sys.stdin.readline().strip())
    queries = []

    for i in range(nbr_queries):
        query = sys.stdin.readline().strip().split()
        queries.append(query) 

    return letters, scores, queries


def needleman_wunsch(seq1, seq2, letters, score_matrix, gap_penalty=-4):
    # Create a dictionary to map each letter to its index in the score matrix
    letter_to_index = {letter: index for index, letter in enumerate(letters)}
    
    # Initialize the scoring matrix and the traceback matrix
    n, m = len(seq1), len(seq2)
    scores = [[0] * (m + 1) for _ in range(n + 1)]
    traceback = [[None] * (m + 1) for _ in range(n + 1)]

    #initialize the first row and column. (scores for aligning with gap in beginning)
    for i in range(1, n + 1):
        scores[i][0] = i * gap_penalty
        traceback[i][0] = 'UP'
    for j in range(1, m + 1):
        scores[0][j] = j * gap_penalty
        traceback[0][j] = 'LEFT'

    #fill scoring matrix and update traceback matrix
    #O(n * m), everything inside is O(1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            char1 = seq1[i - 1]
            char2 = seq2[j - 1]
            
            # Lookup the score for aligning char1 with char2
            if char1 in letter_to_index and char2 in letter_to_index:
                match_score = score_matrix[letter_to_index[char1]][letter_to_index[char2]]
            else:
                match_score = gap_penalty
            
            match = scores[i - 1][j - 1] + match_score #match = diag down ight
            delete = scores[i - 1][j] + gap_penalty #delete = down (append seq1 with *)
            insert = scores[i][j - 1] + gap_penalty #insert = right (append seq2 with *)
            
            # Choose the highest scoring option
            best_score = max(match, delete, insert)
            scores[i][j] = best_score
            
            if best_score == match:
                traceback[i][j] = 'DIAG'
            elif best_score == delete:
                traceback[i][j] = 'UP'
            else:
                traceback[i][j] = 'LEFT'
    
    # Trace back to build the alignment
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = n, m
    
    while i > 0 or j > 0: #worst case O(n+m)?
        if traceback[i][j] == 'DIAG':
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif traceback[i][j] == 'UP':
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append('*')
            i -= 1
        elif traceback[i][j] == 'LEFT':
            aligned_seq1.append('*')
            aligned_seq2.append(seq2[j - 1])
            j -= 1
    
    # Reverse the aligned sequences as we've traced them backwards
    aligned_seq1.reverse()
    aligned_seq2.reverse()
    
    return ''.join(aligned_seq1), ''.join(aligned_seq2)



def main():
    letters, scores, queries = parse()
    for q in queries:
        string1, string2 = needleman_wunsch(q[0], q[1],letters,scores)
        print(string1," ",string2)




if __name__ == "__main__":
    main()