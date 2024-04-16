import sys

'''
Gale-Shapley algorithm solving the stable matching problem
a_pref - proposing entities preferences list ("students"), 
b_pref - receiving entities preferences list ("companies")
'''
def gale_shapley(b_pref, a_pref):
    b_matches = {}
    a_matches = {}

    # while there are unassigned b's
    while len(b_pref) > 0:
        b, preferences = b_pref.popitem()
        a = preferences.pop(0)

        # if a is not matched, match a and b
        if a not in a_matches:
            a_matches[a] = b
            b_matches[b] = a
        # if a is matched, check if a prefers b over current match
        else:
            current_b = a_matches[a]
            current_b_preferences = a_pref[current_b]
            # if a prefers b over current match, match a and b and unmatch current match
            if current_b_preferences.index(b) < current_b_preferences.index(current_b):
                b_pref[b] = preferences
            # if a does not prefer b over current match, add a back to b's preferences
            else:
                b_pref[current_b] = current_b_preferences[1:]
                b_matches[b] = a
                a_matches[a] = b

    # return the stable matches
    return b_matches
    


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


def main():
    #parsea fil, dela upp i a och b prefs (dictionaries {s:[c,...],s...}, {c:[s,...],c...})
    c_prefs, s_prefs, N = parse()
    print(c_prefs)
    print(s_prefs)
    print(N)

    prefs = pref_to_index([4,2,1,3])
    print("PREFS", prefs)

    result = gale_shapley(c_prefs, s_prefs)
    print("GS Result: ", result)

if __name__ == "__main__":
    main()