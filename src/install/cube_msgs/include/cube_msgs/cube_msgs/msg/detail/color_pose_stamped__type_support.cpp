// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "cube_msgs/msg/detail/color_pose_stamped__functions.h"
#include "cube_msgs/msg/detail/color_pose_stamped__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace cube_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ColorPoseStamped_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) cube_msgs::msg::ColorPoseStamped(_init);
}

void ColorPoseStamped_fini_function(void * message_memory)
{
  auto typed_message = static_cast<cube_msgs::msg::ColorPoseStamped *>(message_memory);
  typed_message->~ColorPoseStamped();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ColorPoseStamped_message_member_array[3] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cube_msgs::msg::ColorPoseStamped, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Pose>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cube_msgs::msg::ColorPoseStamped, pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "color",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cube_msgs::msg::ColorPoseStamped, color),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ColorPoseStamped_message_members = {
  "cube_msgs::msg",  // message namespace
  "ColorPoseStamped",  // message name
  3,  // number of fields
  sizeof(cube_msgs::msg::ColorPoseStamped),
  false,  // has_any_key_member_
  ColorPoseStamped_message_member_array,  // message members
  ColorPoseStamped_init_function,  // function to initialize message memory (memory has to be allocated)
  ColorPoseStamped_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ColorPoseStamped_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ColorPoseStamped_message_members,
  get_message_typesupport_handle_function,
  &cube_msgs__msg__ColorPoseStamped__get_type_hash,
  &cube_msgs__msg__ColorPoseStamped__get_type_description,
  &cube_msgs__msg__ColorPoseStamped__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace cube_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<cube_msgs::msg::ColorPoseStamped>()
{
  return &::cube_msgs::msg::rosidl_typesupport_introspection_cpp::ColorPoseStamped_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, cube_msgs, msg, ColorPoseStamped)() {
  return &::cube_msgs::msg::rosidl_typesupport_introspection_cpp::ColorPoseStamped_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
