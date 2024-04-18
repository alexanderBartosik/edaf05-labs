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
            if s in c_prefs[c] and (c_prefs[c].index(s) < c_prefs[c].index(current_student)): #linjärsökning som kan undvikas med pref-to-index
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