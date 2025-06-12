// #include <geometry_msgs/msg/pose_stamped.hpp>
// #include <moveit_msgs/msg/planning_scene.hpp>
// #include <moveit/planning_interface/planning_interface.hpp>
// #include <moveit/move_group_interface/move_group_interface.hpp>
// #include <rclcpp/rclcpp.hpp>
// #include <shape_msgs/msg/plane.hpp>
// #include <arm_description/srv/go_to_pose.hpp>

// class GoToPoseServiceNode : public rclcpp::Node {
// private:
//     std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_;
//     rclcpp::Service<arm_description::srv::GoToPose>::SharedPtr service_;
//     rclcpp::Publisher<moveit_msgs::msg::PlanningScene>::SharedPtr planning_scene_publisher_;
//     bool initialized_;

//     bool is_pose_reachable(const geometry_msgs::msg::Pose& pose) {
//         double distance = std::sqrt(
//             std::pow(pose.position.x, 2) +
//             std::pow(pose.position.y, 2) +
//             std::pow(pose.position.z, 2)
//         );
//         return (distance <= 0.3) && (pose.position.z > 0.1);
//     }

//     void update_planning_scene() {
//     moveit_msgs::msg::PlanningScene planning_scene;
//     planning_scene.robot_state.joint_state.header.stamp = this->now();
//     planning_scene.world.collision_objects.clear();
//     moveit_msgs::msg::CollisionObject ground;
//     ground.header.frame_id = "base_link";
//     ground.header.stamp = this->now();
//     ground.id = "ground";
//     shape_msgs::msg::Plane plane;
//     plane.coef = {0.0, 0.0, 1.0, 0.05}; // Plane at z = -0.05
//     ground.planes.push_back(plane);
//     geometry_msgs::msg::Pose pose;
//     pose.orientation.w = 1.0;
//     ground.plane_poses.push_back(pose);
//     planning_scene.world.collision_objects.push_back(ground);
//     planning_scene.is_diff = true;
//     planning_scene_publisher_->publish(planning_scene);
// }

//     void GoToPose_callback(
//     const std::shared_ptr<arm_description::srv::GoToPose::Request> request,
//     std::shared_ptr<arm_description::srv::GoToPose::Response> response) {
    
//     if (!initialized_) {
//         response->success = false;
//         response->message = "Node not fully initialized";
//         RCLCPP_ERROR(this->get_logger(), "Service called before initialization complete");
//         return;
//     }

//     RCLCPP_INFO(this->get_logger(), "Received GoToPose request");
//     RCLCPP_INFO(this->get_logger(), "Target position: [%.3f, %.3f, %.3f]",
//                 request->target_pose.position.x,
//                 request->target_pose.position.y,
//                 request->target_pose.position.z);

//     // Create pose with guaranteed valid orientation
//     geometry_msgs::msg::PoseStamped target_pose_stamped;
//     target_pose_stamped.header.frame_id = "base_link";
//     target_pose_stamped.header.stamp = this->now();
//     target_pose_stamped.pose.position = request->target_pose.position;
    
//     // Ensure orientation is valid - if not provided, use default
//     if (std::abs(request->target_pose.orientation.x) < 1e-6 &&
//         std::abs(request->target_pose.orientation.y) < 1e-6 &&
//         std::abs(request->target_pose.orientation.z) < 1e-6 &&
//         std::abs(request->target_pose.orientation.w) < 1e-6) {
//         // No orientation provided, use default (pointing down)
//         target_pose_stamped.pose.orientation.w = 1.0;
//         target_pose_stamped.pose.orientation.x = 0.0;
//         target_pose_stamped.pose.orientation.y = 0.0;
//         target_pose_stamped.pose.orientation.z = 0.0;
//         RCLCPP_INFO(this->get_logger(), "Using default orientation");
//     } else {
//         target_pose_stamped.pose.orientation = request->target_pose.orientation;
//         RCLCPP_INFO(this->get_logger(), "Using provided orientation: [%.3f, %.3f, %.3f, %.3f]",
//                     request->target_pose.orientation.x,
//                     request->target_pose.orientation.y,
//                     request->target_pose.orientation.z,
//                     request->target_pose.orientation.w);
//     }

//     // Check reachability
//     if (!is_pose_reachable(target_pose_stamped.pose)) {
//         response->success = false;
//         response->message = "Target pose is not reachable";
//         RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
//         return;
//     }

//     // Clear previous targets
//     move_group_interface_->clearPoseTargets();
    
//     try {
//         // First attempt: Full pose planning
//         RCLCPP_INFO(this->get_logger(), "Attempting full pose planning...");
//         move_group_interface_->setPoseTarget(target_pose_stamped);
        
//         moveit::planning_interface::MoveGroupInterface::Plan my_plan;
//         moveit::core::MoveItErrorCode success_code;
        
//         for (int i = 0; i < 3; ++i) {
//             success_code = move_group_interface_->plan(my_plan);
//             if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                 RCLCPP_INFO(this->get_logger(), "Full pose planning succeeded on attempt %d", i + 1);
//                 break;
//             }
//             RCLCPP_WARN(this->get_logger(), "Planning attempt %d failed with code %d: %s",
//                         i + 1, success_code.val, moveit::core::errorCodeToString(success_code).c_str());
//             rclcpp::sleep_for(std::chrono::milliseconds(500));
//         }

