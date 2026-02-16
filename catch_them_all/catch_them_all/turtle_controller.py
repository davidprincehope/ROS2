from my_robot_interfaces.msg import NameOrientation
from turtlesim.msg import Pose
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math 
from turtlesim.srv import Kill

class TurtleController(Node): 
    def __init__(self): 
        super().__init__("turtle_controller_node")
        self.new_turtle_subscriber_ = self.create_subscription(NameOrientation, "Name_and_Orientation",self.new_turtles_callback, 10)
        self.turtle1_pos_subs_ = self.create_subscription(Pose, "/turtle1/pose", self.turtle1_pos_callback, 10)
        self.turtle1_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.turtle1_vel_timer_ = self.create_timer(0.1, self.pid_turtle_kill)
        self.kill_client_ = self.create_client(Kill, "/kill")

        self.dist_tolerance = 0.2
        self.theta_tolerance = 0.3
        self.dt = 0.1


        self.integral_dist = 0.0 
        self.integral_theta = 0.0

        self.derivative_dist = 0.0
        self.derivative_theta = 0.0

        self.prev_theta_error = 0.0 
        self.prev_dist_error = 0.0 

        self.kp_dist= 5.1
        self.ki_dist = 0.01
        self.kd_dist = 0.008

        self.kp_theta = 8.0
        self.ki_theta = 0.001
        self.kd_theta = 0.04

        self.current_target_index_ = 0

        self.turtle_name_and_orietation_dictionary = {}
        self.turtle1_pos_ = None 

        # self.spawned_turtle_number 

    def turtle1_pos_callback(self, msg:Pose):
        
        self.turtle1_pos_ = [msg.x,msg.y,msg.theta,msg.linear_velocity,msg.angular_velocity]

    def new_turtles_callback(self, msg:NameOrientation):

        theta = msg.random_theta
        y_position = msg.random_y
        turtle_name = msg.turtle_name
        x_position = msg.random_x

        self.turtle_name_and_orietation_dictionary[turtle_name] = [x_position,y_position,theta]
        self.get_logger().info(f"Turtle_name: {turtle_name} ,Turtle_X_position: {self.turtle_name_and_orietation_dictionary[turtle_name][1]}, Turtle_y_position: {self.turtle_name_and_orietation_dictionary[turtle_name][0]}, Turtle_theta_position: {self.turtle_name_and_orietation_dictionary[turtle_name][2]}")

    def pid_turtle_kill(self): 
        msg = Twist()
        request = Kill.Request()
    
        if self.turtle1_pos_ is None: 
            return 
        if len(self.turtle_name_and_orietation_dictionary) == 0: 
            return
        
        turtle_list = list(self.turtle_name_and_orietation_dictionary.items())
        if self.current_target_index_ >= len(turtle_list):
            return 
        
        turle_name, turtle_orientation = turtle_list[self.current_target_index_]
        x_dist = turtle_orientation[0] - self.turtle1_pos_[0]
        y_dist = turtle_orientation[1] - self.turtle1_pos_[1]

        distance = (x_dist**2 + y_dist**2)**0.5
        goal_theta = math.atan2(y_dist, x_dist)
        theta_error = goal_theta - self.turtle1_pos_[2]


        while theta_error > math.pi: 
            theta_error -= 2 * math.pi
        while theta_error < -math.pi: 
            theta_error += 2 * math.pi

        
        if abs(distance) < self.dist_tolerance and abs(theta_error) < self.theta_tolerance:

            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.integral_dist = 0 
            self.integral_theta = 0 
            request.name = turle_name
            future = self.kill_client_.call_async(request)
            future.add_done_callback(self.kill_callback)
            

            self.current_target_index_ += 1 
        else:

            self.integral_theta += theta_error * self.dt
            derivative_theta = (theta_error - self.prev_theta_error) / self.dt
            u_theta = (
                self.kp_theta * theta_error
                + self.ki_theta * self.integral_theta
                + self.kd_theta * derivative_theta
            )

            if abs(theta_error) < self.theta_tolerance:
                self.integral_dist += distance * self.dt
                derivative_dist = (distance - self.prev_dist_error) / self.dt
                u_dist = (
                    self.kp_dist * distance
                    + self.ki_dist * self.integral_dist
                    + self.kd_dist * derivative_dist
                )
            else:
                u_dist = 0.0  


            msg.linear.x = float(u_dist)
            msg.angular.z = float(u_theta)

        self.get_logger().info(
            f"turtle_name:{turle_name} distance to goal : {distance:.3f}, angular difference : {theta_error:.3f}"
        )


        self.prev_dist_error = distance
        self.prev_theta_error = theta_error


        self.turtle1_vel_pub_.publish(msg)

    def kill_callback(self, future): 
        response = future.result()
        self.get_logger().info(f"Turtle {response} has been sucessfully excommunicated")

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__": 
    main()