import sys
import time
from collections import deque

'''
Gale-Shapley algorithm for the stable marriage problem.
c_prefs: dictionary with company preferences
s_prefs: dictionary with student preferences
'''
def gs(c_prefs, s_prefs):

    # Add each student to a list p
    p = deque(s_prefs.keys())
    matches = {}
    idx = {student: 0 for student in s_prefs}

    while p:
        #take the first student from p
        s = p.popleft()
        #find the next company student prefers most and has not applied to
        clist = s_prefs[s]
        c = clist[idx[s]]
        idx[s] += 1

        if c not in matches: 
            #c has no student, match it with s
            matches[c] = s
        else:
            #if c already has a student, check pref
            current_student = matches[c]
            #check if s in the c prefs and compare
            if s in c_prefs[c] and (c_prefs[c][s-1] < c_prefs[c][current_student-1]):
                #if c prefers s over its current student
                matches[c] = s
                #add old (curr) s back to p
                if current_student not in p:
                    p.append(current_student)
            elif current_student not in p:
                #if s rejected, add back to p
                p.append(s)

    return matches        

def parse():
    c_prefs = {}
    s_prefs = {}
    first_line = sys.stdin.readline()
    N = int(first_line)

    ints = []

    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        ints.extend(line_of_ints)

    for i in range(len(ints)):
        j = i%(N+1)
        
        if j == 0:
            key = ints[i]
            preferences = ints[i+1:i+N+1]
            if not key in c_prefs:
                c_prefs[key] = pref_to_index_for_one_key(preferences)
            elif not key in s_prefs:
                s_prefs[key] = preferences

    return c_prefs, s_prefs, N

#Ska användas för att sortera company prefs enligt hint på slide 26 F01
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
    c_prefs, s_prefs, N = parse()
    start = time.time()
    result = gs(c_prefs, s_prefs)
    stop = time.time()
    
    runtime = stop - start
    with open('runtime.txt', 'a') as file:
        file.write("N: " + str(N) + ", time: " + str(runtime) + '\n')

    output(result)

if __name__ == "__main__":
    main()