//         if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//             RCLCPP_INFO(this->get_logger(), "Executing full pose plan...");
//             moveit::core::MoveItErrorCode execute_code = move_group_interface_->execute(my_plan);
//             if (execute_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                 response->success = true;
//                 response->message = "Successfully moved to target pose";
//                 RCLCPP_INFO(this->get_logger(), "Full pose execution successful");
//                 return;
//             } else {
//                 RCLCPP_ERROR(this->get_logger(), "Full pose execution failed with code: %d", execute_code.val);
//             }
//         }

//         // Second attempt: Position-only planning (safer approach)
//         RCLCPP_INFO(this->get_logger(), "Attempting position-only planning...");
//         move_group_interface_->clearPoseTargets();
        
//         // Use position target without specifying end-effector link to avoid TF lookup
//         move_group_interface_->setPositionTarget(
//             target_pose_stamped.pose.position.x,
//             target_pose_stamped.pose.position.y,
//             target_pose_stamped.pose.position.z);
        
//         for (int i = 0; i < 3; ++i) {
//             success_code = move_group_interface_->plan(my_plan);
//             if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                 RCLCPP_INFO(this->get_logger(), "Position-only planning succeeded on attempt %d", i + 1);
//                 break;
//             }
//             RCLCPP_WARN(this->get_logger(), "Position-only attempt %d failed with code %d: %s",
//                         i + 1, success_code.val, moveit::core::errorCodeToString(success_code).c_str());
//             rclcpp::sleep_for(std::chrono::milliseconds(500));
//         }
        
//         if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//             RCLCPP_INFO(this->get_logger(), "Executing position-only plan...");
//             moveit::core::MoveItErrorCode execute_code = move_group_interface_->execute(my_plan);
//             if (execute_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                 response->success = true;
//                 response->message = "Successfully moved to target position (orientation may vary)";
//                 RCLCPP_INFO(this->get_logger(), "Position-only execution successful");
//                 return;
//             } else {
//                 RCLCPP_ERROR(this->get_logger(), "Position-only execution failed with code: %d", execute_code.val);
//             }
//         }

//         // Third attempt: Try a nearby reachable position
//         RCLCPP_INFO(this->get_logger(), "Attempting modified target position...");
//         move_group_interface_->clearPoseTargets();
        
//         // Slightly modify the target to make it more reachable
//         double modified_x = std::min(0.25, std::max(0.1, target_pose_stamped.pose.position.x));
//         double modified_z = std::min(0.3, std::max(0.12, target_pose_stamped.pose.position.z));
        
//         move_group_interface_->setPositionTarget(modified_x, 0.0, modified_z);
        
//         success_code = move_group_interface_->plan(my_plan);
//         if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//             RCLCPP_INFO(this->get_logger(), "Modified target planning succeeded");
//             moveit::core::MoveItErrorCode execute_code = move_group_interface_->execute(my_plan);
//             if (execute_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                 response->success = true;
//                 response->message = "Successfully moved to modified target position [" + 
//                                   std::to_string(modified_x) + ", 0.0, " + std::to_string(modified_z) + "]";
//                 RCLCPP_INFO(this->get_logger(), "Modified target execution successful");
//                 return;
//             }
//         }

//         // All attempts failed
//         response->success = false;
//         response->message = "All planning attempts failed. Target may be unreachable.";
//         RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
        
//     } catch (const std::exception& e) {
//         response->success = false;
//         response->message = "Exception during planning: " + std::string(e.what());
//         RCLCPP_ERROR(this->get_logger(), "Exception in GoToPose_callback: %s", e.what());
//     }
// }

//     void initialize() {
//         try {
//             RCLCPP_INFO(this->get_logger(), "Initializing MoveGroupInterface...");
//             move_group_interface_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
//                 shared_from_this(), "arm");
            
//             RCLCPP_INFO(this->get_logger(), "Waiting for joint states...");
//             if (!wait_for_joint_states(10.0)) { // Increased timeout
//                 RCLCPP_ERROR(this->get_logger(), "Failed to get initial joint states");
//                 rclcpp::shutdown();
//                 return;
//             }
            
//             RCLCPP_INFO(this->get_logger(), "Configuring MoveGroupInterface...");
//             move_group_interface_->setPlanningTime(30.0);
//             move_group_interface_->setNumPlanningAttempts(30);
//             move_group_interface_->setMaxVelocityScalingFactor(0.1);
//             move_group_interface_->setMaxAccelerationScalingFactor(0.1);
//             move_group_interface_->setGoalPositionTolerance(0.005);
//             move_group_interface_->setGoalOrientationTolerance(0.1);
//             move_group_interface_->allowReplanning(true);
//             move_group_interface_->setPlannerId("RRTConnect");
            
//             RCLCPP_INFO(this->get_logger(), "Setting up planning scene...");
//             planning_scene_publisher_ = create_publisher<moveit_msgs::msg::PlanningScene>("/planning_scene", 10);
//             update_planning_scene();
            
//             print_robot_info();
            
//             RCLCPP_INFO(this->get_logger(), "Creating service...");
//             service_ = this->create_service<arm_description::srv::GoToPose>(
//                 "GoToPose",
//                 std::bind(&GoToPoseServiceNode::GoToPose_callback, this, std::placeholders::_1, std::placeholders::_2));
            
//             initialized_ = true;
//             RCLCPP_INFO(this->get_logger(), "GoToPose service ready");
//         } catch (const std::exception& e) {
//             RCLCPP_ERROR(this->get_logger(), "Initialization failed: %s", e.what());
//             rclcpp::shutdown();
//         }
//     }

