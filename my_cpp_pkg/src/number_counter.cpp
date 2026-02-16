    #include "rclcpp/rclcpp.hpp"
    #include "example_interfaces/msg/int64.hpp"
    #include "example_interfaces/srv/set_bool.hpp"
     
    class Number_counter : public rclcpp::Node // MODIFY NAME
    {
    private:
        std::int64_t counter_ ; 
        rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscriber_;
        rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_; 
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Service<example_interfaces::srv::SetBool>::SharedPtr server_ ; 
    public:
        Number_counter() : Node("Number_counter"), counter_(0)
        {
            RCLCPP_INFO(this->get_logger(), "This is the node to count the numbers and also publish "); 
            subscriber_ = this->create_subscription<example_interfaces::msg::Int64>("number_publisher", 10, std::bind(&Number_counter::subscriber_callback,this, std::placeholders::_1));
            publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number_count", 10); 
            timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&Number_counter::publisher_callback, this));

            server_ = this->create_service<example_interfaces::srv::SetBool>("reset_counter", std::bind(&Number_counter::callback_reset_counter, this, std::placeholders::_1, std::placeholders::_2));
            RCLCPP_INFO(this->get_logger(), "Send true to reset_counter service tio reset the counter" );
        }
    private: 
        void subscriber_callback(const example_interfaces::msg::Int64::SharedPtr msg){ 
            RCLCPP_INFO(this->get_logger(), "Received: %ld", msg->data);
            counter_ ++ ;  
        }
        void publisher_callback(){ 
            auto msg = example_interfaces::msg::Int64();
            msg.data = counter_; 
            publisher_->publish(msg);
            RCLCPP_INFO(this->get_logger(), "Current count: %ld", counter_); 
        }

        void callback_reset_counter(const example_interfaces::srv::SetBool::Request::SharedPtr request, 
        const example_interfaces::srv::SetBool::Response::SharedPtr response){
            bool boolean = request->data; 
            if(!boolean){
                counter_ = 0; 
                RCLCPP_INFO(this->get_logger(), "Counter reset to zero"); 
                response->success;
            }else { 
                RCLCPP_INFO(this->get_logger(), "Counter continues"); 
                response->success;
            }

        }
        
    };
     
    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<Number_counter>(); // MODIFY NAME
        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
    }