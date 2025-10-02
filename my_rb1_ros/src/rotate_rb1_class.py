#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import tf

class RotateRb1():
    
    def __init__(self):
        self.cmd_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.readOdom_callback)
        self.cmd = Twist()
        self.yaw = 0
        self.ctrl_c = False
        self.rate = rospy.Rate(1) #1hz
        rospy.on_shutdown(self.shutdownhook)

    def readOdom_callback(self, msg):
        #Cannot return values directly from callback. Therefore update the class property "angle" to store value
        (roll, pitch, yaw) = tf.transformations.euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
        self.yaw = yaw

    def publish_cmd_vel(self):
        while not self.ctrl_c:
            connections = self.cmd_publisher.get_num_connections()
            if connections > 0:
                self.cmd_publisher.publish(self.cmd)
                rospy.loginfo("Cmd Published")
                break
            else:
                self.rate.sleep()
        
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.stop()
        self.ctrl_c = True

    def rotate(self, degrees):
        radians = math.radians(degrees)
        desired_yaw = radians + self.yaw
        #print(f"Desired Yaw: {desired_yaw}")
        #print(f"Initial Self Yaw: {self.yaw}")

        if (radians > 0):
            self.cmd.angular.z = 0.2
            
            rospy.loginfo("Rotating Rb1")
            while not self.ctrl_c and self.yaw < desired_yaw:
                self.publish_cmd_vel()
                #print(f"Self Yaw: {self.yaw}")
                self.rate.sleep()
        elif (radians < 0):
            self.cmd.angular.z = -0.2
            
            rospy.loginfo("Rotating Rb1")
            while not self.ctrl_c and self.yaw > desired_yaw:
                self.publish_cmd_vel()
                #print(f"Self Yaw: {self.yaw}")
                self.rate.sleep()
            
        self.stop()

    def stop(self):
        rospy.loginfo("Stopping rb1")
        self.cmd.angular.z = 0.0
        self.publish_cmd_vel()