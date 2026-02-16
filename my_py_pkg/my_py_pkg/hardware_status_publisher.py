#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus


class HardwareStatusPublisherNode(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("Hardware_status_publisher") 
        self.hw_status_pub_ = self.create_publisher(HardwareStatus, "Hardware_status", 10)
        self.timer_ = self.create_timer(1.0, self.publish_hw_status) 
        self.get_logger().info("HW status has been published")

    def publish_hw_status (self): 
        msg = HardwareStatus()
        msg.temprature = 43.7 
        msg.are_motors_ok = True
        msg.debug_message = "Nothing special"
        self.hw_status_pub_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisherNode()  # MODIFY NAME
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()