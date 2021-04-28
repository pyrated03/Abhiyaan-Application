#!/usr/bin/env python3

# importing necesary modules
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow
from threading import Thread


# CONSTANTS
DIST_TOLERANCE = 2.0  # for stopping turtle when it reaches the desired zone


# just an infinite loop to keep program running
def mainloop():
    while True:
        pass


class TurtleBot:
    def __init__(self):
        # Creates a node with name 'maneuver_problem' and make sure it is a unique node (using anonymous=True).
        rospy.init_node('maneuver_problem', anonymous=True)
        # to publish to turtle2 to move
        self.velocity_publisher = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
        # subscribe to topic for getting own position and calling function to update own position
        self.pose_subscriber = rospy.Subscriber('/turtle2/pose', Pose, self.update_pose)
        # subscribe to topic to acquire target position(turtle1) and calling function to move towards goal
        self.target_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.Overtake)
        # pose object for own position
        self.pose = Pose()
        self.rate = rospy.Rate(10)  

    # function to update it's postion
    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    # function to conpute the euclidean distance between self and target(ie between turtle2 and turtle1)
    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))
    #callback function to assign the linear velocity. As the turtle approaches the target, it slows down(since vel = const*distance, as distance decreases, velocity decreases.) 
    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)


    # function to move towards target
    def Overtake(self, data):
        self.target_subscriber.unregister()
        goal_pose = Pose()

        goal_pose.x = round(data.x, 4)
        goal_pose.y = round(data.y, 4)

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= DIST_TOLERANCE:
            vel_msg.linear.x = self.linear_vel(goal_pose)     #First, moving horizontally in x-direction till it reaches desired zone
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()	
	
        # stop when turtle reaches desired zone
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.z = 1.0    # Turning turtle2 by 1 radian anticlockwise, so that the turtle is oriented towards the new goal
        self.velocity_publisher.publish(vel_msg)

        #Now, we define a new goal, towards which the turtle shall travel. This is defined to be 4 units above and 2 units behind turtle2(This will somewhat be in line with the current location)
        goal_pose_new = Pose()
        goal_pose_new = goal_pose
	    goal_pose_new.x = goal_pose.x - 2.0
        goal_pose_new.y = goal_pose.y + 4.0
        
        #Repeating the above performed loop, but now, towards the new goal(goal_pose_new).
        while self.euclidean_distance(goal_pose_new) >= DIST_TOLERANCE:
            vel_msg.linear.x = 0
            vel_msg.linear.y = self.linear_vel(goal_pose_new)
            vel_msg.linear.z = 0
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()

        # stop when turtle reaches desired zone
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.z = -1.0  # Turning turtle2 by 1 radian clockwise , so that the turtle is oriented towards the final goal
        self.velocity_publisher.publish(vel_msg)

        #Once again, we are shifting the goal towards which the turtle shall move. This is set to be 6 units ahead of the current goal.(which is 4 units ahead, and 4 units above the first target, ie location of turtle 1)   
        goal_pose_final = Pose()
        goal_pose_final = goal_pose_new
        goal_pose_final.x = goal_pose_new.x + 6.0
            
        #Yet again we repeat the loop performed above, but this time towards the final goal(goal_pose_final).
        while self.euclidean_distance(goal_pose_final) >= DIST_TOLERANCE:
            vel_msg.linear.x = self.linear_vel(goal_pose_final)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        
        #Once we reach within a the desired zone(2 units from goal_pose_final) we stop the turtle completely. Hence the turtle2 stops at a safe distance from turtle1
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

        
if __name__ == '__main__':
    try:
        x = TurtleBot()
        t = Thread(target=mainloop)  # thread to keep program running
        t.daemon = True
        t.start()
        t.join()
    except Exception as e:
        print("ERROR : ", e)
        pass
