#!/usr/bin/env python3

# importing necessary libraries
import rospy
from std_msgs.msg import String

#Callback Function to assign the message recieved from Node1 in the global variable
def callback_node1(data):
    global data_node1  #Setting it global so that it is accessible from other functions as well
    data_node1 = data.data

#Callback Function to append the 2 messages from the 2 nodes, and print it.
def callback_node2(data):
    data_node2 = data.data
    final = data_node1 + data_node2  # Appending the 2 messages
    print(final)
    
#Function to listen to the messages by subscribing the corresponding nodes
def listener():
    print(">>> Listening:")
    rospy.init_node('node3', anonymous=True)  # initializing node node3 as unique(using anonymous=True)
    rospy.Subscriber('/team_abhiyaan', String, callback_node1)  # initializing the subscriber, to topic '/team_abhiyaan' to get the message from node1 and call the function callback_node1
    rospy.Subscriber('/autonomy', String, callback_node2) # initializing the subscriber, to topic '/autonomy' to get the message from node2 and call the function callback_node2
    rospy.spin()  # wait till user terminates the execution


if __name__ == "__main__":
    listener()
    
    
    

    
