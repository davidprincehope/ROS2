    #include "rclcpp/rclcpp.hpp"
    #include "example_interfaces/srv/add_two_ints.hpp"
     
    class AddTwoIntsClientNode : public rclcpp::Node 
    {
    private: 
        rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_ ; 
    public:
        AddTwoIntsClientNode() : Node("add_two_ints_client") 
        {
           client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_inits");
        }
        void callAddTwoInts(int a, int b) { 
            while(!client_->wait_for_service(std::chrono::seconds(1))){
                RCLCPP_WARN(this->get_logger(), "Waiting for the server"); 
            }
            auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
            request->a = a; 
            request->b  = b;

            client_->async_send_request(request,std::bind(&AddTwoIntsClientNode::callbackCallAddTwoInts, this, std::placeholders::_1));
        }

    private:
        void callbackCallAddTwoInts(rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future){ 
            auto response = future.get();
            RCLCPP_INFO(this->get_logger(), "Sum: %d",(int)response->sum); 
        }
    };
     
    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<AddTwoIntsClientNode>(); // MODIFY NAME
        node->callAddTwoInts(10,5); 
        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
    }