import sys
import time
import math

'''
In lab 4 there is a water gun battle of N players and the coordinates (x,y)
for every player is given in the input file. The task is to find distances between
them with optimal time complexity. The naive approach is O(n^2) but the optimal
approach is O(n log n) using divide and conquer algorithm that involves recursive
methods and sorting. 
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
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) # euclidean norm 2 coordinates
    
    # closest_cross_pair is a helper function that finds the closest pair of points
    def closest_cross_pair(points, strip, delta):
        strip.sort(key=lambda point: point[1])  # Sort strip by y-coordinate
        min_dist = delta
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    # clostest_recursive is a recursive function that finds the closest pair of points    
    def closest_recursive(points):
        # If there are only 3 or fewer points, calculate and return the closest pair
        if len(points) <= 3:
            return min(distance(points[i], points[j]) for i in range(len(points)) for j in range(i + 1, len(points)))

        # Find the middle point
        mid = len(points) // 2
        mid_point = points[mid]
        left = points[:mid]
        right = points[mid:]

        # Subdivide the points into two sets and find the closest pair in each set
        dl = closest_recursive(left)
        dr = closest_recursive(right)
        d = min(dl, dr)

        # Find the closest pair of points that are in different sets
        strip = [p for p in points if abs(p[0] - mid_point[0]) < d]
        return min(d, closest_cross_pair(points, strip, d))

    # Converting coordinates to point list and initiating the process
    points = list(zip(x, y))
    points.sort(key=lambda point: point[0])  # Sort points by x-coordinate
    closest_distance = closest_recursive(points)
    return format(closest_distance, '.6f')

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