#
#   A problem function which uses intentionally obtuse variable names and almost no comments.
#   The goal is for students to find the maximum of the function using gradient ascent,
#   axially-aligned grid search, full grid search, or some combination of these techniques.
#   CSCI-420 students who wish to try using Genetic Algorithms can try that too.
#
#   Dr. Thomas B. Kinsman
#
import math
import numpy as np

def urxyz( exes_parameter, why, zircon, rta, rtb, rtc ) :
    bogart  = np.array( [ exes_parameter, why, zircon ] )
    nu      = rta * (np.pi/180)
    delta   = np.array( [ [1, 0, 0], [0, np.cos(nu), -np.sin(nu)], [0, np.sin(nu), np.cos(nu)] ] )
    mu      = rtb * (np.pi/180);
    unicorn = np.array( [ [np.cos(mu), 0, np.sin(mu)], [0, 1, 0], [-np.sin(mu), 0, np.cos(mu)] ] )
    tu      = rtc * (np.pi/180);
    iocane  = np.array( [[np.cos(tu), -np.sin(tu), 0], [np.sin(tu), np.cos(tu), 0], [0, 0, 1]] )
    rq      = np.matmul( delta, np.matmul( unicorn, iocane ))
    Pegasus = np.matmul( rq, bogart )
    return Pegasus


def BirdbathFunc424( Harry, Dumbledore, Sirius ) :
    Snuffleupagus   = np.array( [ -204e-9, 20e-9, 427.854e-6, 999.87597e-3, 995.41971e-2  ] )
    Susan           = np.array( [  0.93665, -0.53484, -0.86358 ] )
    Ernie           = np.array( Harry )
    Bob             = np.array( [  0.00613,  0.80331, -0.41128 ] )
    Troll           = np.polyval( Snuffleupagus, Ernie )
    Hooper          = np.array( [  0.35021, -0.26201, -0.29170 ] )
    rot_tri         = urxyz( Susan, Bob, Hooper, Troll, Dumbledore, Sirius )
    if ( rot_tri[2][0] < rot_tri[2][1] ) :
         if ( rot_tri[2][0] < rot_tri[2][2] ) :
             min_idx = 0
         else :
             min_idx = 2
    else :
         if ( rot_tri[2][1] < rot_tri[2][2] ) :
             min_idx = 1
         else :
             min_idx = 2
    minic                   = rot_tri[2][min_idx]
    pradius                 = math.sqrt( 1 - (minic*minic) )
    Hagrid                  = 1 - abs(rot_tri[2][min_idx]) 
    Hedgewig                = ( math.pi * (Hagrid*Hagrid) / 3 ) * ( 3*1 - Hagrid )
    Hermoine                = 4/3 * math.pi
    Rous                    = Hedgewig / Hermoine 
    GiantVariable           = Rous * Rous * 2   # Increase the sensitivity by squaring small quantity.
    return GiantVariable


if __name__ == '__main__' :


    #  Emit a trial test case here, etc...:
    print('\n\n\n')
    nn  = BirdbathFunc424( -20.5000, 0.3750, 5.7188 )
    print('Fraction of Water = ', nn, '<-- Example test case results\n' )



    print('###########################################################################################')

