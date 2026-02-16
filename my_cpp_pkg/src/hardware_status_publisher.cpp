    #include "rclcpp/rclcpp.hpp"
    #include "my_robot_interfaces/msg/hardware_status.hpp"


    class HardwareStatusPublisher : public rclcpp::Node // MODIFY NAME
    {
    private: 
        rclcpp::TimerBase::SharedPtr timer_ ;
        rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr publisher_;

    public:
        HardwareStatusPublisher() : Node("Hardware_Publisher") // MODIFY NAME
        {
            publisher_ = this->create_publisher<my_robot_interfaces::msg::HardwareStatus>("Hardware_Status_Publisher", 10); 
            RCLCPP_INFO(this->get_logger(), "The topic has started"); 
            timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&HardwareStatusPublisher::publisher_callback, this)); 
        }
     
    private:
        void publisher_callback(){ 
            auto msg = my_robot_interfaces::msg::HardwareStatus(); 

            msg.temprature = 52.7;
            msg.are_motors_ok = true;
            msg.debug_message = "Motors are too hot";

            publisher_->publish(msg);
        }
        
    };



     
    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<HardwareStatusPublisher>(); // MODIFY NAME
        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
    }