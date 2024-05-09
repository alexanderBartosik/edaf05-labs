import sys
import time
import math

'''
In lab 4 there is a water gun battle of N players and the coordinates (x,y)
for every player is given in the input file. The task is to find distances between
them with optimal time complexity.
'''

# Parses the content of lab 4 input files
def parse():
    
    # Extract the first line of the input file (N: num players)
    first_line = sys.stdin.readline().strip().split()
    N = int(first_line[0]) # only 1 number in lab 4 input files

    # Extract the rest of the lines (x: x-coord, y: y-coord)
    all_lines_of_ints = []
    for line in sys.stdin:
        line_of_ints = [int(x) for x in line.strip().split()]
        all_lines_of_ints.append(line_of_ints)
    x = [line[0] for line in all_lines_of_ints]
    y = [line[1] for line in all_lines_of_ints]

    return N, x, y

'''
The algo function should return the answer to the problem
'''
def algo(x, y):

    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def closest_cross_pair(points, strip, delta):
        strip.sort(key=lambda point: point[1])  # Sort strip by y-coordinate
        min_dist = delta
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    def closest_recursive(points):
        if len(points) <= 3:
            return min(distance(points[i], points[j]) for i in range(len(points)) for j in range(i + 1, len(points)))

        mid = len(points) // 2
        mid_point = points[mid]
        left = points[:mid]
        right = points[mid:]

        dl = closest_recursive(left)
        dr = closest_recursive(right)
        d = min(dl, dr)

        strip = [p for p in points if abs(p[0] - mid_point[0]) < d]
        return min(d, closest_cross_pair(points, strip, d))

    # Converting coordinates to point list and initiating the process
    points = list(zip(x, y))
    points.sort(key=lambda point: point[0])  # Sort points by x-coordinate
    distance = closest_recursive(points)
    distance = format(distance, '.6f')
    return distance

def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')

def main():
    _, x, y = parse()

    start = time.time()
    answer = algo(x, y)
    stop = time.time()

    write_to_output_file(start, stop)

    print(answer)

if __name__ == "__main__":
    main()