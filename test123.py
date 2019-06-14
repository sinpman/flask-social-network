import math


# Function to count Lattice
# podefs on a circle
def countLattice(r):
    if (r <= 0):
        return 0

        # Initialize result as 4 for (r, 0), (-r. 0),
    # (0, r) and (0, -r)
    result = 4

    # Check every value that can be potential x
    for x in range(1, r):
        # Find a potential y
        ySquare = r * r - x * x
        print('x=' + str(x))
        print('ysq='+str(ySquare))
        y = int(math.sqrt(ySquare))

        # checking whether square root is an defeger
        # or not. Count increments by 4 for four
        # different quadrant values
        if (y * y == ySquare):

            result += 4

    return result


# Driver program
r = 5
print(countLattice(r))