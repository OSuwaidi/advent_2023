# بسم الله الرحمن الرحيم وبه نستعين

"""
Due to strong, probably-magical winds, the hailstones are all flying through the air in perfectly linear trajectories. You make a note of each hailstone's position and velocity (your puzzle input). For example:

19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
Each line of text corresponds to the position and velocity of a single hailstone. The positions indicate where the hailstones are right now (at time 0). The velocities are constant and indicate exactly how far each hailstone will move in one nanosecond.

Each line of text uses the format px py pz @ vx vy vz. For instance, the hailstone specified by 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y position 19, Z position 15, X velocity 1, Y velocity -5, and Z velocity -3. After one nanosecond, the hailstone would be at 21, 14, 12.

Perhaps you won't have to do anything. How likely are the hailstones to collide with each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward in time, how many of the hailstones' paths will intersect within a test area? (The hailstones themselves don't have to collide, just test for intersections between the paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at least 7 and at most 27; in your actual data, you'll need to check a much larger test area. Comparing all pairs of hailstones' future paths produces the following results:

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
So, in this example, 2 hailstones' future paths cross inside the boundaries of the test area.

However, you'll need to search a much larger test area if you want to see if any hailstones might collide. Look for intersections that happen with an X and Y position each at least 200000000000000 and at most 400000000000000. Disregard the Z axis entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections. How many of these intersections occur within the test area?
"""
from rich import print
from tqdm import trange
import sympy as sym


