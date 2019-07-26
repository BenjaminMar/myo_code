#!/usr/bin/env python
#ROS
import rospy
from std_msgs.msg import Int8
from std_msgs.msg import String

####################################################################

def callback(data):
    global stats
    global total
    global on

    if(on and total < 10):
        stats[data.data] = 1 + stats[data.data]
        total += 1
    elif(on and total == 10):
        print(stats)
        on = False

####################################################################

def inputs(data):
    global on
    global total
    global stats

    if(on and data.data == " "):
        on = True
    elif(not on and data.data == " "):
        total = 0
        stats = [0]*6
        on = True

####################################################################

def listener():
    global stats
    global total
    global on
    global max

    on = False
    total = 0
    stats = [0]*6

    rospy.init_node('graphs', anonymous=True)
    rospy.Subscriber("input_cmd", String, inputs)
    rospy.Subscriber("rt_cmd", Int8, callback)
    rospy.spin()

####################################################################
if __name__ == '__main__':
    listener()