#!/usr/bin/env python3

# importing necessary modules
import rospy
from std_msgs.msg import String


def talker():
    print("Publishing:")
    pub = rospy.Publisher('/team_abhiyaan', String, queue_size=10)  # initialising the publisher with topic, dtype and queue size
    rospy.init_node('Node1', anonymous=True)  # initialising node and make it unique(using anonymous=True)
    rate = rospy.Rate(10)  # The value 10 corrsponds to 10Hz, i.e. publish message 10 times a second

    #In the below loop, while the rospy is not shutdown, we publish the message in the topic, 10 times a second
    while not rospy.is_shutdown():
        message = "Team Abhiyaan:"
        # rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()


if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
