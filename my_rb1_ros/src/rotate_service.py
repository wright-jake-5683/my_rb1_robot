#! /usr/bin/env python

import rospy
from my_rb1_ros.srv import Rotate, RotateResponse
from rotate_rb1_class import RotateRb1
import tf

def my_callback(request):
    rospy.loginfo("The Service /rotate_robot has been requested")
    rotate_object.rotate(request.degrees)

    rospy.loginfo("Finished service request for /rotate_robot")
    response = RotateResponse()
    response.result = f"Service completed. Rb1 has rotated {request.degrees}"
    return response


rospy.init_node('rotate_rb1_server') 
my_service = rospy.Service('/rotate_robot', Rotate , my_callback)
rotate_object = RotateRb1()
rospy.loginfo("Service /rotate_robot Ready")
rospy.spin() # keep the service open.