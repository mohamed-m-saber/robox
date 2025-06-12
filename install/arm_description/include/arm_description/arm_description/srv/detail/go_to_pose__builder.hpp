// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_description:srv/GoToPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "arm_description/srv/go_to_pose.hpp"


#ifndef ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__BUILDER_HPP_
#define ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_description/srv/detail/go_to_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_description
{

namespace srv
{

namespace builder
{

class Init_GoToPose_Request_target_pose
{
public:
  Init_GoToPose_Request_target_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::arm_description::srv::GoToPose_Request target_pose(::arm_description::srv::GoToPose_Request::_target_pose_type arg)
  {
    msg_.target_pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_description::srv::GoToPose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_description::srv::GoToPose_Request>()
{
  return arm_description::srv::builder::Init_GoToPose_Request_target_pose();
}

}  // namespace arm_description


namespace arm_description
{

namespace srv
{

namespace builder
{

class Init_GoToPose_Response_message
{
public:
  explicit Init_GoToPose_Response_message(::arm_description::srv::GoToPose_Response & msg)
  : msg_(msg)
  {}
  ::arm_description::srv::GoToPose_Response message(::arm_description::srv::GoToPose_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_description::srv::GoToPose_Response msg_;
};

class Init_GoToPose_Response_success
{
public:
  Init_GoToPose_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToPose_Response_message success(::arm_description::srv::GoToPose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GoToPose_Response_message(msg_);
  }

private:
  ::arm_description::srv::GoToPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_description::srv::GoToPose_Response>()
{
  return arm_description::srv::builder::Init_GoToPose_Response_success();
}

}  // namespace arm_description


namespace arm_description
{

namespace srv
{

namespace builder
{

class Init_GoToPose_Event_response
{
public:
  explicit Init_GoToPose_Event_response(::arm_description::srv::GoToPose_Event & msg)
  : msg_(msg)
  {}
  ::arm_description::srv::GoToPose_Event response(::arm_description::srv::GoToPose_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_description::srv::GoToPose_Event msg_;
};

class Init_GoToPose_Event_request
{
public:
  explicit Init_GoToPose_Event_request(::arm_description::srv::GoToPose_Event & msg)
  : msg_(msg)
  {}
  Init_GoToPose_Event_response request(::arm_description::srv::GoToPose_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GoToPose_Event_response(msg_);
  }

private:
  ::arm_description::srv::GoToPose_Event msg_;
};

class Init_GoToPose_Event_info
{
public:
  Init_GoToPose_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToPose_Event_request info(::arm_description::srv::GoToPose_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GoToPose_Event_request(msg_);
  }

private:
  ::arm_description::srv::GoToPose_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_description::srv::GoToPose_Event>()
{
  return arm_description::srv::builder::Init_GoToPose_Event_info();
}

}  // namespace arm_description

#endif  // ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__BUILDER_HPP_
