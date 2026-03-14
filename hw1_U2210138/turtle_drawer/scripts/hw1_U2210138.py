#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def get_twist(linear_x, angular_z):
    """Helper to create a velocity message"""
    msg = Twist()
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    return msg

def move():
    rospy.init_node('turtle_mover')
    
    # FIXED: Changed queue_msg_size to queue_size
    # Mapping the turtle names to their publishers
    p0 = rospy.Publisher('/t0/cmd_vel', Twist, queue_size=10)
    p1 = rospy.Publisher('/t1/cmd_vel', Twist, queue_size=10)
    p3 = rospy.Publisher('/t3/cmd_vel', Twist, queue_size=10)
    p8 = rospy.Publisher('/t8/cmd_vel', Twist, queue_size=10)
    
    rate = rospy.Rate(10) # 10Hz for smoother movement
    start_time = rospy.get_time()

    rospy.loginfo("Drawing digits 0, 1, 3, 8...")

    while not rospy.is_shutdown():
        now = rospy.get_time() - start_time
        
        # t0: Draw 0 (Circle)
        if now < 2.14: # 6.3
            p0.publish(get_twist(0.80, 1.28))
        elif 2.14 <= now < 3.14:
            p0.publish(get_twist(2.1, 0.5))
        elif 3.14 <= now < 5.28:
            p0.publish(get_twist(0.80, 1.25)) # 1.28 -> 1.2
        elif 5.28 <= now < 6.28:
            p0.publish(get_twist(2.1, 0.5))
        elif 6.28 <= now < 8.42:
            p0.publish(get_twist(0.80, 1.28))
        else:
            p0.publish(get_twist(0, 0))
#--------------------------------------------------
        # t1: Digit 1 with an inclined hook
        if now < 0.3:
            # Phase 1: Draw the incline (the hook)
            p1.publish(get_twist(0.0, 0.7)) 
            
        elif 0.3 <= now < 0.6:
            # Pivot to face perfectly DOWN (-1.57 radians)
            # rotate from -0.785 to -1.57
            p1.publish(get_twist(1.0, 0)) 
            
        elif 0.6 <= now < 1.32:
            # Phase 3: Draw the vertical stem
            p1.publish(get_twist(1.5, 0.5))
            # p1.publish(get_twist(0, 3.1415))

        elif 1.32 <= now < 2.4:
            p1.publish(get_twist(0, 3.14))

        elif 2.4 <= now < 3.6:
            p1.publish(get_twist(2.3, 0))

        else:
            # Stop
            p1.publish(get_twist(0, 0))
#--------------------------------------------------
        # t3: Draw 3 (Two arcs)
        if now < 1.57:
            # Phase 1: Top Arc
            p3.publish(get_twist(2.2, -3.0)) # -6?
            
        elif 1.57 <= now < 2.5:
            # Phase 2: THE PIVOT (Increased from 0.43s to 0.93s)
            # We stop linear movement and just rotate
            p3.publish(get_twist(0.0, 4.3)) 
            
        elif 2.5 <= now < 4.07:
            # Phase 3: Bottom Arc
            p3.publish(get_twist(2.2, -3.0))
            
        else:
            # Stop
            p3.publish(get_twist(0, 0))
#--------------------------------------------------
        # t8: Draw 8 (Figure 8)
        if now < 3.14:
            p8.publish(get_twist(1.5, 2.0))
        elif now < 9.42:
            p8.publish(get_twist(1.5, -2.0))
        else:
            p8.publish(get_twist(0, 0))

        # Stop the script after 10 seconds
        if now > 10.0:
            rospy.loginfo("Finished drawing.")
            break
            
        rate.sleep()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass