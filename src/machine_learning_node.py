#!/usr/bin/env python
#ROS
import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String
from std_msgs.msg import Int8

import numpy

####################################################################
#Manages the machine learning system
class datas:
    _datasets = []
    _datasets_copy = []
    _last_data = []
    _record = True
    modif_range = 300
    _auto_learn = False
    _rt_mode = False

    def __init__(self, modif_r, auto_learn):
        self.reset()
        self.modif_range = modif_r
        self._auto_learn = auto_learn

    #Reset all the datasets
    def reset(self):
        self._datasets = []
        self._datasets_copy = []
        self._last_data = []
        self._record = True


    #Insert a new data from the raw2avg node into the datasets array.
    #Handle the end of the record.
    def __add__(self, data):
        if(self._record and data.data[0] != -1):
            self._datasets.append(data.data)
        elif(self._record and data.data[0] == -1):
            self._record = False
            self._datasets_copy = list(self._datasets)
            print(str(len(self._datasets)) + " datasets catched")
        elif(self._record == False and data.data[0] != -1):
            self._last_data = data.data
            if(not self._rt_mode):
                print("new values to analyse -> " + str(self._last_data))
            self.predict(data)
        return(self)

    #Find the minimum comparison score
    def _find_min(self, comp_scores):
        return(comp_scores.index(min(comp_scores)))

    #Pick and display the best comparison score
    def _display_result(self, comp_scores, minimum):
        global pub
        
        if(self._rt_mode):
            pub.publish(minimum)
        else:
            print("machine learning match scores ->")
            print(comp_scores)
            print("machine learning best match ->")
            print(minimum)

    #Update the database with the new value
    #The weight of the modification depends on the comparison score
    def _update_datasets(self, minimum, comp_scores):
        if(comp_scores[minimum] <= self.modif_range):
            i = 0
            new_datasets = []
            modif_weight = float(comp_scores[minimum]) / float(self.modif_range)
            for row in self._last_data:
                new_datasets.append(int((float(row) * (1.0 - modif_weight)) + (float(self._datasets[minimum][i]) * (modif_weight))))
                i += 1
            return(new_datasets)
        else:
            return(self._datasets[minimum])

    #Compute all the matching scores between the datasets and the unknown value
    def predict(self, data):
        comp_scores = []
        i = 0
        if(not self._record):
            for ds in self._datasets:
                n = 0
                for value in ds:
                    if(n == 0):
                        comp_scores.append(abs(value - self._last_data[n]))
                    else:
                        comp_scores[i] += abs(value - self._last_data[n])
                    n += 1
                i += 1
            minimum = self._find_min(comp_scores)
            self._display_result(comp_scores, minimum)
            if(self._auto_learn):
                self._datasets[minimum] = self._update_datasets(minimum, comp_scores)

    #Reset the default datasets
    def forget(self):
        print(self)
        self._datasets = self._datasets_copy

    #When the print function is called on the object
    def __repr__(self):
        print("old --> " + str(self._datasets))
        print("---------------------------------------------")
        print("new --> " + str(self._datasets_copy))
        return("---------------------------------------------")

    #Switch on/off the autolearn mode
    def switch_auto_learn(self):
        if(self._auto_learn):
            print("auto learn mode : OFF")
            self._auto_learn = False
        else:
            print("auto learn mode : ON")
            self._auto_learn = True

    #Switch on/off the real time mode
    def switch_real_time(self):
        if(self._rt_mode):
            print("real time mode : OFF")
            self._rt_mode = False
        else:
            print("real time mode : ON")
            self._rt_mode = True

####################################################################

def inputs(data):
    global datas

    if(data.data == "reset"):
        datas.reset()
    elif(data.data == "rt"):
        datas.switch_real_time()
    elif(data.data == "al"):
        datas.switch_auto_learn()
    elif(data.data == "forget"):
        datas.forget()
    elif(data.data == "display"):
        print(datas)

####################################################################

def callback(data):
    global datas

    datas = datas + data

####################################################################

def listener():
    global datas
    global pub

    datas = datas(300, False)
    rospy.init_node('machine_learning_node', anonymous=True)
    rospy.Subscriber("chatter", Int32MultiArray, callback)
    rospy.Subscriber("input_cmd", String, inputs)
    pub = rospy.Publisher('rt_cmd', Int8, queue_size=10)
    rospy.spin()

####################################################################
if __name__ == '__main__':
    listener()