    #include "rclcpp/rclcpp.hpp"
    #include "example_interfaces/srv/set_bool.hpp"
     
    class ResetCounter: public rclcpp::Node // MODIFY NAME
    {
   
    private:
        rclcpp::Client<example_interfaces::srv::SetBool>::SharedPtr client_ ; 

    public:
        ResetCounter() : Node("reset counter client ") 
        {
           client_ = this->create_client<example_interfaces::srv::SetBool>("set_bool");

        }
        void callSetState(bool bool_data) {
            while(!client_->wait_for_service(std::chrono::seconds(1))){
                RCLCPP_WARN(this->get_logger(), "Waiting for the server"); 
            }
            auto request = std::make_shared<example_interfaces::srv::SetBool::Request>();
            request->data = bool_data ; 
            client_->async_send_request(request,std::bind(&ResetCounter::callbackResetCounter, this, std::placeholders::_1));
        }
    private:
        void callbackResetCounter(rclcpp::Client<example_interfaces::srv::SetBool>::SharedFuture future){ 
            auto response = future.get();
            response->success;
            RCLCPP_INFO(this->get_logger(), "Service Complete"); 
        }


    };
     
     
    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<ResetCounter>(); // MODIFY NAME
        node->callSetState(true); 
        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
    }