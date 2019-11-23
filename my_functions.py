import numpy as np
import math

def triangle_wave(theta):
    theta = np.array([theta])
    output = np.zeros(theta.shape[0])
    for idx  in range(len(theta)):
        theta_now = theta[idx]
        while theta_now > 2*math.pi:
            theta_now = theta_now - 2*math.pi
        if theta_now < math.pi/2:
            output[idx] =  2* theta_now / math.pi
        elif (theta_now >= math.pi/2) and (theta_now < 3*math.pi/2):
            output[idx] = -2*theta_now/math.pi + 2
        elif theta_now >= 3*math.pi/2 :
            output[idx] = 2*theta_now/math.pi - 4
        else:
            print(' triangle wave defined in interval 0 to 2*pi')
    return output