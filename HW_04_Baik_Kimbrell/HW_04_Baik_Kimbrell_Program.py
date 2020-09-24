import BirdBathFunction_424_v420 as bb424
import BirdBathFunction_431_v420 as bb431


def helper(func):
    curr_best_water = -1
    curr_best_roll = -1
    curr_best_twist = -1
    curr_best_tilt = -1
    mini = -45
    maxi = 45
    delta = [12, 6, 1]
    for d in delta:
        roll = mini
        tilt = mini
        twist = mini
        curr_best_water, curr_best_roll, curr_best_tilt, curr_best_twist = findbest(roll, tilt, twist, mini, maxi, d, func)
        curr_bests = [curr_best_roll, curr_best_tilt, curr_best_twist]
        mini = min(curr_bests) - d
        maxi = max(curr_bests) + d

    return curr_best_water, curr_best_roll, curr_best_tilt, curr_best_twist


def findbest(roll, tilt, twist, min, max, delta, func):
    best_water = -1
    best_roll = -1
    best_tilt = -1
    best_twist = -1
    while roll < max:
        tilt = min
        while tilt < max:
            twist = min
            while twist < max:
                water = func(roll, tilt, twist)
                if(water > best_water):
                    best_water = water
                    best_roll = roll
                    best_tilt = tilt
                    best_twist = twist
                twist+= delta
            tilt +=  delta
        roll += delta
    return best_water, best_roll, best_tilt, best_twist


if __name__ == '__main__' :
    print('Bird Bath Function 424\n')
    best_water, best_roll, best_tilt, best_twist = helper(bb424.BirdbathFunc424)
    print('Best Fraction of Water = ', best_water, '\n')
    print('Roll: ', best_roll, " Tilt: ", best_tilt, " Twist: ", best_twist)
    print('\n###\n')
    print('Bird Bath Function 431\n')
    best_water, best_roll, best_tilt, best_twist = helper(bb431.BirdbathFunc431)
    print('Best Fraction of Water = ', best_water, '\n')
    print('Roll: ', best_roll, " Tilt: ", best_tilt, " Twist: ", best_twist)