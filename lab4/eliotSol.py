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
    N, *points = [tuple(map(int, line.strip().split())) for line in sys.stdin]
    return N, points

'''
Divide and conquer algorithm that finds the closest pair of points in a set of points.

Time complexity: O(n log n) according to the Master Theorem

points - a list of tuples (x, y) representing the coordinates of the points
'''
def find_closest_pair(points):

    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) # euclidean norm 2 coordinates
    
    # closest_cross_pair is a helper function that finds the closest pair of points
    def closest_cross_pair(strip, delta):
        strip.sort(key=lambda point: point[1])  # Sort strip by y-coordinate
        min_dist = delta
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    '''
    closest_recursive is a recursive function that finds the closest pair of points
    in a set of points.
    Divide into two sets, find the closest pair in each set, and then find the closest pair
    '''
    def closest_recursive(points):
        # BOTTOM CASE: If there are only 3 or fewer points, calculate and return the closest pair
        if len(points) <= 3:
            return min(distance(points[i], points[j]) for i in range(len(points)) for j in range(i + 1, len(points)))

        # Divide the points into two sets (left/right)
        mid = len(points) // 2
        mid_point = points[mid]
        left = points[:mid]
        right = points[mid:]

        # Recursively find the closest pair of points in each set
        dl = closest_recursive(left)
        dr = closest_recursive(right)
        d = min(dl, dr) # Find the minimum distance between the two sets

        # Find the closest pair of points that are in different sets
        strip = [p for p in points if abs(p[0] - mid_point[0]) < d]
        return min(d, closest_cross_pair(strip, d))

    # Converting coordinates to point list and initiating the process
    points.sort(key=lambda point: point[0])  # Sort points by x-coordinate O(n log n)
    closest_distance = closest_recursive(points)
    return format(closest_distance, '.6f') # Return on desired format

def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')

def main():
    _, points = parse()

    start = time.time()
    closest_dist = find_closest_pair(points)
    stop = time.time()

    write_to_output_file(start, stop)

    print(closest_dist)

if __name__ == "__main__":
    main()