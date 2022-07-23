import time
import urx
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    rob = urx.Robot("192.168.1.10")
    #rob = urx.Robot("localhost")
    rob.set_tcp((0,0,0,0,0,0))
    rob.set_payload(0.5, (0,0,0))
    try:
        l = 0.05
        v = 0.1
        a = 0.3
        pose = rob.getl()
        time.sleep(2)
        print("robot tcp is at: ", pose)
        print("absolute move in base coordinate ")
        pose[2] += l
        rob.movel(pose, acc=a, vel=v, wait=False)
        time.sleep(2)
        print("relative move in base coordinate ")
        rob.translate((0, 0, -l), acc=a, vel=v, wait=False)
        time.sleep(1)
        print("relative move back and forth in tool coordinate")
        rob.translate_tool((0, 0, -l), acc=a, vel=v, wait=False)
        time.sleep(2)
        rob.translate_tool((0, 0, l), acc=a, vel=v, wait=False)
        time.sleep(2)
    finally:
        rob.close()

