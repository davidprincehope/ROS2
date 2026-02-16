#include <iostream>
#include "rclcpp/rclcpp.hpp"

class testing_node: public rclcpp::Node
{
private:

public:
    testing_node(): Node("this_is_a_rlly_long_node")
    {
        RCLCPP_INFO(this->get_logger(), "Class Instantiated Successfully");
    }

};



int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<testing_node>();
    RCLCPP_INFO(node->get_logger(), "Testing Node has been started.");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}