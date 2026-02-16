#!/usr/bin/env python3 

import rclpy 
from rclpy.node import Node
from my_led_interfaces.msg import LedStatus
from my_led_interfaces.srv import LedController 


# Led panel node should have a publisher and also a service 

class LedPanelNode(Node): 
    def __init__(self):
        super().__init__("led_panel_node")
        self.counter_ = 0 
        self.get_logger().info("This is the node to set the state of the 3 LEDs")
        self.server_ = self.create_service(LedController, "set_led", self.callback_set_led)
        self.led_status_pub_ = self.create_publisher(LedStatus, "led_panel_state", 10)
        self.create_timer(1.0, self.callback_publish_panel_state)
        self.led_msg = LedStatus()

    def callback_publish_panel_state(self):
        msg = self.led_msg
        self.led_status_pub_.publish(msg=msg)
        self.get_logger().info(f"Led1_ON :{msg.led_one_state}, Led2_ON :{msg.led_two_state}, LED3_ON :{msg.led_three_state}")

    def callback_set_led(self, request: LedController.Request,response: LedController.Response):
        
        msg = self.led_msg 

        if request.led_number == 1:
            msg.led_one_state = request.state
        elif request.led_number == 2:
            msg.led_two_state = request.state
        elif request.led_number == 3:
            msg.led_three_state = request.state
        else:
            self.get_logger().warn("Invalid LED number")
            response.success = False
            response.message = "Not Successful"
            return response
        
        self.get_logger().info(f"Set LED {request.led_number} to state {request.state}")
        response.success = True
        response.message = "Successful"
        return response

def main(args=None): 
    rclpy.init(args=args)
    node = LedPanelNode()
    rclpy.spin(node=node)
    rclpy.shutdown()


if __name__ == "__main__": 
    main()
    
