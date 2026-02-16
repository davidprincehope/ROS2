#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String 
 
class radio(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("radio_topic") # MODIFY NAME
        self._publisher= self.create_publisher(String, "mr_topic", 10) 
        self.timer = self.create_timer(0.5,self.timer_callback) 
        self.get_logger().info("Robot new station has been started")

    def timer_callback(self):
        msg = String()
        msg.data = "Hello"
        self._publisher.publish(msg=msg)
 

def main(args=None):
    rclpy.init(args=args)
    node = radio() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":  
    main()  