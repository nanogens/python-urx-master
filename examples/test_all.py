"""
Testing script that runs many of the urx methods, while attempting to keep robot pose around its starting pose 
"""

from math import pi
import time
import sys

import urx
import logging


def wait():
    if do_wait:
        print("Click enter to continue")
        input()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    do_wait = True
    if len(sys.argv) > 1:
        do_wait = False

    rob = urx.Robot("192.168.1.10")
    #rob = urx.Robot("localhost")
    rob.set_tcp((0, 0, 0, 0, 0, 0))
    rob.set_payload(0.5, (0, 0, 0))
    try:
        l = 13.5
        v = 5.5
        a = 1.5
        r = 0.41
        print("Digital out 0 and 1 are: ", rob.get_digital_out(0), rob.get_digital_out(1))
        print("Analog inputs are: ", rob.get_analog_inputs())
        initj = rob.getj()
        print("Initial joint configuration is ", initj)
        t = rob.get_pose()
        time.sleep(3)
        print("Transformation from base to tcp is: ", t)


        print("Translating in x")
        #wait()
        rob.translate((l, 5.0, 0), acc=a, vel=v, wait=False)
        time.sleep(6)
        pose = rob.getl()
        print("robot tcp is at: ", pose)

        print("moving in z")

        pose[2] += l
        rob.movel(pose, acc=a, vel=v, wait=False)
        print("Waiting 2s for end move")
        time.sleep(2)

        print("Moving through several points with a radius")

        pose[0] -= l
        p1 = pose[:]
        pose[2] -= l
        p2 = pose[:]
        rob.movels([p1, p2], vel=v, acc=a, radius=r, wait=False)

        print("rotate tcp around around base z ")

        t.orient.rotate_zb(pi / 8)
        rob.set_pose(t, vel=v, acc=a, wait=False)

        print("moving in tool z")
        rob.translate_tool((0, 0, l), vel=v, acc=a, wait=False)

        print("moving in tool -z using speed command")

        rob.speedl_tool((0, 0, -v, 0, 0, 0), acc=a, min_time=3)
        print("Waiting 2 seconds2")
        time.sleep(2)
        print("stop robot")
        rob.stopj()

        print("Test movec")

        pose = rob.get_pose()
        via = pose.copy()
        via.pos[0] += l
        to = via.copy()
        to.pos[1] += l
        rob.movec(via, to, acc=a, vel=v, wait=False)

        print("Sending robot back to original position")
        rob.movej(initj, acc=0.8, vel=0.2, wait=False)

    finally:
        rob.close()
