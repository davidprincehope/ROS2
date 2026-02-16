    #include <rclcpp/rclcpp.hpp>
    #include "example_interfaces/msg/int64.hpp"

    class Number_publisher : public rclcpp::Node // MODIFY NAME
    {
    private:
        rclcpp::TimerBase::SharedPtr timer_ ;
        rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
        int number_; 
        
    public:
        Number_publisher() : Node("number_publisher")
        {
            this->declare_parameter("number", 2); 
            this->declare_parameter("timer_frequency", 1.0); 
            number_ = this->get_parameter("number").as_int();
            double timer_frequency= this->get_parameter("timer_frequency").as_double();

            publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number_publisher", 10); 
            RCLCPP_INFO(this->get_logger(), "The topic has started"); 
            timer_ = this->create_wall_timer(std::chrono::duration<double>(timer_frequency), std::bind(&Number_publisher::publisher_callback, this)); 
        }
     
    private:
        void publisher_callback(){ 
            auto msg = example_interfaces::msg::Int64(); 
            msg.data = number_;
            publisher_->publish(msg);
        }
    };
     
    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<Number_publisher>(); // MODIFY NAME
        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
    }