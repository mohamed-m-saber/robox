// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "cube_msgs/msg/color_pose_stamped.hpp"


#ifndef CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__STRUCT_HPP_
#define CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__msg__ColorPoseStamped __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__msg__ColorPoseStamped __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ColorPoseStamped_
{
  using Type = ColorPoseStamped_<ContainerAllocator>;

  explicit ColorPoseStamped_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->color = "";
    }
  }

  explicit ColorPoseStamped_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    pose(_alloc, _init),
    color(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->color = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _color_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _color_type color;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__color(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->color = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::msg::ColorPoseStamped_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::msg::ColorPoseStamped_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::msg::ColorPoseStamped_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::msg::ColorPoseStamped_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__msg__ColorPoseStamped
    std::shared_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__msg__ColorPoseStamped
    std::shared_ptr<cube_msgs::msg::ColorPoseStamped_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ColorPoseStamped_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->color != other.color) {
      return false;
    }
    return true;
  }
  bool operator!=(const ColorPoseStamped_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ColorPoseStamped_

// alias to use template instance with default allocator
using ColorPoseStamped =
  cube_msgs::msg::ColorPoseStamped_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace cube_msgs

#endif  // CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__STRUCT_HPP_
