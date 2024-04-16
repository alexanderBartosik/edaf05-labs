import sys

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

        if c not in matches:
            # If the company has no student, match it with s
            matches[c] = s

        elif c_prefs[c].index(s) < c_prefs[c].index(matches[c]):
            # If the company prefers s over its current student
            sc = matches[c]
            matches[c] = s
            # Add the displaced student back to p
            if sc not in p:
                p.append(sc)
        else:
            # If the company prefers its current student over s
            # Add s back to p to try the next preferred company in the next round
            if s not in p:
                p.append(s)

    return matches


def line_to_dict(line, c_prefs, s_prefs):
    parts = line.strip().split()
    ints = [int(x) for x in parts]
    key = ints[0]
    values = ints[1:]

    if not key in c_prefs: #första förekomsten är company
        c_prefs[key] = values
    else: #andra förekomsten är student
        s_prefs[key] = values

def parse():
    c_prefs = {}
    s_prefs = {}
    N = int(sys.stdin.readline())

    for line in sys.stdin:
        line_to_dict(line, c_prefs, s_prefs)

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
    c_prefs, s_prefs, N = parse()
    #print(c_prefs)
    #print(s_prefs)
    #print(N)


    #prefs = pref_to_index([4,2,1,3])
    #print("PREFS", prefs)

    result = gs(c_prefs, s_prefs)
    output(result)


if __name__ == "__main__":
    main()
