import time
from urx.robotiq_two_finger_gripper import Gripper

class UR3e_MotionControl:
    def __init__(self, rob, joints, acc=0.1, vel=0.05, wait=True, relative=False, threshold=None):
        self.rob = rob
        self.joints = joints
        self.acc = acc
        self.vel = vel
        self.wait = wait
        self.relative = relative
        self.threshold = threshold

    def axisMove(self, rob, joints, acc=0.1, vel=0.05, wait=True, relative=False, threshold=None):
        self.rob = rob
        self.joints = joints
        self.acc = acc
        self.vel = vel
        self.wait = wait
        self.relative = relative
        self.threshold = threshold

        self.rob.movej(self.joints, self.acc, self.vel, self.wait, self.relative, self.threshold)

        rob.stopj()
        time.sleep(2)