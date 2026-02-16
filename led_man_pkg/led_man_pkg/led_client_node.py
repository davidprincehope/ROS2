#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_led_interfaces.srv import LedController
from rclpy.duration import Duration
from functools import partial

class BatteryStateClient(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("battery_node")  # MODIFY NAME
        self.client_ = self.create_client(LedController, "set_led")
        self.current_level_  = "full"
        self.timer = self.create_timer(1.0,self.callback_timer_battery_percentages) 
        self.start_time = self.get_current_time_seconds()

    def get_current_time_seconds(self): 
        time_now = self.get_clock().now()
        return time_now

    def set_led_state(self, state,led_number): 
        while not self.client_.wait_for_service(1.0): 
            self.get_logger().warn("waiting for set led server......")

        request = LedController.Request()
        request.state = state
        request.led_number = led_number 

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_led_states))


    def callback_led_states(self, future): 
        try:
            response = future.result()
            self.get_logger().info(response.message) 
            self.get_logger().info(f"Response success: {response.success}") 
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))

    def set_led_pattern(self,level):

        if level == "full":
            for led in (1,2,3): 
                self.set_led_state(False, led)
        elif level == "empty": 
            self.set_led_state(True,1)

    def callback_timer_battery_percentages(self): 
        now = self.get_current_time_seconds()

        if self.current_level_ == "full":
            elapsed = now-self.start_time
            if elapsed > Duration(seconds=4):
                self.current_level_ = "empty"
                self.set_led_pattern(self.current_level_)
                self.get_logger().info(f"Current Level : {self.current_level_}")
                self.start_time = now
                
        elif self.current_level_ == "empty": 
            elapsed = now-self.start_time
            if elapsed > Duration(seconds=6): 
                self.current_level_ = "full"
                self.set_led_pattern(self.current_level_)
                self.get_logger().info(f"Current Level : {self.current_level_}")
                self.start_time = now
                

def main(args=None):
    rclpy.init(args=args)
    node = BatteryStateClient()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()