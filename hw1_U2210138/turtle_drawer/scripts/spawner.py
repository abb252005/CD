#!/usr/bin/env python3
import rospy
from turtlesim.srv import Spawn, Kill

def setup_turtles():
    rospy.init_node('turtle_spawner')
    rospy.wait_for_service('kill')
    rospy.wait_for_service('spawn')
    
    spawner = rospy.ServiceProxy('spawn', Spawn)
    killer = rospy.ServiceProxy('kill', Kill)

    # Kill default turtle
    try: killer('turtle1')
    except: pass

    # Spawn 4 turtles: t0, t1, t3, t8
    spawner(1.65, 5.25, -1.175, "t0") # default, 5.0
    # spawner(5.0, 4.7, 0.16, "t1")
    spawner(4.25, 6.5, 1, "t1")
    spawner(6.5, 7.6, 0.41, "t3")
    spawner(9.5, 6.2, 0.37, "t8")
    print("Turtles spawned!")

if __name__ == '__main__':
    setup_turtles()