def clean_hailstones(hailstone_info: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    positions, velocities = hailstone_info.rstrip().split(" @ ")
    positions = tuple(map(int, positions.split(", ")))
    velocities = tuple(map(int, velocities.split(", ")))
    return positions, velocities

with open("day4.txt", "r") as txt_file:
    solutions_found = 0
    MIN_BOUND = 200000000000000
    MAX_BOUND = 400000000000000
    
    hailstones = txt_file.readlines()
    hailstones = tuple(map(clean_hailstones, hailstones))

    for i in trange(len(hailstones) - 1):
        positions_i, velocities_i = hailstones[i]
        xi_initial, yi_initial, _ = positions_i
        vxi, vyi, _ = velocities_i
        
        mi = vyi / vxi  # slope

        for j in range(i+1, len(hailstones)):
            ti, tj = sym.symbols("ti, tj")  # initialize the ith and jth hailstones' time variables

            positions_j, velocities_j = hailstones[j]
            xj_initial, yj_initial, _ = positions_j
            vxj, vyj, _ = velocities_j
            
            mj = vyj / vxj

            if mi == mj:  # same slope in 2D implies parallel or coinciding lines
                continue

            else:
                xi_future = xi_initial + vxi * ti
                yi_future = yi_initial + vyi * ti

                xj_future = xj_initial + vxj * tj
                yj_future = yj_initial + vyj * tj

                fx = xi_future - xj_future  # check where the hailstones' trajectories would intersect in the x-direction (xi_future - xj_future = 0 --> xi_future = xj_future)
                fy = yi_future - yj_future  # check where the hailstones' trajectories would intersect in the y-direction

                solution = sym.solve((fx, fy))  # solves the equations as if they were equalling 0 by default

                # If a solutions exists (implies trajectories are non-parallel nor intersecting everywhere)
                if all(time > 0 for time in solution.values()):  # times calculated must be positive because we're travelling forward in time
                    ti, tj = solution.values()  # returns a dictionary where the keys are variables and values are their corresponding solutions
                    x_intersection = xi_future.subs(solution)  # must provide the solution as a dictionary of the sympy variable and its calculated value
                    y_intersection = yi_future.subs(solution)

                    if MIN_BOUND <= x_intersection <= MAX_BOUND and MIN_BOUND <= y_intersection <= MAX_BOUND:
                        solutions_found += 1

    print(f"Solutions found: {solutions_found}")


"""
You find a rock on the ground nearby. While it seems extremely unlikely, if you throw it just right, you should be able to hit every hailstone in a single throw!

You can use the probably-magical winds to reach any integer position you like and to propel the rock at any integer velocity. Now including the Z axis in your calculations, if you throw the rock at time 0, where do you need to be so that the rock perfectly collides with every hailstone? Due to probably-magical inertia, the rock won't slow down or change direction when it collides with a hailstone.

In the example above, you can achieve this by moving to position 24, 13, 10 and throwing the rock at velocity -3, 1, 2. If you do this, you will hit every hailstone as follows:

Hailstone: 19, 13, 30 @ -2, 1, -2
Collision time: 5
Collision position: 9, 18, 20

Hailstone: 18, 19, 22 @ -1, -1, -2
Collision time: 3
Collision position: 15, 16, 16

Hailstone: 20, 25, 34 @ -2, -2, -4
Collision time: 4
Collision position: 12, 17, 18

Hailstone: 12, 31, 28 @ -1, -2, -1
Collision time: 6
Collision position: 6, 19, 22

Hailstone: 20, 19, 15 @ 1, -5, -3
Collision time: 1
Collision position: 21, 14, 12
Above, each hailstone is identified by its initial position and its velocity. Then, the time and position of that hailstone's collision with your rock are given.

After 1 nanosecond, the rock has exactly the same position as one of the hailstones, obliterating it into ice dust! Another hailstone is smashed to bits two nanoseconds after that. After a total of 6 nanoseconds, all of the hailstones have been destroyed.

So, at time 0, the rock needs to be at X position 24, Y position 13, and Z position 10. Adding these three coordinates together produces 47. (Don't add any coordinates from the rock's velocity.)

Determine the exact position and velocity the rock needs to have at time 0 so that it perfectly collides with every hailstone. What do you get if you add up the X, Y, and Z coordinates of that initial position?
"""
import numpy as np

rx, ry, rz, vxr, vyr, vzr = sym.symbols("rx, ry, rz, vxr, vyr, vzr")

with open("day4.txt", "r") as txt_file:
    """
    Notice that initially, we have 6 variables (unknowns) related to the rock's initial positions and velocities.
    Then, for each hailstone we consider intersecting with the rock at a specific time, we introduce an additional variable (ti).

    Notice also that every hailstone we consider intersecting with the rock adds 3 equations (one for each dimension).

    Now, denoting "n" as the number of hailstones (events) considered, we have:
        - 6 + n --> degrees of freedom (number of unknowns in the system)
        - 3n --> number of constraints (number of equations)

    Therefore, to obtain an exactly determined system (exactly one solution), we need have an equal number of DoF and equations:
        ==> 6 + n = 3n
        ==> n = 3

    Therefore, to solve this problem, we need to consider 3 linearly independent events (hailstones) to find a unique solution.
    """
    hailstones = txt_file.readlines()
    hailstones = tuple(map(clean_hailstones, hailstones))

    positions_1, velocities_1 = hailstones[0]
    positions = [positions_1]
    matrix = [velocities_1]  # select and insert the first vector to be in our matrix

    for hailstone in hailstones[1:]:
        positions_2, velocities_2 = hailstone

        if not all(coord == 0 for coord in np.cross(velocities_1, velocities_2)):  # if cross product is non-zero (not the zero vector) (implies vectors are linearly independent)
            positions.append(positions_2)
            matrix.append(velocities_2)
            break

    while len(matrix) == 2:
        for hailstone in hailstones[1:]:
            positions_3, velocities_3 = hailstone

            if np.linalg.det(matrix + [velocities_3]) != 0:  # if adding the new vector to the matrix results in a non-zero determinant, it implies the set of three vectors is linearly independent
                positions.append(positions_3)
                matrix.append(velocities_3)
                break

    equations = []

    for i, (positions_i, velocities_i) in enumerate(zip(positions, matrix)):
        t = sym.symbols(f"t{i}")
        x, y, z = positions_i
        vx, vy, vz = velocities_i

        equations.append(rx + vxr * t - (x + vx*t))
        equations.append(ry + vyr * t - (y + vy * t))
        equations.append(rz + vzr * t - (z + vz * t))

    solution = sym.solve(equations)[0]

    print(solution[rx] + solution[ry] + solution[rz])
