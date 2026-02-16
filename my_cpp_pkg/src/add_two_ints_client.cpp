    #include "rclcpp/rclcpp.hpp"
    #include "example_interfaces/srv/add_two_ints.hpp"

    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<rclcpp::Node>("add_two_ints_client_no_oop"); // MODIFY NAME

        auto client = node->create_client<example_interfaces::srv::AddTwoInts>("add_two_inits");
        
        while(!client->wait_for_service(std::chrono::seconds(1))){
            RCLCPP_WARN(node->get_logger(), "waiting for server....");
        }

        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = 6; 
        request->b  = 2; 
        auto future = client->async_send_request(request); 
        rclcpp::spin_until_future_complete(node, future); 

        auto response = future.get(); 
        RCLCPP_INFO(node->get_logger(), "%d + %d +%d", (int)request->a,(int)request->b, (int)response->sum);



        rclcpp::shutdown();
        return 0;
    }