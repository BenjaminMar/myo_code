#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt8

#This node was done to get the user's comands from the terminal and send those to the other nodes

def callback(data):
	print(data.data)

def main():
	rospy.init_node('input', anonymous=True)
	pub = rospy.Publisher('input_cmd', String, queue_size=1)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		text = raw_input()
		pub.publish(text)
		rate.sleep()

if __name__ == '__main__':
	main()