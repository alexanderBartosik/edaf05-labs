import sys
import time
from collections import deque

def gs(c_prefs, s_prefs):
    p = deque(s_prefs.keys())
    matches = {}
    idx = {student: 0 for student in s_prefs}
    
    while p:
        # Take the first student from p
        s = p.popleft()

        # Find the next preferred company that hasn't been applied to yet
        clist = s_prefs[s]
        c = clist[idx[s]]
            
        idx[s] = idx[s]+1 #increment for later

        if c not in matches: 
            # If the company has no student, match it with s
            matches[c] = s

        elif c_prefs[c][s-1] < c_prefs[c][matches[c]-1]: #PREF TO INDEX
                # If the company prefers s over its current student
                matches[c] = s
                p.append(matches[c])
        else:
                # If s is not in the preference list, or if the current student is preferred,
                # re-add the current student to p to reconsider their options
                p.append(s)
    return matches


def parse():
    c_prefs = {}
    s_prefs = {}
    first_line = sys.stdin.readline()
    N = int(first_line)

    ints = []

    for line in sys.stdin:
        parts = line.strip().split()
        l_int = [int(x) for x in parts]
        ints.extend(l_int)

    for i in range(0,len(ints),N+1):
        key = ints[i]
        values = ints[i+1:i+N+1]

        if not key in c_prefs: #första förekomsten är company
            c_prefs[key] = values
        elif not key in s_prefs: #andra, student
            s_prefs[key] = values
        else: #tredje förekomsten ska inte ske, nåt e fel
            #throwa nåt?
            continue 

    #TODO: c_prefs pref to index sort

    return c_prefs, s_prefs, N


#Ska användas för att sortera company prefs enligt hint på slide 26 F01
#funkar bara utan repetitioner och om samtliga tal från min till max förekommer
def pref_to_index_for_one_key(pref_list): 
    pref_list_copy = pref_list.copy()
    for i in range(len(pref_list)):
        pref_list[pref_list_copy[i]-1] = i + 1
    return pref_list


#resultat från gs-algoritmen, dictionary med företag (nyckel) - studentpar.
def output(r_dic):
    r_sorted = dict(sorted(r_dic.items()))
    for c in r_sorted:
        print(r_sorted[c])



def main():
    #parsea fil, dela upp i student och company prefs (dictionaries {s:[c,...],s...}, {c:[s,...],c...})

    startParse = time.time()
    c_prefs, s_prefs, N = parse()
    endParse = time.time()
    parsetime = endParse - startParse

    #print("parsing took: ", end-start)

    #prefs = pref_to_index([4,2,1,3])
    #print("PREFS", prefs)

    startGS = time.time()
    result = gs(c_prefs, s_prefs)
    endGS = time.time()
    algotime = endGS - startGS

    kvot = algotime /(N*N)

    with open('times.txt','a') as file:
        file.write(f'N: {N}, took: {parsetime} to parse and {algotime} to create matches. time/N^2: {kvot} \n')

    
    output(result)



if __name__ == "__main__":
    main()