//     bool wait_for_joint_states(double timeout) {
//         auto start = this->now();
//         while (this->now() - start < rclcpp::Duration::from_seconds(timeout)) {
//             try {
//                 auto current_state = move_group_interface_->getCurrentState(1.0);
//                 if (current_state) {
//                     RCLCPP_INFO(this->get_logger(), "Successfully received joint states");
//                     return true;
//                 }
//             } catch (const std::exception& e) {
//                 RCLCPP_WARN(this->get_logger(), "Waiting for joint states: %s", e.what());
//             }
//             rclcpp::sleep_for(std::chrono::milliseconds(100));
//         }
//         RCLCPP_WARN(this->get_logger(), "Timeout waiting for joint states, continuing anyway");
//         return true; // Continue to allow debugging
//     }

//     void print_robot_info() {
//         RCLCPP_INFO(this->get_logger(), "=== Robot Information ===");
//         RCLCPP_INFO(this->get_logger(), "Planning group: %s", "arm");
//         RCLCPP_INFO(this->get_logger(), "Planning frame: %s", move_group_interface_->getPlanningFrame().c_str());
//         RCLCPP_INFO(this->get_logger(), "End-effector link: %s", move_group_interface_->getEndEffectorLink().c_str());
        
//         std::vector<std::string> joint_names = move_group_interface_->getJointNames();
//         RCLCPP_INFO(this->get_logger(), "Active joints: %zu", joint_names.size());
//         for (const auto& joint_name : joint_names) {
//             RCLCPP_INFO(this->get_logger(), "  - %s", joint_name.c_str());
//         }
//         RCLCPP_INFO(this->get_logger(), "========================");
//     }

// public:
//     GoToPoseServiceNode() : Node("go_to_pose_service_node"), initialized_(false) {
//         RCLCPP_INFO(this->get_logger(), "Starting GoToPose service node...");
//     }
    
//     void start_initialization() {
//         initialize();
//     }
// };

// int main(int argc, char** argv) {
//     rclcpp::init(argc, argv);
//     auto node = std::make_shared<GoToPoseServiceNode>();
    
//     node->start_initialization();
    
//     rclcpp::spin(node);
//     rclcpp::shutdown();
//     return 0;
// }




// #include <geometry_msgs/msg/pose_stamped.hpp>
// #include <moveit_msgs/msg/planning_scene.hpp>
// #include <moveit/planning_interface/planning_interface.hpp>
// #include <moveit/move_group_interface/move_group_interface.hpp>
// #include <rclcpp/rclcpp.hpp>
// #include <shape_msgs/msg/plane.hpp>
// #include <arm_description/srv/go_to_pose.hpp>
// #include <thread>

// class GoToPoseServiceNode : public rclcpp::Node {
// private:
//     std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_;
//     rclcpp::Service<arm_description::srv::GoToPose>::SharedPtr service_;
//     rclcpp::Publisher<moveit_msgs::msg::PlanningScene>::SharedPtr planning_scene_publisher_;
//     bool initialized_;

//     bool is_pose_reachable(const geometry_msgs::msg::Pose& pose) {
//         double distance = std::sqrt(
//             std::pow(pose.position.x, 2) +
//             std::pow(pose.position.y, 2) +
//             std::pow(pose.position.z, 2)
//         );
//         return (distance <= 0.3) && (pose.position.z > 0.1);
//     }

//     void update_planning_scene() {
//         moveit_msgs::msg::PlanningScene planning_scene;
//         planning_scene.robot_state.joint_state.header.stamp = this->now();
//         planning_scene.world.collision_objects.clear();
//         moveit_msgs::msg::CollisionObject ground;
//         ground.header.frame_id = "base_link";
//         ground.header.stamp = this->now();
//         ground.id = "ground";
//         shape_msgs::msg::Plane plane;
//         plane.coef = {0.0, 0.0, 1.0, 0.05}; // Plane at z = -0.05
//         ground.planes.push_back(plane);
//         geometry_msgs::msg::Pose pose;
//         pose.orientation.w = 1.0;
//         ground.plane_poses.push_back(pose);
//         planning_scene.world.collision_objects.push_back(ground);
//         planning_scene.is_diff = true;
//         planning_scene_publisher_->publish(planning_scene);
//     }

//     // Process the request asynchronously to avoid blocking
//     void process_goto_request_async(
//         const std::shared_ptr<arm_description::srv::GoToPose::Request> request,
//         std::shared_ptr<arm_description::srv::GoToPose::Response> response) {
        
//         std::thread([this, request, response]() {
//             this->process_goto_request(request, response);
//         }).detach();
//     }

//     void process_goto_request(
//         const std::shared_ptr<arm_description::srv::GoToPose::Request> request,
//         std::shared_ptr<arm_description::srv::GoToPose::Response> response) {
        
//         if (!initialized_) {
//             response->success = false;
//             response->message = "Node not fully initialized";
//             RCLCPP_ERROR(this->get_logger(), "Service called before initialization complete");
//             return;
//         }

//         RCLCPP_INFO(this->get_logger(), "Received GoToPose request");
//         RCLCPP_INFO(this->get_logger(), "Target position: [%.3f, %.3f, %.3f]",
//                     request->target_pose.position.x,
//                     request->target_pose.position.y,
//                     request->target_pose.position.z);

