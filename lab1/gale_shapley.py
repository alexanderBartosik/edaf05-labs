import sys

'''
Gale-Shapley algorithm solving the stable matching problem
a_pref - proposing entities preferences list ("students"), 
b_pref - receiving entities preferences list ("companies")
'''
def gale_shapley(a_pref, b_pref):
    b_matches = {}
    a_matches = {}
    a_free = list(a_pref.keys())
    # While there are free a's
    while a_free:
        a = a_free.pop(0)
        b = a_pref[a].pop(0)
        # If b is free, match a and b
        if b in b_matches:
            a2 = b_matches[b]
            # If a prefers b over a2, match a and b and free a2
            if b_pref[b].index(a) < b_pref[b].index(a2):
                a_matches[a] = b
                a_free.append(a2)
            else:
                a_free.append(a)
        else:
            b_matches[b] = a
            a_matches[a] = b
    return a_matches


def line_to_dict(line, c_prefs, s_prefs):
    parts = line.strip().split()
    ints = [int(x) for x in parts]
    key = ints[0]
    values = ints[1:]

    if not key in c_prefs: #första förekomsten är b
        c_prefs[key] = values
    else: #andra förekomsten är a
        s_prefs[key] = values


def parse():
    c_prefs = {}
    s_prefs = {}
    N = int(sys.stdin.readline())

    for line in sys.stdin:
        line_to_dict(line, c_prefs, s_prefs)

    #TODO: c_prefs pref to index sort

    return c_prefs, s_prefs, N


#Ska användas för att sortera b prefs enligt hint på slide 26 F01
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
    result = gale_shapley(s_prefs, c_prefs)
    output(result)


if __name__ == "__main__":
    main()