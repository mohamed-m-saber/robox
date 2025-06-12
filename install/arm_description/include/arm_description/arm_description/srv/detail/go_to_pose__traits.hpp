// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_description:srv/GoToPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "arm_description/srv/go_to_pose.hpp"


#ifndef ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__TRAITS_HPP_
#define ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_description/srv/detail/go_to_pose__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace arm_description
{

namespace srv
{

inline void to_flow_style_yaml(
  const GoToPose_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_pose
  {
    out << "target_pose: ";
    to_flow_style_yaml(msg.target_pose, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GoToPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_pose:\n";
    to_block_style_yaml(msg.target_pose, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GoToPose_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace arm_description

namespace rosidl_generator_traits
{

[[deprecated("use arm_description::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_description::srv::GoToPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_description::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_description::srv::to_yaml() instead")]]
inline std::string to_yaml(const arm_description::srv::GoToPose_Request & msg)
{
  return arm_description::srv::to_yaml(msg);
}

template<>
inline const char * data_type<arm_description::srv::GoToPose_Request>()
{
  return "arm_description::srv::GoToPose_Request";
}

template<>
inline const char * name<arm_description::srv::GoToPose_Request>()
{
  return "arm_description/srv/GoToPose_Request";
}

template<>
struct has_fixed_size<arm_description::srv::GoToPose_Request>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct has_bounded_size<arm_description::srv::GoToPose_Request>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct is_message<arm_description::srv::GoToPose_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace arm_description
{

namespace srv
{

inline void to_flow_style_yaml(
  const GoToPose_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GoToPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GoToPose_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace arm_description

namespace rosidl_generator_traits
{

[[deprecated("use arm_description::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_description::srv::GoToPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_description::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_description::srv::to_yaml() instead")]]
inline std::string to_yaml(const arm_description::srv::GoToPose_Response & msg)
{
  return arm_description::srv::to_yaml(msg);
}

template<>
inline const char * data_type<arm_description::srv::GoToPose_Response>()
{
  return "arm_description::srv::GoToPose_Response";
}

template<>
inline const char * name<arm_description::srv::GoToPose_Response>()
{
  return "arm_description/srv/GoToPose_Response";
}

template<>
struct has_fixed_size<arm_description::srv::GoToPose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_description::srv::GoToPose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_description::srv::GoToPose_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace arm_description
{

namespace srv
{

inline void to_flow_style_yaml(
  const GoToPose_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GoToPose_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GoToPose_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace arm_description

namespace rosidl_generator_traits
{

[[deprecated("use arm_description::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_description::srv::GoToPose_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_description::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_description::srv::to_yaml() instead")]]
inline std::string to_yaml(const arm_description::srv::GoToPose_Event & msg)
{
  return arm_description::srv::to_yaml(msg);
}

template<>
inline const char * data_type<arm_description::srv::GoToPose_Event>()
{
  return "arm_description::srv::GoToPose_Event";
}

template<>
inline const char * name<arm_description::srv::GoToPose_Event>()
{
  return "arm_description/srv/GoToPose_Event";
}

template<>
struct has_fixed_size<arm_description::srv::GoToPose_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_description::srv::GoToPose_Event>
  : std::integral_constant<bool, has_bounded_size<arm_description::srv::GoToPose_Request>::value && has_bounded_size<arm_description::srv::GoToPose_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<arm_description::srv::GoToPose_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_description::srv::GoToPose>()
{
  return "arm_description::srv::GoToPose";
}

template<>
inline const char * name<arm_description::srv::GoToPose>()
{
  return "arm_description/srv/GoToPose";
}

template<>
struct has_fixed_size<arm_description::srv::GoToPose>
  : std::integral_constant<
    bool,
    has_fixed_size<arm_description::srv::GoToPose_Request>::value &&
    has_fixed_size<arm_description::srv::GoToPose_Response>::value
  >
{
};

template<>
struct has_bounded_size<arm_description::srv::GoToPose>
  : std::integral_constant<
    bool,
    has_bounded_size<arm_description::srv::GoToPose_Request>::value &&
    has_bounded_size<arm_description::srv::GoToPose_Response>::value
  >
{
};

template<>
struct is_service<arm_description::srv::GoToPose>
  : std::true_type
{
};

template<>
struct is_service_request<arm_description::srv::GoToPose_Request>
  : std::true_type
{
};

template<>
struct is_service_response<arm_description::srv::GoToPose_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__TRAITS_HPP_
