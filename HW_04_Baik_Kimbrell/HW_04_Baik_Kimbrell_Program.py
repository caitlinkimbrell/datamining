import BirdBathFunction_424_v420 as bb424
import BirdBathFunction_431_v420 as bb431


def helper(func):
    """
    Using three different increments, find how much tilt, roll, and twist of the birdbath
    yields maximum water-holding ability.
    :param func: an unknown convex function of birdbath
    """
    curr_best_water = -1
    curr_best_roll = -1
    curr_best_twist = -1
    curr_best_tilt = -1
    mini = -45
    maxi = 45
    delta = [12, 6, 1]
    for d in delta:
        roll = mini                     # set the three variables to the minimum of the range
        tilt = mini
        twist = mini
        curr_best_water, curr_best_roll, curr_best_tilt, curr_best_twist = findbest(roll, tilt, twist, mini, maxi, d, func)
        curr_bests = [curr_best_roll, curr_best_tilt, curr_best_twist]
        mini = min(curr_bests) - d      # mini is minimum of the current best values - current delta
        maxi = max(curr_bests) + d      # maxi is maximum of the current best values + current delta

    return curr_best_water, curr_best_roll, curr_best_tilt, curr_best_twist


def findbest(roll, tilt, twist, min, max, delta, func):
    """
    Get the roll, tilt, and twist values in degrees that
    enable the birdbath to hold the maximum amount of water.
    """
    best_water = -1
    best_roll = -1
    best_tilt = -1
    best_twist = -1
    while roll < max:                           # until roll, tilt, twist values hit max value in a range
        tilt = min                              # evaluate how much water it holds and increment by delta
        while tilt < max:
            twist = min
            while twist < max:
                water = func(roll, tilt, twist)
                if(water > best_water):         # compare the current water fraction with the best water fraction
                    best_water = water
                    best_roll = roll
                    best_tilt = tilt
                    best_twist = twist
                twist+= delta                   # increment the twist, tilt, roll by delta
            tilt +=  delta
        roll += delta
    return best_water, best_roll, best_tilt, best_twist


if __name__ == '__main__' :
    print('Bird Bath Function 424\n')
    best_water, best_roll, best_tilt, best_twist = helper(bb424.BirdbathFunc424) # get the max water fraction
    print('Best Fraction of Water = ', best_water, '\n')                         # of #424 birdbath function
    print('Roll: ', best_roll, " Tilt: ", best_tilt, " Twist: ", best_twist)     # and three vars for it
    print('\n###\n')
    print('Bird Bath Function 431\n')
    best_water, best_roll, best_tilt, best_twist = helper(bb431.BirdbathFunc431) # get the max water fraction
    print('Best Fraction of Water = ', best_water, '\n')                         # of #431 birdbath function
    print('Roll: ', best_roll, " Tilt: ", best_tilt, " Twist: ", best_twist)     # and three vars for that