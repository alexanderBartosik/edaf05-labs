import sys


def gs(student_prefs, company_prefs):
    return 0

def parse(line):
    print(line," yeehaw\n")


def main():
    #parsea fil, dela upp i student och company prefs (dictionaries {s:[c,...],s...}, {c:[s,...],c...} ??)
    student_dict = {}
    company_dict = {}
    
    for line in sys.stdin:
        parse(line)

    result = gs(student_dict, company_dict)

    print(result)
