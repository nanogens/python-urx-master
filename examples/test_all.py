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

    rob = urx.Robot("192.168.1.10")
    # rob = urx.Robot("localhost")
    # grip = urx.Robot("127.0.0.1")
    # robotiqgrip = Robotiq_Two_Finger_Gripper() # gripper

    motion = UR3e_MotionControl(rob, (0.0, 0, 0, 0, 0, 0))

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

        index = 0
        step = 0.25
        wp_index = 0

        #jointz = array(joints, [0.0, 0.0, 0.0, 7, 9])

        jointz = motion.joints
        jointzz = []
        jointzz = [jointz, jointz, jointz, jointz, jointz]



        while i < 1:


            while True:  # making a loop

                # Return to Home
                if keyboard.is_pressed('h'):
                    time.sleep(0.2)
                    index = 0 # how many steps we take in the azimuth step example
                    wp_index = 0 # delete all waypoints
                    motion.axisMove(rob, (0, 0, 0, 0, 0, 0), acc=a, vel=v)

                # Erase all Waypoints
                elif keyboard.is_pressed('e'):  # if key 'e' is pressed
                    time.sleep(0.2)
                    print('\nErasing all waypoints...')
                    wp_index = 0 # delete all waypoints
                    for wipe in range(5):
                        jointzz[wipe] = 0

                # Get and show the current joint positions
                elif keyboard.is_pressed('m'):  # if key 'm' is pressed
                    time.sleep(0.2)  #added to prevent repetitive keystoke inputs
                    print('You Pressed the "m" key!')
                    jointz = rob.getj()
                    print("\nRobot joint positions: ", jointz)

                # Advance a step - counts up to 5 steps then quit
                elif keyboard.is_pressed('q'):  # if key 'q' is pressed
                    time.sleep(0.2)
                    print('You Pressed the "q" key!')
                    index = index + 1
                    motion.axisMove(rob, (step * index, 0, 0, 0, 0, 0), acc=a, vel=v)
                    #if index == 5:
                        #break  # finishing the loop

                # Move to the stored joint position stored when "m" was pressed
                elif keyboard.is_pressed('g'):
                    time.sleep(0.2)
                    motion.axisMove(rob, jointz, acc=a, vel=v)

                # Close the connection to the robot
                elif keyboard.is_pressed('c'):
                    time.sleep(0.2)
                    print('\nClosed connection to robot...')
                    rob.close()

                # Open the econnection to the robot
                elif keyboard.is_pressed('o'):
                    time.sleep(0.2)
                    print('\nOpen connection to robot...')
                    rob.close()
                    rob = urx.Robot("192.168.1.10")
                    motion = UR3e_MotionControl(rob, (0.0, 0, 0, 0, 0, 0))

                # Save the waypoint
                elif keyboard.is_pressed('w'):
                    time.sleep(0.2)
                    if wp_index < 5:
                        jointzz[wp_index] = rob.getj()
                        for x in range(5):
                            txt = "\nWaypoint " + str(x) + " : "
                            print(txt)
                            print(jointzz[x])
                        wp_index = wp_index + 1
                    else:
                        print('\nWaypoints array filled!')

                # Calibrate the gripper
                elif keyboard.is_pressed('k'):
                    time.sleep(0.2)
                    asyncio.run(run())

                # Move the gripper up to the point specified - pos/speed/force
                elif keyboard.is_pressed('p'):
                    time.sleep(0.2)
                    asyncio.run(grippermove(150,5,20)) # pos,speed,force

                # Cycle through waypoints
                elif keyboard.is_pressed('u'):
                    time.sleep(0.2)
                    for r in range(5):
                        print('\nMoving to Waypoint #', r)
                        motion.axisMove(rob, jointzz[r], acc=a, vel=v)
                    print('\nVisited all waypoints!')

            print("stop robot")
            rob.stopj()
            time.sleep(1)



    finally:
        rob.close()
