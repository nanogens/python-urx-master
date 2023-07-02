"""
Testing script that runs many of the urx methods, while attempting to keep robot pose around its starting pose
"""

from math import pi
import time
import sys

import urx
import logging

import keyboard

import asyncio
from urx.robotiq_two_finger_gripper import Gripper
from UR3e_MotionControl import UR3e_MotionControl

from array import *

async def log_info(gripper):
    print(f"Pos: {str(await gripper.get_current_position()): >3}  "
          f"Open: {await gripper.is_open(): <2}  "
          f"Closed: {await gripper.is_closed(): <2}  ")


async def run():
    gripper = Gripper("192.168.1.10")  # actual ip of the ur arm
    await gripper.connect()
    await gripper.activate()  # calibrates the gripper

    await gripper.move(200, 50, 20)
    await gripper.move(50, 50, 20)
    await gripper.disconnect()

async def grippermove(pos=50,speed=10,force=20):
    gripper = Gripper("192.168.1.10")  # actual ip of the ur arm
    await gripper.connect()
    await gripper.move(pos, speed, force)
    time.sleep(2)
    await gripper.disconnect()

def wait():
    if do_wait:
        print("Click enter to continue")
        input()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    do_wait = True
    if len(sys.argv) > 1:
        do_wait = False

    # establish connection with robot arm
    rob = urx.Robot("192.168.1.10")
    # motion control object
    motion = UR3e_MotionControl(rob, (0.0, 0, 0, 0, 0, 0))

    print("Setting TCP...")
    rob.set_tcp((0, 0, 0, 0, 0, 0))
    print("Setting Default Maximum Anticipated Payload...")
    rob.set_payload(0.5, (0, 0, 0))
    print("Preliminary Settings Complete...")

    try:
        # ensure robot is stopped
        print("stop robot")
        rob.stopj()
        time.sleep(1)

        # ----------------------------------------------------------

        # don't need this
        l = 0.05
        v = 6.50
        a = 0.25
        r = 0.10
        print("Digital out 0 and 1 are: ", rob.get_digital_out(0), rob.get_digital_out(1))
        print("Analog inputs are: ", rob.get_analog_inputs())

        # get initial joint positions and display them
        initj = rob.getj()
        print("Initial joint configuration is ", initj)
        t = rob.get_pose()
        time.sleep(1)
        print("Transformation from base to tcp is: ", t)

        # ----------------------------------------------------------

        # global variables
        i = 0
        index = 0
        step = 0.25
        wp_index = 0
        xyz = 0
        xyzdelta = 0.005
        gripcloseset = 3

        # ----------------------------------------------------------

        # this is a single defined waypoint
        definedwaypoint = (1.0857954025268555, -0.2617195409587403, 0.9592779318438929, -2.216668268243307, -1.531335179005758, 1.1343679428100586)

        # ----------------------------------------------------------

        # arrays holding joint positions
        jointz = motion.joints
        jointzz = []
        jointzz = [jointz, jointz, jointz, jointz, jointz, jointz, jointz, jointz, jointz]

        # ----------------------------------------------------------

        # initialize all coordinates in waypoints of array to zero
        for setzero in range(len(jointzz)):
            jointzz[setzero] = (0, 0, 0, 0, 0, 0)

        # load in all the waypoints
            # home
            jointzz[1] = (0, 0, 0, 0, 0, 0)

            # position above object (source)
            jointzz[2] = (1.0857954025268555, -0.2617195409587403, 0.9592779318438929, -2.216668268243307, -1.531335179005758, 1.1343679428100586)

            # position blelow object (source)
            jointzz[3] = (1.0862512588500977, -0.029597119694091845, 0.7858131567584437, -2.2747250996031703, -1.5312512556659144, 1.1338286399841309)

            # position above object (source)
            jointzz[4] = (1.0857954025268555, -0.2617195409587403, 0.9592779318438929, -2.216668268243307, -1.531335179005758, 1.1343679428100586)

            # position above object (dest)
            jointzz[5] = (1.2588582038879395, -0.30276282251391606, 1.0660179297076624, -2.290422578851217, -1.5229170958148401, 1.3078656196594238)

            # position below object (dest)
            jointzz[6] = (1.2592053413391113, -0.11561758935961919, 0.9416797796832483, -2.352659841577047, -1.5229170958148401, 1.3074584007263184)

            # position above object (dest)
            jointzz[7] = (1.2588582038879395, -0.30276282251391606, 1.0660179297076624, -2.290422578851217, -1.5229170958148401, 1.3078656196594238)

            jointzz[8] = (0, 0, 0, 0, 0, 0)

        # ----------------------------------------------------------


        # ----------------------------------------------------------

        action = 0
        command = 0

        # loop for 1x iteration
        while i < 1:
            # check to see if key is pressed
            if(action == 0):
                while True:
                    command = keyboard.read_key()
                    time.sleep(0.2)
                    break
                action = 1

            # if a key was pressed, check to see if the key was an actual command
            while action == 1:  # making a loop
                # Return to Home
                if command == 'h':
                    time.sleep(0.2)
                    motion.axisMove(rob, (0, 0, 0, 0, 0, 0), acc=a, vel=v)
                    action = 0

                # Erase all Waypoints
                elif command == 'e': # if key 'e' is pressed
                    time.sleep(0.2)
                    print('\nErasing all waypoints...')
                    wp_index = 0 # delete all waypoints
                    # erase all waypoints -- initialize all coordinates in waypoints of array to zero
                    for setzero in range(len(jointzz)):
                        jointzz[setzero] = (0, 0, 0, 0, 0, 0)
                    action = 0

                # Get and show the current joint positions
                elif command == 'm':  # if key 'm' is pressed
                    time.sleep(0.2)  #added to prevent repetitive keystoke inputs
                    print('You Pressed the "m" key!')
                    jointz = rob.getj()
                    print("\nRobot joint positions: ", jointz)
                    action = 0

                # Advance a step - counts up to 5 steps then quit - removed, infinite increments now
                elif command == 'q':  # if key 'q' is pressed
                    time.sleep(0.2)
                    print('You Pressed the "q" key!')
                    motion.axisMove(rob, (step * index, 0, 0, 0, 0, 0), acc=a, vel=v)
                    index = index + 1;
                    #if index == 5:
                        #break  # finishing the loop
                    action = 0

                # Move to the stored joint position stored when "m" was pressed
                elif command == 'g':
                    time.sleep(0.2)
                    motion.axisMove(rob, jointz, acc=a, vel=v)
                    action = 0

                # Close the connection to the robot
                elif command == 'c':
                    time.sleep(0.2)
                    print('\nClosed connection to robot...')
                    rob.close()
                    action = 0

                # Open the connection to the robot
                elif command == 'o':
                    time.sleep(0.2)
                    print('\nOpen connection to robot...')
                    rob.close()
                    rob = urx.Robot("192.168.1.10")
                    motion = UR3e_MotionControl(rob, (0.0, 0, 0, 0, 0, 0))
                    action = 0

                # Save the waypoint
                elif command == 'w':
                    time.sleep(0.2)
                    if wp_index < len(jointzz):
                        jointzz[wp_index] = rob.getj()
                        for x in range(len(jointzz)):
                            txt = "\nWaypoint " + str(x) + " : "
                            print(txt)
                            print(jointzz[x])
                        wp_index = wp_index + 1
                    else:
                        print('\nWaypoints array filled!')
                    action = 0

                # Save the waypoint
                elif command == 'a':
                    time.sleep(0.2)
                    for f in range(len(jointzz)):
                        txt2 = "\nWaypoint Readoout " + str(f) + " : "
                        print(txt2)
                        print(jointzz[f])
                    action = 0

                # Calibrate the gripper
                elif command == 'k':
                    time.sleep(0.2)
                    asyncio.run(run())
                    action = 0

                # Move the gripper up to the point specified - pos/speed/force
                elif command == 'p':
                    time.sleep(0.2)
                    asyncio.run(grippermove(gripcloseset, 5, 10)) # pos,speed,force
                    action = 0

                # Move the gripper up to the point specified - pos/speed/force
                elif command == 'y':
                    time.sleep(0.2)
                    gripcloseset = gripcloseset + 5
                    asyncio.run(grippermove(gripcloseset, 5, 10)) # pos,speed,force
                    print("\nGripcloseset value: ", gripcloseset)
                    action = 0

                # Get pos xyz
                elif command == 'd':
                    time.sleep(0.2)
                    xyz = rob.get_pos()
                    print(xyz)
                    action = 0

                # Set pos xyz (as defined by 'd') where get_pos is used to save an xyz coordinate system
                elif command == 'z':
                    time.sleep(0.2)
                    rob.set_pos((-0.28313, -0.42972, 0.12349), 0.1, 0.05, False)
                    print("\nReached the set position")
                    action = 0




                # Setpos - Increment axis X
                elif command == 's':
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x + xyzdelta, rob.get_pos().y, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new incremental X set position")
                    action = 0

                # Setpos - Decrement axis X
                elif command == 'i':
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x - xyzdelta, rob.get_pos().y, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new decremental X set position")
                    action = 0

                # Setpos - Increment axis Y
                elif command == 'j':
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y + xyzdelta, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new incremental Y set position")
                    action = 0

                # Setpos - Decrement axis Y
                elif command == 'r':
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y - xyzdelta, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new decremental Y set position")
                    action = 0

                # Setpos - Increment axis Z
                elif command == 'n':
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y, rob.get_pos().z + xyzdelta), 0.01, 0.01, False)
                    print("\nReached the new incremental Z set position")
                    action = 0

                # Setpos - Decrement axis Z
                elif command == 'b':
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y, rob.get_pos().z - xyzdelta), 0.01, 0.01, False)
                    print("\nReached the new decremental Z set position")
                    action = 0



                # Go to a defined waypoint
                elif command == 't':
                    time.sleep(0.2)
                    motion.axisMove(rob, definedwaypoint, acc=a, vel=v)
                    print("\nReached the defined waypoint")
                    action = 0

                # Cycle through waypoints
                elif command == 'u':
                    time.sleep(0.2)
                    print('here')
                    for r in range(len(jointzz)):
                        print('\nMoving to Waypoint #', r)
                        motion.axisMove(rob, jointzz[r], acc=a, vel=v)

                        if(r == 0): # home
                            asyncio.run(run())  # calibrate the gripper
                        if(r == 1): # point above object source
                            time.sleep(0.5)
                        elif(r == 2): # object source
                            time.sleep(0.5)
                            asyncio.run(grippermove(3, 5, 10)) # open gripper
                        elif (r == 3):  # object source
                            time.sleep(0.5)
                            asyncio.run(grippermove(143, 5, 10))  # close gripper
                        elif(r == 6): # object dest
                            time.sleep(0.5)
                            asyncio.run(grippermove(3, 5, 10)) # open gripper
                    print('\nVisited all waypoints!')
                    action = 0

                # Open gripper
                elif command == 'x':
                    time.sleep(0.5)
                    asyncio.run(grippermove(3, 5, 10))  # open gripper
                    print('\nOpened gripper!')
                    action = 0

                # Close gripper
                elif command == 'l':
                    time.sleep(0.5)
                    asyncio.run(grippermove(143, 5, 10))  # close gripper
                    print('\nClosed gripper!')
                    action = 0

                # Cycle through waypoints
                elif command == 'f':
                    time.sleep(0.2)
                    for r in range(len(jointzz)):
                        print('\nMoving to Waypoint #', r)
                        motion.axisMove(rob, jointzz[r], acc=a, vel=v)
                    print('\nVisited all waypoints!')
                    action = 0

                elif (action == 1):
                    #action = 2 # you can make it 2 to exit
                    print("\ninvalid key")  # should be exiting
                    #i = 0
                    action = 0


    finally:
        print("Stopping robot...")
        print("\nExiting")
        rob.stopj()
        time.sleep(1)
        rob.close()