//         // Create pose with guaranteed valid orientation
//         geometry_msgs::msg::PoseStamped target_pose_stamped;
//         target_pose_stamped.header.frame_id = "base_link";
//         target_pose_stamped.header.stamp = this->now();
//         target_pose_stamped.pose.position = request->target_pose.position;
        
//         // Ensure orientation is valid - if not provided, use default
//         if (std::abs(request->target_pose.orientation.x) < 1e-6 &&
//             std::abs(request->target_pose.orientation.y) < 1e-6 &&
//             std::abs(request->target_pose.orientation.z) < 1e-6 &&
//             std::abs(request->target_pose.orientation.w) < 1e-6) {
//             // No orientation provided, use default (pointing down)
//             target_pose_stamped.pose.orientation.w = 1.0;
//             target_pose_stamped.pose.orientation.x = 0.0;
//             target_pose_stamped.pose.orientation.y = 0.0;
//             target_pose_stamped.pose.orientation.z = 0.0;
//             RCLCPP_INFO(this->get_logger(), "Using default orientation");
//         } else {
//             target_pose_stamped.pose.orientation = request->target_pose.orientation;
//             RCLCPP_INFO(this->get_logger(), "Using provided orientation: [%.3f, %.3f, %.3f, %.3f]",
//                         request->target_pose.orientation.x,
//                         request->target_pose.orientation.y,
//                         request->target_pose.orientation.z,
//                         request->target_pose.orientation.w);
//         }

//         // Check reachability
//         if (!is_pose_reachable(target_pose_stamped.pose)) {
//             response->success = false;
//             response->message = "Target pose is not reachable";
//             RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
//             return;
//         }

//         try {
//             // Clear previous targets
//             move_group_interface_->clearPoseTargets();
            
//             // First attempt: Full pose planning with timeout
//             RCLCPP_INFO(this->get_logger(), "Attempting full pose planning...");
//             move_group_interface_->setPoseTarget(target_pose_stamped);
            
//             moveit::planning_interface::MoveGroupInterface::Plan my_plan;
//             moveit::core::MoveItErrorCode success_code;
            
//             // Use asyncMove to avoid blocking - but first try synchronous with timeout
//             auto start_time = std::chrono::steady_clock::now();
//             const auto timeout = std::chrono::seconds(10); // 10 second timeout
            
//             success_code = move_group_interface_->plan(my_plan);
//             auto elapsed = std::chrono::steady_clock::now() - start_time;
            
//             if (elapsed > timeout) {
//                 response->success = false;
//                 response->message = "Planning timeout exceeded";
//                 RCLCPP_ERROR(this->get_logger(), "Planning timeout exceeded");
//                 return;
//             }

//             if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                 RCLCPP_INFO(this->get_logger(), "Full pose planning succeeded");
                
//                 // Execute with timeout check
//                 start_time = std::chrono::steady_clock::now();
//                 moveit::core::MoveItErrorCode execute_code = move_group_interface_->execute(my_plan);
//                 elapsed = std::chrono::steady_clock::now() - start_time;
                
//                 if (elapsed > timeout) {
//                     response->success = false;
//                     response->message = "Execution timeout exceeded";
//                     RCLCPP_ERROR(this->get_logger(), "Execution timeout exceeded");
//                     return;
//                 }
                
//                 if (execute_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                     response->success = true;
//                     response->message = "Successfully moved to target pose";
//                     RCLCPP_INFO(this->get_logger(), "Full pose execution successful");
//                     return;
//                 } else {
//                     RCLCPP_ERROR(this->get_logger(), "Full pose execution failed with code: %d", execute_code.val);
//                 }
//             } else {
//                 RCLCPP_WARN(this->get_logger(), "Full pose planning failed with code %d: %s",
//                            success_code.val, moveit::core::errorCodeToString(success_code).c_str());
//             }

//             // Fallback: Position-only planning
//             RCLCPP_INFO(this->get_logger(), "Attempting position-only planning...");
//             move_group_interface_->clearPoseTargets();
//             move_group_interface_->setPositionTarget(
//                 target_pose_stamped.pose.position.x,
//                 target_pose_stamped.pose.position.y,
//                 target_pose_stamped.pose.position.z);
            
//             start_time = std::chrono::steady_clock::now();
//             success_code = move_group_interface_->plan(my_plan);
//             elapsed = std::chrono::steady_clock::now() - start_time;
            
//             if (elapsed > timeout) {
//                 response->success = false;
//                 response->message = "Position planning timeout exceeded";
//                 RCLCPP_ERROR(this->get_logger(), "Position planning timeout exceeded");
//                 return;
//             }
            
//             if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                 RCLCPP_INFO(this->get_logger(), "Position-only planning succeeded");
                
//                 start_time = std::chrono::steady_clock::now();
//                 moveit::core::MoveItErrorCode execute_code = move_group_interface_->execute(my_plan);
//                 elapsed = std::chrono::steady_clock::now() - start_time;
                
//                 if (elapsed > timeout) {
//                     response->success = false;
//                     response->message = "Position execution timeout exceeded";
//                     RCLCPP_ERROR(this->get_logger(), "Position execution timeout exceeded");
//                     return;
//                 }
                
//                 if (execute_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
//                     response->success = true;
//                     response->message = "Successfully moved to target position (orientation may vary)";
//                     RCLCPP_INFO(this->get_logger(), "Position-only execution successful");
//                     return;
//                 } else {
//                     RCLCPP_ERROR(this->get_logger(), "Position-only execution failed with code: %d", execute_code.val);
//                 }
//             }

