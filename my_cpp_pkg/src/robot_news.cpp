    #include "example_interfaces/msg/string.hpp"
    #include "rclcpp/rclcpp.hpp"

    class Robotnews : public rclcpp::Node // MODIFY NAME
    {
    private: 
        std::string robot_name_;
        rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_; 

    public:
        Robotnews() : Node("radio_publisher"), robot_name_("daug")
        {
            this->declare_parameter("robot_name", "daug");
            robot_name_ = this->get_parameter("robot_name").as_string(); 
            
            publisher_ = this->create_publisher<example_interfaces::msg::String>("robot_news", 10); 
            RCLCPP_INFO(this->get_logger(), "This topic as started"); 
            timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&Robotnews::publishednews,this));
        }
     
    private:
        void publishednews() {
            auto msg = example_interfaces::msg::String(); 
            msg.data = std::string("Hi this is ") + robot_name_ + std::string("from the robot news station"); 
            publisher_->publish(msg); 
        }
    };
     
    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<Robotnews>(); 
        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
    }