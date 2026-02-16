#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoInitsServerNode(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("add_two_inits_server")  # MODIFY NAME
        self.server_ = self.create_service(AddTwoInts, "add_two_inits",self.callback_add_two_init)
        self.get_logger().info("Add Two Ints Server has been started. ")

    def callback_add_two_init(self, request: AddTwoInts.Request, response: AddTwoInts.Response):
        response.sum = request.a + request.b 
        self.get_logger().info(str(request.a) + "+" + str(request.b) + " = " + str(response.sum))
        return response 


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoInitsServerNode()  # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()