//             // All attempts failed
//             response->success = false;
//             response->message = "All planning attempts failed. Target may be unreachable.";
//             RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
            
//         } catch (const std::exception& e) {
//             response->success = false;
//             response->message = "Exception during planning: " + std::string(e.what());
//             RCLCPP_ERROR(this->get_logger(), "Exception in process_goto_request: %s", e.what());
//         }
//     }

//     void GoToPose_callback(
//         const std::shared_ptr<arm_description::srv::GoToPose::Request> request,
//         std::shared_ptr<arm_description::srv::GoToPose::Response> response) {
        
//         // Immediately return a response to prevent hanging
//         // The actual work is done asynchronously
//         RCLCPP_INFO(this->get_logger(), "GoToPose service called - processing request");
        
//         if (!initialized_) {
//             response->success = false;
//             response->message = "Node not fully initialized";
//             RCLCPP_ERROR(this->get_logger(), "Service called before initialization complete");
//             return;
//         }

//         // For now, return immediate success and process asynchronously
//         // In a real implementation, you might want to use action servers for long-running operations
//         response->success = true;
//         response->message = "Motion request received and being processed";
        
//         // Process the actual motion in a separate thread
//         process_goto_request_async(request, response);
//     }

//     void initialize() {
//         try {
//             RCLCPP_INFO(this->get_logger(), "Initializing MoveGroupInterface...");
            
//             // Use a callback group for the MoveGroupInterface to avoid executor conflicts
//             auto callback_group = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
//             rclcpp::executors::SingleThreadedExecutor executor;
//             executor.add_callback_group(callback_group, this->get_node_base_interface());
            
//             move_group_interface_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
//                 shared_from_this(), "arm");
            
//             RCLCPP_INFO(this->get_logger(), "Waiting for joint states...");
//             if (!wait_for_joint_states(5.0)) { // Reduced timeout
//                 RCLCPP_WARN(this->get_logger(), "Could not get initial joint states, continuing anyway");
//             }
            
//             RCLCPP_INFO(this->get_logger(), "Configuring MoveGroupInterface...");
//             // Reduced timeouts to prevent hanging
//             move_group_interface_->setPlanningTime(10.0);  // Reduced from 30.0
//             move_group_interface_->setNumPlanningAttempts(5);  // Reduced from 30
//             move_group_interface_->setMaxVelocityScalingFactor(0.2);  // Increased for faster motion
//             move_group_interface_->setMaxAccelerationScalingFactor(0.2);
//             move_group_interface_->setGoalPositionTolerance(0.01);  // Slightly relaxed
//             move_group_interface_->setGoalOrientationTolerance(0.2);  // More relaxed
//             move_group_interface_->allowReplanning(true);
//             move_group_interface_->setPlannerId("RRTConnect");
            
//             RCLCPP_INFO(this->get_logger(), "Setting up planning scene...");
//             planning_scene_publisher_ = create_publisher<moveit_msgs::msg::PlanningScene>("/planning_scene", 10);
            
//             // Small delay to let publishers connect
//             rclcpp::sleep_for(std::chrono::milliseconds(500));
//             update_planning_scene();
            
//             print_robot_info();
            
//             RCLCPP_INFO(this->get_logger(), "Creating service...");
//             service_ = this->create_service<arm_description::srv::GoToPose>(
//                 "GoToPose",
//                 std::bind(&GoToPoseServiceNode::GoToPose_callback, this, std::placeholders::_1, std::placeholders::_2));
            
//             initialized_ = true;
//             RCLCPP_INFO(this->get_logger(), "GoToPose service ready");
            
//         } catch (const std::exception& e) {
//             RCLCPP_ERROR(this->get_logger(), "Initialization failed: %s", e.what());
//             initialized_ = false;
//             // Don't shutdown immediately, let the node continue for debugging
//         }
//     }

//     bool wait_for_joint_states(double timeout) {
//         auto start = this->now();
//         while (this->now() - start < rclcpp::Duration::from_seconds(timeout)) {
//             try {
//                 // Use shorter timeout for getCurrentState to avoid hanging
//                 auto current_state = move_group_interface_->getCurrentState(0.5);
//                 if (current_state) {
//                     RCLCPP_INFO(this->get_logger(), "Successfully received joint states");
//                     return true;
//                 }
//             } catch (const std::exception& e) {
//                 RCLCPP_WARN(this->get_logger(), "Waiting for joint states: %s", e.what());
//             }
//             rclcpp::sleep_for(std::chrono::milliseconds(100));
            
//             // Allow ROS to process callbacks during wait
//             rclcpp::spin_some(this->get_node_base_interface());
//         }
//         RCLCPP_WARN(this->get_logger(), "Timeout waiting for joint states");
//         return false;
//     }

//     void print_robot_info() {
//         try {
//             RCLCPP_INFO(this->get_logger(), "=== Robot Information ===");
//             RCLCPP_INFO(this->get_logger(), "Planning group: %s", "arm");
//             RCLCPP_INFO(this->get_logger(), "Planning frame: %s", move_group_interface_->getPlanningFrame().c_str());
//             RCLCPP_INFO(this->get_logger(), "End-effector link: %s", move_group_interface_->getEndEffectorLink().c_str());
            
