    #include <rclcpp/rclcpp.hpp>
    #include "example_interfaces/msg/string.hpp"

    class smartphone : public rclcpp::Node // MODIFY NAME
    {
    private:
        rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;
    
    public:
        smartphone() : Node("node_name")// MODIFY NAME
        {
            RCLCPP_INFO(this->get_logger(), " The subscriber has started"); 
            subscriber_ = this->create_subscription<example_interfaces::msg::String>("robot_news",10, std::bind(&smartphone::callbackRobotNews,this, std::placeholders::_1));
    
        }
     
    private:
        void callbackRobotNews(const example_interfaces::msg::String::SharedPtr msg){
            RCLCPP_INFO(this->get_logger(), "%s", msg->data.c_str()); 
        }

    };
     
    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<smartphone>(); // MODIFY NAME
        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
    }