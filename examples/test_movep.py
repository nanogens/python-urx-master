import time
import urx
import logging

if __name__ == "__main__":
    rob = urx.Robot("192.168.1.10")
    try:
        l = 0.17
        v = 0.17
        a = 0.01
        r = 0.05
        pose = rob.getl()
        pose[2] += l
        rob.movep(pose, acc=a, vel=v, wait=True)
        while True:
            p = rob.getl(wait=True)
            if p[2] > pose[2] - 0.05:
                break

        print("stop robot")
        rob.stopj()
        time.sleep(1)

        pose[1] += l
        rob.movep(pose, acc=a, vel=v, wait=True)
        while True:
            p = rob.getl(wait=True)
            if p[1] > pose[1] - 0.05:
                break

        print("stop robot")
        rob.stopj()
        time.sleep(1)

        pose[2] -= l
        rob.movep(pose, acc=a, vel=v, wait=True)
        while True:
            p = rob.getl(wait=True)
            if p[2] < pose[2] + 0.05:
                break

        pose[1] -= l
        rob.movep(pose, acc=a, vel=v, wait=True)

    finally:
        rob.close()
