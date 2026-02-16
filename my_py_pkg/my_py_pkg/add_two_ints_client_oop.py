#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial

class AddTwoIntsClient(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("add_two_ints_client_oop")  # MODIFY NAME
        self.client_ = self.create_client(AddTwoInts, "add_two_inits")

    def call_add_two_ints(self,a,b): 
        while not self.client_.wait_for_service(1.0): 
            self.get_logger().warn("waiting for add two ints server......")

        request = AddTwoInts.Request()
        request.a = 3
        request.b = 8 

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_add_two_ints, request = request))
        
    def callback_call_add_two_ints(self, future, request): 
        response = future.result() 
        self.get_logger().info("Got Response: " + str(response.sum))
        self.get_logger().info(str(request.a) + "+" + str(request.b) + " = " + str(response.sum))



def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClient()  
    node.call_add_two_ints(2,7)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()