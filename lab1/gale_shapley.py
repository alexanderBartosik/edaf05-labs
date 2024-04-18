import sys
import time

def gs(c_prefs, s_prefs):

    p = list(s_prefs.keys())
    matches = {}
    applied = {student: [] for student in s_prefs}
    
    while p:
        # Take the first student from p
        s = p.pop(0)
        # Find the next preferred company that hasn't been applied to yet
        for c in s_prefs[s]:
            if c not in applied[s]:
                applied[s].append(c)
                break
        else:
            # If all companies have been applied to, skip further processing
            continue

        if c not in matches: #AAAAAAAAAAAAA
            # If the company has no student, match it with s
            matches[c] = s

        else:
            # If the company already has a student, check the company's preference
            current_student = matches[c]
            # Check if s is in the company's preference list and compare preferences
            if s in c_prefs[c] and (c_prefs[c].index(s) < c_prefs[c].index(current_student)):
                # If the company prefers s over its current student
                matches[c] = s
                # Add the displaced student back to p
                if current_student not in p:
                    p.append(current_student)
            elif current_student not in p:
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
        line_of_ints = [int(x) for x in line.strip().split()]
        ints.extend(line_of_ints)

    for i in range(len(ints)):
        j = i%(N+1)
        
        if j == 0:
            key = ints[i]
            preferences = ints[i+1:i+N+1]
            if not key in c_prefs:
                c_prefs[key] = preferences
            elif not key in s_prefs:
                s_prefs[key] = preferences
            
    return c_prefs, s_prefs, N


#Ska användas för att sortera company prefs enligt hint på slide 26 F01
#funkar bara utan repetitioner och om samtliga tal från min till max förekommer
def pref_to_index(prefs): 
    
    index_based_list = [0] * len(prefs)
    for i, pref in enumerate(prefs):
        index_based_list[pref - 1] = i + 1

    return index_based_list

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