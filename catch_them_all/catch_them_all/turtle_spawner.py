import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from my_robot_interfaces.msg import NameOrientation
import random 
import math 

class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.client_ = self.create_client(Spawn, "/spawn")
        self.timer = self.create_timer(0.5,self.timer_callback)
        self.turtle_count = 1
        self.turtle_name_array = []
        self.publisher_ = self.create_publisher(NameOrientation, "Name_and_Orientation", 10)


    def timer_callback(self):
        self.spawn_call_function()

    def kill_callback(self): 
        pass

    def spawn_call_function(self): 
        while not self.client_.wait_for_service(1.0): 
            self.get_logger().warn("waiting for spawn server")

        self.turtle_count += 1 
        request = Spawn.Request()

        rand_name = f"turtle{self.turtle_count}"
        rand_theta = random.randint(0,360) * math.pi / 180
        rand_x = random.uniform(0.0,10.0)
        rand_y = random.uniform(0.0,10.0)


        request.theta = rand_theta
        request.x = rand_x
        request.y = rand_y
        request.name = rand_name


        msg = NameOrientation()

        msg.random_theta = rand_theta
        msg.random_x = rand_x 
        msg.random_y = rand_y 
        msg.turtle_name = f"turtle{self.turtle_count}"

        self.publisher_.publish(msg)
        self.get_logger().info("message Published")

        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_spawn)

    def callback_spawn(self, future): 
        response = future.result()
        self.get_logger().info(f"Turtle_name: {response}")
    
def main(args= None): 
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__": 
    main()