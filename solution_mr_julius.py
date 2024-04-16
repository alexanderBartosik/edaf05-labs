import os
import sys 
import time

#processes in terms of lines, not used anymore
def process_input(input_data):
    lines = []
    for line in input_data.splitlines():
        lines.append(line)
    return lines

#processes in terms of individual items
def process_input2(input_data):
    lines = []
    lines.append(input_data[0])
    n = int(input_data[0]) + 1
    index = 1
    while index < len(input_data):
        lines.append(input_data[index:index+n])
        index += n
    return lines


#write to file, not used
def write_output(file, list):
    with open(file, 'w') as f:
        for item in list:
            f.write("%s\n" % item)

#print to console
def print_output(list):
    for item in list:
        print(item, flush=True)

#Generates the preference lists, two lists with the index corresponding 
def generate_pref_lists(n, input_list):
    companies_pref = [None] * (n)
    students_pref =  [None] * (n)
    for line in input_list[1:]:
        index = int(line[0]) - 1
        if companies_pref[index] is None:
            # print(index + 1)
            companies_pref[index] = create_inverted_list(line[1:])
        else:
            students_pref[index] = line[1:]

    return companies_pref, students_pref

#Creates an inverted list for companies
def create_inverted_list(list):
    inverted_list = [None] * len(list)
    for i in range(len(list)):
        temp = int(list[i]) - 1
        inverted_list[temp] = i + 1
    return inverted_list

def stable_matching(input_list):
    # num_stud_comp = len(input_list) // 2
    algo_start_time = time.time()
    n = int(input_list[0])
    companies_pref, students_pref = generate_pref_lists(n, input_list)
    #Algorithm
    students_free = list(range(n))
    companies_free = [-1] * n
    matches =[-1] * n
    while students_free:
        s = students_free.pop(0)
        c = int(students_pref[s].pop(0)) - 1
        if companies_free[c] == -1:
            companies_free[c] = s
            matches[c] = s+1
        elif companies_pref[c][s] < companies_pref[c][companies_free[c]]:
            students_free.append(companies_free[c])
            companies_free[c] = s
            matches[c] = s+1
        else:
            students_free.append(s)

    #Temp fix for index issue
    # for i in range(len(matches)):
    #     matches[i] += 1
    algo_end_time = time.time()
    algo_total_time = algo_end_time - algo_start_time
    # print("Algo time: " + str(algo_total_time))
    return matches

def main(output_file = None):
    # directory = '/Users/juliuse/School/LTH/edaf05/lab1/data/secret'
    # file_name = '0testsmall.in'
    # file_path = os.path.join(directory, file_name)

    dir = '/Users/juliuse/School/LTH/edaf05/lab1'
    output_name = 'output.in'
    output_path = os.path.join(dir, output_name)

    program_start_time = time.time()
    process_start_time = time.time()
    input_data = sys.stdin.read().strip()
    input_list = process_input2(input_data.split())
    process_end_time = time.time()
    process_total_time = process_end_time - process_start_time
    # print("Process Time: " + str(process_total_time))

    # write_output(output_path, stable_matching(input_list))
    print_output(stable_matching(input_list))
    program_end_time = time.time()
    program_total_time = program_end_time - program_start_time
    # print("Program Time: " + str(program_total_time))

if __name__ == "__main__":
    main()