//             std::vector<std::string> joint_names = move_group_interface_->getJointNames();
//             RCLCPP_INFO(this->get_logger(), "Active joints: %zu", joint_names.size());
//             for (const auto& joint_name : joint_names) {
//                 RCLCPP_INFO(this->get_logger(), "  - %s", joint_name.c_str());
//             }
//             RCLCPP_INFO(this->get_logger(), "========================");
//         } catch (const std::exception& e) {
//             RCLCPP_WARN(this->get_logger(), "Could not print robot info: %s", e.what());
//         }
//     }

// public:
//     GoToPoseServiceNode() : Node("go_to_pose_service_node"), initialized_(false) {
//         RCLCPP_INFO(this->get_logger(), "Starting GoToPose service node...");
//     }
    
//     void start_initialization() {
//         // Run initialization in a separate thread to avoid blocking
//         std::thread([this]() {
//             this->initialize();
//         }).detach();
//     }
// };

// int main(int argc, char** argv) {
//     rclcpp::init(argc, argv);
    
//     // Use MultiThreadedExecutor to handle concurrent callbacks
//     rclcpp::executors::MultiThreadedExecutor executor;
//     auto node = std::make_shared<GoToPoseServiceNode>();
    
//     executor.add_node(node);
//     node->start_initialization();
    
//     executor.spin();
//     rclcpp::shutdown();
//     return 0;
// }



#include <geometry_msgs/msg/pose_stamped.hpp>
#include <moveit_msgs/msg/planning_scene.hpp>
#include <moveit/planning_interface/planning_interface.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <rclcpp/rclcpp.hpp>
#include <shape_msgs/msg/plane.hpp>
#include <arm_description/srv/go_to_pose.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <chrono>
#include <future>

class GoToPoseServiceNode : public rclcpp::Node {
private:
    std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_;
    rclcpp::Service<arm_description::srv::GoToPose>::SharedPtr service_;
    rclcpp::Publisher<moveit_msgs::msg::PlanningScene>::SharedPtr planning_scene_publisher_;
    rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_state_sub_;
    bool initialized_;
    bool joint_states_received_;

    // Joint state callback to verify we're receiving joint states
    void joint_state_callback(const sensor_msgs::msg::JointState::SharedPtr msg) {
        if (!joint_states_received_) {
            RCLCPP_INFO(this->get_logger(), "Joint states received successfully");
            joint_states_received_ = true;
        }
    }

    bool is_pose_reachable(const geometry_msgs::msg::Pose& pose) {
        double distance = std::sqrt(
            std::pow(pose.position.x, 2) +
            std::pow(pose.position.y, 2) +
            std::pow(pose.position.z, 2)
        );
        // Adjusted reachability check - be more conservative
        return (distance <= 0.35) && (distance >= 0.1) && (pose.position.z > 0.05);
    }

    void update_planning_scene() {
        moveit_msgs::msg::PlanningScene planning_scene;
        planning_scene.robot_state.joint_state.header.stamp = this->now();
        planning_scene.world.collision_objects.clear();
        
        // Add ground plane
        moveit_msgs::msg::CollisionObject ground;
        ground.header.frame_id = "base_link";
        ground.header.stamp = this->now();
        ground.id = "ground";
        shape_msgs::msg::Plane plane;
        plane.coef = {0.0, 0.0, 1.0, 0.02}; // Plane at z = -0.02
        ground.planes.push_back(plane);
        geometry_msgs::msg::Pose pose;
        pose.orientation.w = 1.0;
        ground.plane_poses.push_back(pose);
        
        planning_scene.world.collision_objects.push_back(ground);
        planning_scene.is_diff = true;
        planning_scene_publisher_->publish(planning_scene);
    }

    // Check if kinematics solver is available
    bool check_kinematics_solver() {
        try {
            // Try to get current state - this will fail if no kinematics solver
            auto current_state = move_group_interface_->getCurrentState(0.5);
            if (!current_state) {
                RCLCPP_ERROR(this->get_logger(), "Cannot get current robot state - check kinematics configuration");
                return false;
            }
            
            // Try a simple IK solve
            geometry_msgs::msg::Pose test_pose;
            test_pose.position.x = 0.2;
            test_pose.position.y = 0.0;
            test_pose.position.z = 0.2;
            test_pose.orientation.w = 1.0;
            
            move_group_interface_->setPoseTarget(test_pose);
            move_group_interface_->setPlanningTime(1.0); // Short planning time for test
            
            moveit::planning_interface::MoveGroupInterface::Plan test_plan;
            auto result = move_group_interface_->plan(test_plan);
            
            move_group_interface_->clearPoseTargets();
            
            if (result.val == moveit::core::MoveItErrorCode::SUCCESS) {
                RCLCPP_INFO(this->get_logger(), "Kinematics solver is working correctly");
                return true;
            } else {
                RCLCPP_WARN(this->get_logger(), "Kinematics solver test failed with code: %d", result.val);
                return false;
            }
        } catch (const std::exception& e) {
            RCLCPP_ERROR(this->get_logger(), "Kinematics solver check failed: %s", e.what());
            return false;
        }
    }

    std::pair<moveit::core::MoveItErrorCode, moveit::planning_interface::MoveGroupInterface::Plan> 
    plan_with_timeout(double timeout_seconds) {
        moveit::planning_interface::MoveGroupInterface::Plan plan;
        
        auto future = std::async(std::launch::async, [this, &plan]() {
            return move_group_interface_->plan(plan);
        });
        
        if (future.wait_for(std::chrono::seconds(static_cast<int>(timeout_seconds))) == std::future_status::timeout) {
            RCLCPP_WARN(this->get_logger(), "Planning timed out after %.1f seconds", timeout_seconds);
            return {moveit::core::MoveItErrorCode::TIMED_OUT, plan};
        }
        
        return {future.get(), plan};
    }

