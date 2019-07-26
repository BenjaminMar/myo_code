#!/usr/bin/env python
import rospy
from datetime import datetime
datetime(2000, 1, 1)
from ros_myo.msg import EmgArray
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String
from std_msgs.msg import UInt8

############################################################
#This object manages all datas recived from the ros_myo node
class data_stack:
	_val = [0,0,0,0,0,0,0,0]
	total = 0
	_stacked_arrays = []
	_nbr_arrays = 0
	recording = False

	def __init__(self):
		self._val = [0,0,0,0,0,0,0,0]

	#Reset the current stack
	def reset(self):
		self._val = [0,0,0,0,0,0,0,0]
		self.total = 0
		self.recording = False
		self.name = ""

	#Reset all the stacked arrays
	def clear(self):
		self._stacked_arrays = []

	#Overload the + operator
	#Add the last raw data array to the current stack
	def __add__(self, data):
		self.total = self.total + 1
		for i in range(len(data.data)):
			self._val[i] = data.data[i] + self._val[i]
		return(self)

	#Compute the average of the current stacked array then insert it into the stack
	def avg(self):
		for i in range(len(self._val)):
			self._val[i] = self._val[i]/self.total
		self._stacked_arrays.append(self._val)
		return(self._stacked_arrays)

	#Publish all the stacked arrays one after the other
	def publish(self):
		global pub

		pub_arrays = Int32MultiArray()
	
		for i in self._stacked_arrays:
			pub_arrays.data = i
			pub.publish(pub_arrays)

		pub_arrays.data = [-1]
		pub.publish(pub_arrays)

	#Display the current stacked array
	def __repr__(self):
		print("-----------------------------")
		print(self._val)
		return("-----------------------------")

############################################################

def callback(data):
	global stack
	global vibrate
	global rt_mode

	global start
	global end
	global rt_mode_frequency

	learning_time = 100

	#If a record is active then stack "learning_time" _values into the current stack of the stack object
	if(stack.recording):
		if(stack.total < learning_time):
			stack = stack + data
			print(data.data)
		else:
			#At the end of the record, add the current stack to the stacked arrays
			print(stack.avg())
			vibrate.publish(1)
			stack.reset()
	#Real time mode
	elif(rt_mode):
		if(stack.total < rt_mode_frequency):
			stack = stack + data
		else:
			#At the end of the record, publish and restart
			stack.avg()
			stack.publish()
			stack.reset()
			stack.clear()

############################################################

def inputs(data):
	global stack
	global rt_mode
	global rt_mode_frequency

	#When the "send" input is catched, publish the all stacked arrays
	if(data.data == "send"):
		stack.publish()
		print("published")
		stack.clear()
	elif(data.data == "rt"):
		if(rt_mode):
		    rt_mode = False
		else:
		    rt_mode = True
	elif(data.data == "+"):
		rt_mode_frequency += 1
		print(rt_mode_frequency)
	elif(data.data == "-"):
		rt_mode_frequency = 1
		print(rt_mode_frequency)
	elif(data.data == "reset"):
		pass
	#When an empty message is catched, switch on the recording mode
	elif(data.data == ""):
		stack.recording = True

############################################################

def main():
	global stack
	global pub
	global vibrate
	global rt_mode
	global rt_mode_frequency
	
	rt_mode = False
	rt_mode_frequency = 1
	rospy.init_node('emg2avg', anonymous=True)
	rospy.Subscriber("/myo_raw/myo_emg", EmgArray, callback)
	rospy.Subscriber("input_cmd", String, inputs)
	pub = rospy.Publisher('chatter', Int32MultiArray, queue_size=10)
	vibrate = rospy.Publisher('/myo_raw/vibrate', UInt8, queue_size=1)
	stack = data_stack()

	rospy.spin()

if __name__ == '__main__':
	main()