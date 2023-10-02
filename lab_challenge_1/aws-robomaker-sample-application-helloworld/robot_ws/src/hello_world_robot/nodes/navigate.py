#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time

class RobotController(object):
    '''A class that manages robot motion and ensures it stops on ROS shutdown.'''

    def __init__(self):
        '''Constructor initializes ROS node and robot movement.'''

        # Setting up the publisher and initializing the message.
        self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.msg = Twist()

        # Ensure the robot stops when ROS shuts down.
        rospy.on_shutdown(self.ensure_stop)

        # Kick off the robot movement.
        rospy.init_node('initiate_and_stop_robot')
        self.initiate_movement()
        rospy.spin()

    def publish(self, msg_type="move"):
        '''Waits for a publisher connection and sends the Twist message.'''

        while self.publisher.get_num_connections() < 1:
            # Pausing until a connection is made.
            rospy.loginfo("Awaiting publisher connection...")
            time.sleep(1)

        rospy.loginfo("Successfully connected to publisher.")

        rospy.loginfo("Dispatching %s message..." % msg_type)
        self.publisher.publish(self.msg)

    def initiate_movement(self):
        '''Initiates the robot's forward motion.'''

        self.msg.linear.x = 0.2
        self.publish()

        time.sleep(18) # The robot moves for a while before coming to a halt.

        rospy.signal_shutdown("Task completed!")

    def ensure_stop(self):
        '''Ensures the robot halts during a system shutdown.'''

        rospy.loginfo("System shutting down. Halting robot...")
        self.msg.linear.x = 0
        self.publish("stop")

if __name__ == '__main__':
    RobotController()