    moveit::core::MoveItErrorCode execute_with_timeout(
        const moveit::planning_interface::MoveGroupInterface::Plan& plan, 
        double timeout_seconds) {
        
        auto future = std::async(std::launch::async, [this, &plan]() {
            return move_group_interface_->execute(plan);
        });
        
        if (future.wait_for(std::chrono::seconds(static_cast<int>(timeout_seconds))) == std::future_status::timeout) {
            RCLCPP_WARN(this->get_logger(), "Execution timed out after %.1f seconds", timeout_seconds);
            return moveit::core::MoveItErrorCode::TIMED_OUT;
        }
        
        return future.get();
    }

    void GoToPose_callback(
        const std::shared_ptr<arm_description::srv::GoToPose::Request> request,
        std::shared_ptr<arm_description::srv::GoToPose::Response> response) {
        
        if (!initialized_) {
            response->success = false;
            response->message = "Node not fully initialized";
            RCLCPP_ERROR(this->get_logger(), "Service called before initialization complete");
            return;
        }

        if (!joint_states_received_) {
            response->success = false;
            response->message = "Joint states not available - check joint_state_publisher";
            RCLCPP_ERROR(this->get_logger(), "Joint states not received");
            return;
        }

        RCLCPP_INFO(this->get_logger(), "Received GoToPose request");
        RCLCPP_INFO(this->get_logger(), "Target position: [%.3f, %.3f, %.3f]",
                    request->target_pose.position.x,
                    request->target_pose.position.y,
                    request->target_pose.position.z);

        // Create pose with guaranteed valid orientation
        geometry_msgs::msg::PoseStamped target_pose_stamped;
        target_pose_stamped.header.frame_id = "base_link";
        target_pose_stamped.header.stamp = this->now();
        target_pose_stamped.pose.position = request->target_pose.position;
        
        // Normalize quaternion if provided
        double quat_norm = std::sqrt(
            std::pow(request->target_pose.orientation.x, 2) +
            std::pow(request->target_pose.orientation.y, 2) +
            std::pow(request->target_pose.orientation.z, 2) +
            std::pow(request->target_pose.orientation.w, 2)
        );
        
        if (quat_norm < 1e-6) {
            // Use default orientation
            target_pose_stamped.pose.orientation.w = 1.0;
            target_pose_stamped.pose.orientation.x = 0.0;
            target_pose_stamped.pose.orientation.y = 0.0;
            target_pose_stamped.pose.orientation.z = 0.0;
            RCLCPP_INFO(this->get_logger(), "Using default orientation");
        } else {
            // Normalize the quaternion
            target_pose_stamped.pose.orientation.x = request->target_pose.orientation.x / quat_norm;
            target_pose_stamped.pose.orientation.y = request->target_pose.orientation.y / quat_norm;
            target_pose_stamped.pose.orientation.z = request->target_pose.orientation.z / quat_norm;
            target_pose_stamped.pose.orientation.w = request->target_pose.orientation.w / quat_norm;
            RCLCPP_INFO(this->get_logger(), "Using normalized orientation: [%.3f, %.3f, %.3f, %.3f]",
                        target_pose_stamped.pose.orientation.x,
                        target_pose_stamped.pose.orientation.y,
                        target_pose_stamped.pose.orientation.z,
                        target_pose_stamped.pose.orientation.w);
        }

        // Check reachability
        if (!is_pose_reachable(target_pose_stamped.pose)) {
            response->success = false;
            response->message = "Target pose is not reachable (outside workspace bounds)";
            RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
            return;
        }

        try {
            // Clear previous targets and stop any motion
            move_group_interface_->clearPoseTargets();
            move_group_interface_->stop();
            
            // Set conservative planning parameters
            move_group_interface_->setPlanningTime(5.0);
            move_group_interface_->setNumPlanningAttempts(5);
            
            // Attempt 1: Full pose planning
            RCLCPP_INFO(this->get_logger(), "Attempting full pose planning...");
            move_group_interface_->setPoseTarget(target_pose_stamped);
            
            auto [success_code, my_plan] = plan_with_timeout(6.0);
            
            if (success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
                RCLCPP_INFO(this->get_logger(), "Full pose planning succeeded, executing...");
                
                moveit::core::MoveItErrorCode execute_code = execute_with_timeout(my_plan, 15.0);
                
                if (execute_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
                    response->success = true;
                    response->message = "Successfully moved to target pose";
                    RCLCPP_INFO(this->get_logger(), "Motion completed successfully");
                    return;
                } else {
                    RCLCPP_ERROR(this->get_logger(), "Execution failed with code: %d", execute_code.val);
                }
            } else {
                RCLCPP_WARN(this->get_logger(), "Full pose planning failed: %s", 
                           moveit::core::errorCodeToString(success_code).c_str());
            }

            // Attempt 2: Position-only planning with relaxed orientation constraints
            RCLCPP_INFO(this->get_logger(), "Attempting position-only planning...");
            move_group_interface_->clearPoseTargets();
            move_group_interface_->setPositionTarget(
                target_pose_stamped.pose.position.x,
                target_pose_stamped.pose.position.y,
                target_pose_stamped.pose.position.z);
            
            // Relax orientation tolerance for position-only planning
            move_group_interface_->setGoalOrientationTolerance(0.5);
            
            auto [pos_success_code, pos_plan] = plan_with_timeout(6.0);
            
            if (pos_success_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
                RCLCPP_INFO(this->get_logger(), "Position-only planning succeeded, executing...");
                
                moveit::core::MoveItErrorCode execute_code = execute_with_timeout(pos_plan, 15.0);
                
                if (execute_code.val == moveit::core::MoveItErrorCode::SUCCESS) {
                    response->success = true;
                    response->message = "Successfully moved to target position (orientation optimized)";
                    RCLCPP_INFO(this->get_logger(), "Position-only motion completed successfully");
                    return;
                }
            }

            // All attempts failed
            response->success = false;
            response->message = "Planning failed. Check kinematics configuration and target reachability.";
            RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
            
        } catch (const std::exception& e) {
            response->success = false;
            response->message = "Exception during planning: " + std::string(e.what());
            RCLCPP_ERROR(this->get_logger(), "Exception in GoToPose_callback: %s", e.what());
        }
    }

