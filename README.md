The following tutorial assumes that you are using the Melodic ROS version.

STEPS TO FOLLOW:
1-Download and install both packages in your catkin workspace.

2-Use the "$ catkin_make" command to build your workspace.

3-Run "$ roscore".

4-In a new tab, run the following command "$ rosrun ros_myo myo-rawNode.py" to launch the Myo raw data reciever node. If you are using a VM, you may have a port permission issue, then use "$ sudo chmod 777 /dev/ttyACM0" to fix it.

5-In a new tab, launch all the gesture recognition system's core nodes using the command "$ roslaunch machine_learning machine_learning.launch". You will then be able to enter all the gesture recognition system's commands in this tab.

6-Now, you can either run the robot control node using "$ rosrun machine_learning rt2turtle.py" if you want to control a robot (you will probably have to modify this node to adapt it to the robot you want to control with. It is configured to publish twist messages into the "cmd_vel" topic by default so you can try it with the turtlesim provided by the ROS beginner tutorial) or simply launch the stone-paper-scissors game included in this package to test the system runing the command "$ rosrun machine_learning spc_game.py" (the informations related to the game will be displayed in this tab/terminal).

COMMANDS LIST:
All the following commands have to be used in the terminal/tab opened in step 5.

"" : Tell the "emg2avg" node to start recording a gesture. It will add this gesture to the
gestures stack.

"send" : Send the gestures stack from the "emg2avg" node to the "machine_learning_node".

"reset" : Reinitialize the database and restart the training phase.

"rt" : Switch on/off the real time mode. When this mode is running the "machine_learning_node"
will automatically generate values at a frequency given by the user.

"al" : Switch on/off the auto-learn mode. When this mode is running at the same time
than the real time mode it will unlock the database modifications (for more information,
please see 1.3.3).

"forget" : Remove the modifications from the auto-learn system and restore the first
database.

"display" : Display the current state of the database.

"spc" : Turn on/off the stone-paper-scissors game.
