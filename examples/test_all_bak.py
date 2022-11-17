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

    print("here 1")
    rob.set_tcp((0, 0, 0, 0, 0, 0))
    print("here 2")
    rob.set_payload(0.5, (0, 0, 0))
    print("here 3")

    try:
        l = 0.05
        v = 6.50
        a = 0.25
        r = 0.10
        print("Digital out 0 and 1 are: ", rob.get_digital_out(0), rob.get_digital_out(1))
        print("Analog inputs are: ", rob.get_analog_inputs())
        initj = rob.getj()
        print("Initial joint configuration is ", initj)
        t = rob.get_pose()
        time.sleep(1)
        print("Transformation from base to tcp is: ", t)

        print("stop robot")
        rob.stopj()
        time.sleep(1)

        # ----------------------------------------------------------
        i = 0
        while i < 1:
            print("Position: Home")
            rob.movej((0.0, 0, 0, 0, 0, 0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)

            # ----------------------------------------------------------

            print("Position: Base Rotation")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.25, 0, 0, 0, 0, 0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)

            # ----------------------------------------------------------

            print("Position: Rotational Lift")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 0, 0, 0, 0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)

            # ----------------------------------------------------------

            print("Position: Elbow Lift")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 2.1, 0, 0, 0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            print("Position: Wrist Lift")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 2.1, 3.3, 0, 0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            print("Position: Finger Rotation")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 2.1, 3.3, 6.3, 0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            print("Position: Ring Rotation")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 2.1, 3.3, 6.3, 6.3), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            # **********************************************************

            # ----------------------------------------------------------

            print("Position: Ring Rotation - Original")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 2.1, 3.3, 6.3, 0.0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            print("Position: Finger Rotation - Original")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 2.1, 3.3, 0.0, 0.0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            print("Position: Wrist Lift - Original")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 2.1, 0.0, 0.0, 0.0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            print("Position: Elbow Lift - Original")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, -3.15, 0.0, 0.0, 0.0, 0.0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------


            print("Position: Rotational Lift - Original")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((6.3, 0.0, 0.0, 0.0, 0.0, 0.0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------

            print("Position: Base Rotation - Original")
            # base rotation, rotational lift, elblow lift, wrist lift, finger rotation, ring rotation
            # 1.0 CCW      , -1.0  lift     ,-1.0 lift,   -1.0 lift  , -1.0 rotation  , -1.0 rotation
            rob.movej((0.0, 0.0, 0.0, 0.0, 0.0, 0.0), acc=a, vel=v)

            print("stop robot")
            rob.stopj()
            time.sleep(1)

            pose = rob.getl()
            print("robot tcp is at: ", pose)


            # ----------------------------------------------------------








            print(i)
            i += 1

    finally:
        rob.close()
