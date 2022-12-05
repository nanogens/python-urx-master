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
        xyz = 0
        xyzdelta = 0.005
        gripcloseset = 3

        #jointz = array(joints, [0.0, 0.0, 0.0, 7, 9])

        definedwaypoint = (-2.0432561079608362, -0.5984586042216797, 1.2107704321490687, -2.2185684643187464, -1.5391314665423792, -0.4559586683856409)

        jointz = motion.joints
        jointzz = []
        jointzz = [jointz, jointz, jointz, jointz, jointz, jointz, jointz, jointz]

        # initialize all coordinates in waypoints of array to zero
        for setzero in range(len(jointzz)):
            jointzz[setzero] = (0, 0, 0, 0, 0, 0)

        jointzz[1] = (-2.0430763403521937, -0.8392384809306641, 0.8563421408282679, -1.6201797924437464, -1.5386770407306116, -0.45425635973085576)
        jointzz[2] = (-2.0432561079608362, -0.5984586042216797, 1.2107704321490687, -2.2185684643187464, -1.5391314665423792, -0.4559586683856409)
        jointzz[3] = (-2.0430763403521937, -0.8392384809306641, 0.8563421408282679, -1.6201797924437464, -1.5386770407306116, -0.45425635973085576)

        jointzz[4] = (-1.6257918516742151, -0.8480075162700196, 0.8989456335650843, -1.6648899517455042, -1.5539429823504847, -0.037108723317281544)
        jointzz[5] = (-1.6259477774249476, -0.5841515821269532, 1.187594238911764, -2.219907423058981, -1.555368725453512, -0.037421528493062794)
        jointzz[6] = (-1.6257918516742151, -0.8480075162700196, 0.8989456335650843, -1.6648899517455042, -1.5539429823504847, -0.037108723317281544)

        jointzz[7] = (0, 0, 0, 0, 0, 0)
        while i < 1:


            while True:  # making a loop

                # Return to Home
                if keyboard.is_pressed('h'):
                    time.sleep(0.2)
                    motion.axisMove(rob, (0, 0, 0, 0, 0, 0), acc=a, vel=v)

                # Erase all Waypoints
                elif keyboard.is_pressed('e'):  # if key 'e' is pressed
                    time.sleep(0.2)
                    print('\nErasing all waypoints...')
                    wp_index = 0 # delete all waypoints
                    # erase all waypoints -- initialize all coordinates in waypoints of array to zero
                    for setzero in range(len(jointzz)):
                        jointzz[setzero] = (0, 0, 0, 0, 0, 0)

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
                    motion.axisMove(rob, (step * index, 0, 0, 0, 0, 0), acc=a, vel=v)
                    index = index + 1;
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

                # Open the connection to the robot
                elif keyboard.is_pressed('o'):
                    time.sleep(0.2)
                    print('\nOpen connection to robot...')
                    rob.close()
                    rob = urx.Robot("192.168.1.10")
                    motion = UR3e_MotionControl(rob, (0.0, 0, 0, 0, 0, 0))

                # Save the waypoint
                elif keyboard.is_pressed('w'):
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

                # Save the waypoint
                elif keyboard.is_pressed('a'):
                    time.sleep(0.2)
                    for f in range(len(jointzz)):
                        txt2 = "\nWaypoint Readoout " + str(f) + " : "
                        print(txt2)
                        print(jointzz[f])

                # Calibrate the gripper
                elif keyboard.is_pressed('k'):
                    time.sleep(0.2)
                    asyncio.run(run())

                # Move the gripper up to the point specified - pos/speed/force
                elif keyboard.is_pressed('p'):
                    time.sleep(0.2)
                    asyncio.run(grippermove(gripcloseset, 5, 10)) # pos,speed,force

                # Move the gripper up to the point specified - pos/speed/force
                elif keyboard.is_pressed('y'):
                    time.sleep(0.2)
                    gripcloseset = gripcloseset + 5
                    asyncio.run(grippermove(gripcloseset, 5, 10)) # pos,speed,force
                    print("\nGripcloseset value: ", gripcloseset)

                # Get pos xyz
                elif keyboard.is_pressed('d'):
                    time.sleep(0.2)
                    xyz = rob.get_pos()
                    print(xyz)

                # Set pos xyz (as defined by 'd') where get_pos is used to save an xyz coordinate system
                elif keyboard.is_pressed('z'):
                    time.sleep(0.2)
                    rob.set_pos((-0.28313, -0.42972, 0.12349), 0.1, 0.05, False)
                    print("\nReached the set position")




                # Setpos - Increment axis X
                elif keyboard.is_pressed('s'):
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x + xyzdelta, rob.get_pos().y, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new incremental X set position")

                # Setpos - Decrement axis X
                elif keyboard.is_pressed('i'):
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x - xyzdelta, rob.get_pos().y, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new decremental X set position")

                # Setpos - Increment axis Y
                elif keyboard.is_pressed('j'):
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y + xyzdelta, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new incremental Y set position")

                # Setpos - Decrement axis Y
                elif keyboard.is_pressed('r'):
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y - xyzdelta, rob.get_pos().z), 0.01, 0.01, False)
                    print("\nReached the new decremental Y set position")

                # Setpos - Increment axis Z
                elif keyboard.is_pressed('n'):
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y, rob.get_pos().z + xyzdelta), 0.01, 0.01, False)
                    print("\nReached the new incremental Z set position")

                # Setpos - Decrement axis Z
                elif keyboard.is_pressed('b'):
                    time.sleep(0.2)
                    rob.set_pos((rob.get_pos().x, rob.get_pos().y, rob.get_pos().z - xyzdelta), 0.01, 0.01, False)
                    print("\nReached the new decremental Z set position")



                # Go to a defined waypoint
                elif keyboard.is_pressed('t'):
                    time.sleep(0.2)
                    motion.axisMove(rob, definedwaypoint, acc=a, vel=v)
                    print("\nReached the defined waypoint")

                # Cycle through waypoints
                elif keyboard.is_pressed('u'):
                    time.sleep(0.2)
                    for r in range(len(jointzz)):
                        print('\nMoving to Waypoint #', r)
                        motion.axisMove(rob, jointzz[r], acc=a, vel=v)

                        if(r == 0): # home
                            asyncio.run(run())  # calibrate the gripper
                        if(r == 1): # point above object source
                            time.sleep(0.5)
                            asyncio.run(grippermove(4, 5, 10)) # open gripper
                        elif(r == 2): # object source
                            time.sleep(0.5)
                            asyncio.run(grippermove(143, 5, 10)) # close gripper
                        elif(r == 5): # object dest
                            time.sleep(0.5)
                            asyncio.run(grippermove(4, 5, 10))
                    print('\nVisited all waypoints!')

                # Cycle through waypoints
                elif keyboard.is_pressed('f'):
                    time.sleep(0.2)
                    for r in range(len(jointzz)):
                        print('\nMoving to Waypoint #', r)
                        motion.axisMove(rob, jointzz[r], acc=a, vel=v)
                    print('\nVisited all waypoints!')

            print("stop robot")
            rob.stopj()
            time.sleep(1)



    finally:
        rob.close()
