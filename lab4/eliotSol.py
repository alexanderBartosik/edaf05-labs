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
    # Read first line (N), then the rest and form list of tuples (x, y)
    N, *points = [tuple(map(int, line.strip().split())) for line in sys.stdin]
    return N, points

'''
Divide and conquer algorithm that finds the closest pair of points in a set of points.

Time complexity: T(n) = 2T(n/2) + O(n) => O(n log n) according to the Master Theorem

points - a list of tuples (x, y) representing the coordinates of all the points
'''
def find_closest_pair(points_x_sort, points_y_sort):

    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) # euclidean norm 2 coordinates
    
    # Closest pair of points in the strip
    def closest_cross_pair(strip_y_sort, delta):
        for i in range(len(strip_y_sort)):
            for j in range(i + 1, min(i + 7, len(strip_y_sort))):
                dist = distance(strip_y_sort[i], strip_y_sort[j])
                if dist < delta:
                    delta = dist
        return delta

    '''
    closest_recursive is a recursive function that finds the closest pair of points
    in a set of points.
    Divide into two sets, find the closest pair in each set, and then find the closest pair
    Time complexity: T(n) = 2T(n/2) + O(n) => O(n log n) according to the Master Theorem
    '''
    def closest_recursive(points_x_sort, points_y_sort):
        # BASE CASE: If there are only 3 or fewer points, calculate and return the closest pair
        n = len(points_x_sort)
        if n <= 3:
            return min(distance(points_x_sort[i], points_x_sort[j]) for i in range(len(points_x_sort)) for j in range(i + 1, n))

        # Divide the points into two sets (left/right) and pick out the midpoint
        mid = n // 2
        mid_point = points_x_sort[mid]
        midpoint_x = mid_point[0]   # x-coord of the midpoint
        left_x  = points_x_sort[:mid]
        right_x = points_x_sort[mid:]

        # Pick out the points that are in the left and right set from the y-sorted list. 
        # If the x-coordinates are equal, sort by y-coordinate
        left_y  = list(filter(lambda point: point <= mid_point, points_y_sort))
        right_y = list(filter(lambda point: point > mid_point, points_y_sort))

        # Recursively find the closest pair of points in each set
        dl = closest_recursive(left_x, left_y)
        dr = closest_recursive(right_x, right_y)
        d = min(dl, dr) # Find the minimum distance between the two sets

        # Find the closest pair of points in different left/right sets filtered by distance d
        # The strip is sorted by y-coord
        strip_y_sort = [p for p in points_y_sort if abs(p[0] - midpoint_x) < d]
        return min(d, closest_cross_pair(strip_y_sort, d))

    # Converting coordinates to point list and initiating the process
    closest_distance = closest_recursive(points_x_sort, points_y_sort)
    return format(closest_distance, '.6f') # Return on desired format

def write_to_output_file(start, stop):
    runtime = stop - start
    with open('time.txt', 'a') as file:
        file.write("Runtime: " + str(runtime) + '\n')


'''
Overall time complexity is init sort and recursive divid and conquer: 
O(n log n) + O(n log n) = O(n log n)
'''
def main():
    _, points = parse()

    '''
    Sort points by x-and y-coordinate O(n log n) + O(n log n) = O(n log n)
    '''
    points_x_sort = sorted(points)
    points_y_sort = sorted(points, key=lambda point: point[1])

    start = time.time()
    closest_dist = find_closest_pair(points_x_sort, points_y_sort)
    stop = time.time()

    write_to_output_file(start, stop)

    print(closest_dist)

if __name__ == "__main__":
    main()