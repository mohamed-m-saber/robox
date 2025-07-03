// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from cube_msgs:action/PickAndPlace.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "cube_msgs/action/pick_and_place.hpp"


#ifndef CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__STRUCT_HPP_
#define CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_Goal __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_Goal __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_Goal_
{
  using Type = PickAndPlace_Goal_<ContainerAllocator>;

  explicit PickAndPlace_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->color = "";
    }
  }

  explicit PickAndPlace_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_pose(_alloc, _init),
    color(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->color = "";
    }
  }

  // field types and members
  using _target_pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _target_pose_type target_pose;
  using _color_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _color_type color;

  // setters for named parameter idiom
  Type & set__target_pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->target_pose = _arg;
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
    cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_Goal
    std::shared_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_Goal
    std::shared_ptr<cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_Goal_ & other) const
  {
    if (this->target_pose != other.target_pose) {
      return false;
    }
    if (this->color != other.color) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_Goal_

// alias to use template instance with default allocator
using PickAndPlace_Goal =
  cube_msgs::action::PickAndPlace_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs


#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_Result __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_Result __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_Result_
{
  using Type = PickAndPlace_Result_<ContainerAllocator>;

  explicit PickAndPlace_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit PickAndPlace_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_Result
    std::shared_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_Result
    std::shared_ptr<cube_msgs::action::PickAndPlace_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_Result_

// alias to use template instance with default allocator
using PickAndPlace_Result =
  cube_msgs::action::PickAndPlace_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs


#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_Feedback __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_Feedback_
{
  using Type = PickAndPlace_Feedback_<ContainerAllocator>;

  explicit PickAndPlace_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
    }
  }

  explicit PickAndPlace_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : status(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
    }
  }

  // field types and members
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_type status;

  // setters for named parameter idiom
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_Feedback
    std::shared_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_Feedback
    std::shared_ptr<cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_Feedback_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_Feedback_

// alias to use template instance with default allocator
using PickAndPlace_Feedback =
  cube_msgs::action::PickAndPlace_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "cube_msgs/action/detail/pick_and_place__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Request __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_SendGoal_Request_
{
  using Type = PickAndPlace_SendGoal_Request_<ContainerAllocator>;

  explicit PickAndPlace_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit PickAndPlace_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const cube_msgs::action::PickAndPlace_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Request
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Request
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_SendGoal_Request_

// alias to use template instance with default allocator
using PickAndPlace_SendGoal_Request =
  cube_msgs::action::PickAndPlace_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Response __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_SendGoal_Response_
{
  using Type = PickAndPlace_SendGoal_Response_<ContainerAllocator>;

  explicit PickAndPlace_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit PickAndPlace_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Response
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Response
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_SendGoal_Response_

// alias to use template instance with default allocator
using PickAndPlace_SendGoal_Response =
  cube_msgs::action::PickAndPlace_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Event __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Event __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_SendGoal_Event_
{
  using Type = PickAndPlace_SendGoal_Event_<ContainerAllocator>;

  explicit PickAndPlace_SendGoal_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit PickAndPlace_SendGoal_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_SendGoal_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_SendGoal_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Event
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_SendGoal_Event
    std::shared_ptr<cube_msgs::action::PickAndPlace_SendGoal_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_SendGoal_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_SendGoal_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_SendGoal_Event_

// alias to use template instance with default allocator
using PickAndPlace_SendGoal_Event =
  cube_msgs::action::PickAndPlace_SendGoal_Event_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs

namespace cube_msgs
{

namespace action
{

struct PickAndPlace_SendGoal
{
  using Request = cube_msgs::action::PickAndPlace_SendGoal_Request;
  using Response = cube_msgs::action::PickAndPlace_SendGoal_Response;
  using Event = cube_msgs::action::PickAndPlace_SendGoal_Event;
};

}  // namespace action

}  // namespace cube_msgs


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Request __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_GetResult_Request_
{
  using Type = PickAndPlace_GetResult_Request_<ContainerAllocator>;

  explicit PickAndPlace_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit PickAndPlace_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Request
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Request
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_GetResult_Request_

// alias to use template instance with default allocator
using PickAndPlace_GetResult_Request =
  cube_msgs::action::PickAndPlace_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs


// Include directives for member types
// Member 'result'
// already included above
// #include "cube_msgs/action/detail/pick_and_place__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Response __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_GetResult_Response_
{
  using Type = PickAndPlace_GetResult_Response_<ContainerAllocator>;

  explicit PickAndPlace_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit PickAndPlace_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    cube_msgs::action::PickAndPlace_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const cube_msgs::action::PickAndPlace_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Response
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Response
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_GetResult_Response_

// alias to use template instance with default allocator
using PickAndPlace_GetResult_Response =
  cube_msgs::action::PickAndPlace_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs


// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Event __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Event __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_GetResult_Event_
{
  using Type = PickAndPlace_GetResult_Event_<ContainerAllocator>;

  explicit PickAndPlace_GetResult_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit PickAndPlace_GetResult_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_GetResult_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<cube_msgs::action::PickAndPlace_GetResult_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Event
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_GetResult_Event
    std::shared_ptr<cube_msgs::action::PickAndPlace_GetResult_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_GetResult_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_GetResult_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_GetResult_Event_

// alias to use template instance with default allocator
using PickAndPlace_GetResult_Event =
  cube_msgs::action::PickAndPlace_GetResult_Event_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs

namespace cube_msgs
{

namespace action
{

struct PickAndPlace_GetResult
{
  using Request = cube_msgs::action::PickAndPlace_GetResult_Request;
  using Response = cube_msgs::action::PickAndPlace_GetResult_Response;
  using Event = cube_msgs::action::PickAndPlace_GetResult_Event;
};

}  // namespace action

}  // namespace cube_msgs


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "cube_msgs/action/detail/pick_and_place__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cube_msgs__action__PickAndPlace_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__cube_msgs__action__PickAndPlace_FeedbackMessage __declspec(deprecated)
#endif

namespace cube_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickAndPlace_FeedbackMessage_
{
  using Type = PickAndPlace_FeedbackMessage_<ContainerAllocator>;

  explicit PickAndPlace_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit PickAndPlace_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const cube_msgs::action::PickAndPlace_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_FeedbackMessage
    std::shared_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cube_msgs__action__PickAndPlace_FeedbackMessage
    std::shared_ptr<cube_msgs::action::PickAndPlace_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickAndPlace_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickAndPlace_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickAndPlace_FeedbackMessage_

// alias to use template instance with default allocator
using PickAndPlace_FeedbackMessage =
  cube_msgs::action::PickAndPlace_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace cube_msgs

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace cube_msgs
{

namespace action
{

struct PickAndPlace
{
  /// The goal message defined in the action definition.
  using Goal = cube_msgs::action::PickAndPlace_Goal;
  /// The result message defined in the action definition.
  using Result = cube_msgs::action::PickAndPlace_Result;
  /// The feedback message defined in the action definition.
  using Feedback = cube_msgs::action::PickAndPlace_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = cube_msgs::action::PickAndPlace_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = cube_msgs::action::PickAndPlace_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = cube_msgs::action::PickAndPlace_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct PickAndPlace PickAndPlace;

}  // namespace action

}  // namespace cube_msgs

#endif  // CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__STRUCT_HPP_
