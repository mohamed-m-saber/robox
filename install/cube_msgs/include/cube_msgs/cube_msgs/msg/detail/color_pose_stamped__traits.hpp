// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "cube_msgs/msg/color_pose_stamped.hpp"


#ifndef CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__TRAITS_HPP_
#define CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "cube_msgs/msg/detail/color_pose_stamped__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace cube_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ColorPoseStamped & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: color
  {
    out << "color: ";
    rosidl_generator_traits::value_to_yaml(msg.color, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ColorPoseStamped & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: color
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "color: ";
    rosidl_generator_traits::value_to_yaml(msg.color, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ColorPoseStamped & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace cube_msgs

namespace rosidl_generator_traits
{

[[deprecated("use cube_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const cube_msgs::msg::ColorPoseStamped & msg,
  std::ostream & out, size_t indentation = 0)
{
  cube_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use cube_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const cube_msgs::msg::ColorPoseStamped & msg)
{
  return cube_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<cube_msgs::msg::ColorPoseStamped>()
{
  return "cube_msgs::msg::ColorPoseStamped";
}

template<>
inline const char * name<cube_msgs::msg::ColorPoseStamped>()
{
  return "cube_msgs/msg/ColorPoseStamped";
}

template<>
struct has_fixed_size<cube_msgs::msg::ColorPoseStamped>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<cube_msgs::msg::ColorPoseStamped>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<cube_msgs::msg::ColorPoseStamped>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__TRAITS_HPP_
