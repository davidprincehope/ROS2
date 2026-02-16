cmake_minimum_required(VERSION 3.8)
project(this_is_a_really_long_node)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

add_executable(testing_node src/testing_node.cpp)   
ament_target_dependencies(testing_node rclcpp)

install(TARGETS
  testing_node
  DESTINATION lib/${PROJECT_NAME}
)
ament_package()