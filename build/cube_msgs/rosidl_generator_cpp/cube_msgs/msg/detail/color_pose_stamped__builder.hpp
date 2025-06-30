// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "cube_msgs/msg/color_pose_stamped.hpp"


#ifndef CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__BUILDER_HPP_
#define CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cube_msgs/msg/detail/color_pose_stamped__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cube_msgs
{

namespace msg
{

namespace builder
{

class Init_ColorPoseStamped_color
{
public:
  explicit Init_ColorPoseStamped_color(::cube_msgs::msg::ColorPoseStamped & msg)
  : msg_(msg)
  {}
  ::cube_msgs::msg::ColorPoseStamped color(::cube_msgs::msg::ColorPoseStamped::_color_type arg)
  {
    msg_.color = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::msg::ColorPoseStamped msg_;
};

class Init_ColorPoseStamped_pose
{
public:
  explicit Init_ColorPoseStamped_pose(::cube_msgs::msg::ColorPoseStamped & msg)
  : msg_(msg)
  {}
  Init_ColorPoseStamped_color pose(::cube_msgs::msg::ColorPoseStamped::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_ColorPoseStamped_color(msg_);
  }

private:
  ::cube_msgs::msg::ColorPoseStamped msg_;
};

class Init_ColorPoseStamped_header
{
public:
  Init_ColorPoseStamped_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ColorPoseStamped_pose header(::cube_msgs::msg::ColorPoseStamped::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ColorPoseStamped_pose(msg_);
  }

private:
  ::cube_msgs::msg::ColorPoseStamped msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::msg::ColorPoseStamped>()
{
  return cube_msgs::msg::builder::Init_ColorPoseStamped_header();
}

}  // namespace cube_msgs

#endif  // CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__BUILDER_HPP_