    void initialize() {
        try {
            RCLCPP_INFO(this->get_logger(), "Initializing MoveGroupInterface...");
            
            // Subscribe to joint states to monitor availability
            joint_state_sub_ = this->create_subscription<sensor_msgs::msg::JointState>(
                "/joint_states", 10,
                std::bind(&GoToPoseServiceNode::joint_state_callback, this, std::placeholders::_1));
            
            move_group_interface_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
                shared_from_this(), "arm");
            
            RCLCPP_INFO(this->get_logger(), "Waiting for joint states...");
            if (!wait_for_joint_states(10.0)) {
                RCLCPP_ERROR(this->get_logger(), "Could not get initial joint states - check joint_state_publisher");
                return;
            }
            
            RCLCPP_INFO(this->get_logger(), "Configuring MoveGroupInterface...");
            move_group_interface_->setPlanningTime(5.0);
            move_group_interface_->setNumPlanningAttempts(5);
            move_group_interface_->setMaxVelocityScalingFactor(0.3);
            move_group_interface_->setMaxAccelerationScalingFactor(0.3);
            move_group_interface_->setGoalPositionTolerance(0.01);
            move_group_interface_->setGoalOrientationTolerance(0.1);
            move_group_interface_->allowReplanning(true);
            move_group_interface_->setPlannerId("RRTConnect");
            
            // Check if kinematics solver is properly configured
            RCLCPP_INFO(this->get_logger(), "Testing kinematics solver...");
            if (!check_kinematics_solver()) {
                RCLCPP_ERROR(this->get_logger(), "Kinematics solver not working - check kinematics.yaml configuration");
                return;
            }
            
            RCLCPP_INFO(this->get_logger(), "Setting up planning scene...");
            planning_scene_publisher_ = create_publisher<moveit_msgs::msg::PlanningScene>("/planning_scene", 10);
            
            rclcpp::sleep_for(std::chrono::milliseconds(1000));
            update_planning_scene();
            
            print_robot_info();
            
            RCLCPP_INFO(this->get_logger(), "Creating service...");
            service_ = this->create_service<arm_description::srv::GoToPose>(
                "GoToPose",
                std::bind(&GoToPoseServiceNode::GoToPose_callback, this, std::placeholders::_1, std::placeholders::_2));
            
            initialized_ = true;
            RCLCPP_INFO(this->get_logger(), "GoToPose service ready");
            
        } catch (const std::exception& e) {
            RCLCPP_ERROR(this->get_logger(), "Initialization failed: %s", e.what());
            initialized_ = false;
        }
    }

    bool wait_for_joint_states(double timeout) {
        auto start = this->now();
        while (this->now() - start < rclcpp::Duration::from_seconds(timeout)) {
            try {
                auto current_state = move_group_interface_->getCurrentState(1.0);
                if (current_state) {
                    RCLCPP_INFO(this->get_logger(), "Successfully received joint states");
                    return true;
                }
            } catch (const std::exception& e) {
                RCLCPP_DEBUG(this->get_logger(), "Waiting for joint states: %s", e.what());
            }
            rclcpp::sleep_for(std::chrono::milliseconds(500));
        }
        return false;
    }

    void print_robot_info() {
        try {
            RCLCPP_INFO(this->get_logger(), "=== Robot Information ===");
            RCLCPP_INFO(this->get_logger(), "Planning group: %s", "arm");
            RCLCPP_INFO(this->get_logger(), "Planning frame: %s", move_group_interface_->getPlanningFrame().c_str());
            RCLCPP_INFO(this->get_logger(), "End-effector link: %s", move_group_interface_->getEndEffectorLink().c_str());
            
            std::vector<std::string> joint_names = move_group_interface_->getJointNames();
            RCLCPP_INFO(this->get_logger(), "Active joints: %zu", joint_names.size());
            for (const auto& joint_name : joint_names) {
                RCLCPP_INFO(this->get_logger(), "  - %s", joint_name.c_str());
            }
            RCLCPP_INFO(this->get_logger(), "========================");
        } catch (const std::exception& e) {
            RCLCPP_WARN(this->get_logger(), "Could not print robot info: %s", e.what());
        }
    }

public:
    GoToPoseServiceNode() : Node("go_to_pose_service_node"), initialized_(false), joint_states_received_(false) {
        RCLCPP_INFO(this->get_logger(), "Starting GoToPose service node...");
    }
    
    void start_initialization() {
        initialize();
    }
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    
    auto node = std::make_shared<GoToPoseServiceNode>();
    node->start_initialization();
    
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}