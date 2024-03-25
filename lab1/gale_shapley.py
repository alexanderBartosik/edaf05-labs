import sys


def gs(student_prefs, company_prefs):
    return 0


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

    #TODO följa hinten och sortera company prefs! slide 26 F01

    return c_prefs, s_prefs, N


def pref_to_index(prefs): #funkar bara utan repetitioner och om samtliga tal från min till max förekommer
    index_based_list = [0] * len(prefs)
    for i, pref in enumerate(prefs):
        index_based_list[pref - 1] = i + 1

    return index_based_list




def main():
    #parsea fil, dela upp i student och company prefs (dictionaries {s:[c,...],s...}, {c:[s,...],c...})
    c_prefs, s_prefs, N = parse()
    print(c_prefs)
    print(s_prefs)
    print(N)


    prefs = pref_to_index([4,2,1,3])
    print("PREFS", prefs)

    result = gs(c_prefs, s_prefs)
    #print(result)


if __name__ == "__main__":
    main()
