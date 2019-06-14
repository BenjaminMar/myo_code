#!/usr/bin/env python
#ROS
import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist

def callback(data):
    global pub
    print(data.data)
    msg = Twist()

    #pouce
    if(data.data == 1):
        msg.angular.z = -1
    #index
    elif(data.data == 2):
        msg.linear.x = 1
    #majeur
    elif(data.data == 3):
        msg.linear.x = 1
    #annulaire
    elif(data.data == 4):
        msg.linear.x = -1
    #auriculaire
    elif(data.data == 5):
        msg.angular.z = 1
    else:
        msg.linear.x = 0
        msg.angular.z = 0

    msg.linear.y = 0
    msg.linear.z = 0
    msg.angular.x = 0
    msg.angular.y = 0
    pub.publish(msg)


####################################################################

def listener():
    global pub

    rospy.init_node('rt2turtle', anonymous=True)
    rospy.Subscriber("rt_cmd", Int8, callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.spin()

####################################################################
if __name__ == '__main__':
    listener()