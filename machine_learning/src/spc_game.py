#!/usr/bin/env python
#ROS
import rospy
import random
from std_msgs.msg import Int8
from std_msgs.msg import String

############################################################
#This object manages the spc game
class spc:
    #Number of identical predictions in a row for a gesture to be detected
    gesture_detect_threshold = 0
    game_on = False
    _scores = [0, 0]
    _last_gesture = -1
    _same_gestures_in_a_row = 0

    def __init__(self, gesture_detect_threshold):
        self.gesture_detect_threshold = gesture_detect_threshold

    #Reset the scores
    def reset(self):
        self._scores = [0, 0]

    #Wait for a gesture to be detected
    def wait_for_gesture(self, gesture):
        if(gesture != 0 and gesture == self._last_gesture):
            self._same_gestures_in_a_row += 1
        else:
            self._same_gestures_in_a_row = 1
            self._last_gesture = gesture

        if(self._same_gestures_in_a_row >= self.gesture_detect_threshold):
            return(True)
        else:
            return(False)

    def console_line(self):
        print("-----------------------")

    #Display the scores
    def display_scores(self):
        print("SCORES : player => " + str(self._scores[0]) + "| computer => " + str(self._scores[1]))

    #Display the computer gesture
    def display_computer_gesture(self, gesture):
        if(gesture == 1):
            self.console_line()
            print("stone")
            self.console_line()
        elif(gesture == 2):
            self.console_line()
            print("paper")
            self.console_line()
        else:
            self.console_line()
            print("scissors")
            self.console_line()

    #Play a round
    def play_round(self):
        computer_gesture = random.randint(1, 3)
        self.display_computer_gesture(computer_gesture)

        if(computer_gesture == self._last_gesture):
            print("DRAW")
        elif((computer_gesture == 1 and self._last_gesture == 2) or (computer_gesture == 2 and self._last_gesture == 3) or (computer_gesture == 3 and self._last_gesture == 1)):
            print("HUMAN WINS")
            self._scores[0] += 1
        else:
            print("COMPUTER WINS")
            self._scores[1] += 1

        self.display_scores()
        self._same_gestures_in_a_row = 0

####################################################################

def callback(data):
    global spc

    if(spc.wait_for_gesture(data.data) and spc.game_on):
        spc.play_round()

####################################################################

def inputs(data):
    global spc

    if(data.data == "spc"):
        if(spc.game_on == False):
            spc.game_on = True
            print("spc game ON")
        else:
            spc.game_on = False
            print("spc game OFF")
    elif(data.data == "spc-reset"):
        spc.reset()
        print("new game")

####################################################################

def listener():
    global spc
    spc = spc(25)

    rospy.init_node('graphs', anonymous=True)
    rospy.Subscriber("input_cmd", String, inputs)
    rospy.Subscriber("rt_cmd", Int8, callback)
    rospy.spin()

####################################################################
if __name__ == '__main__':
    listener()