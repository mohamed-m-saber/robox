// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cube_msgs:action/PickAndPlace.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "cube_msgs/action/pick_and_place.hpp"


#ifndef CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__BUILDER_HPP_
#define CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cube_msgs/action/detail/pick_and_place__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_Goal_color
{
public:
  explicit Init_PickAndPlace_Goal_color(::cube_msgs::action::PickAndPlace_Goal & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_Goal color(::cube_msgs::action::PickAndPlace_Goal::_color_type arg)
  {
    msg_.color = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_Goal msg_;
};

class Init_PickAndPlace_Goal_target_pose
{
public:
  Init_PickAndPlace_Goal_target_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_Goal_color target_pose(::cube_msgs::action::PickAndPlace_Goal::_target_pose_type arg)
  {
    msg_.target_pose = std::move(arg);
    return Init_PickAndPlace_Goal_color(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_Goal>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_Goal_target_pose();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_Result_message
{
public:
  explicit Init_PickAndPlace_Result_message(::cube_msgs::action::PickAndPlace_Result & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_Result message(::cube_msgs::action::PickAndPlace_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_Result msg_;
};

class Init_PickAndPlace_Result_success
{
public:
  Init_PickAndPlace_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_Result_message success(::cube_msgs::action::PickAndPlace_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PickAndPlace_Result_message(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_Result>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_Result_success();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_Feedback_status
{
public:
  Init_PickAndPlace_Feedback_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::cube_msgs::action::PickAndPlace_Feedback status(::cube_msgs::action::PickAndPlace_Feedback::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_Feedback>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_Feedback_status();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_SendGoal_Request_goal
{
public:
  explicit Init_PickAndPlace_SendGoal_Request_goal(::cube_msgs::action::PickAndPlace_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_SendGoal_Request goal(::cube_msgs::action::PickAndPlace_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_SendGoal_Request msg_;
};

class Init_PickAndPlace_SendGoal_Request_goal_id
{
public:
  Init_PickAndPlace_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_SendGoal_Request_goal goal_id(::cube_msgs::action::PickAndPlace_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PickAndPlace_SendGoal_Request_goal(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_SendGoal_Request>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_SendGoal_Request_goal_id();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_SendGoal_Response_stamp
{
public:
  explicit Init_PickAndPlace_SendGoal_Response_stamp(::cube_msgs::action::PickAndPlace_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_SendGoal_Response stamp(::cube_msgs::action::PickAndPlace_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_SendGoal_Response msg_;
};

class Init_PickAndPlace_SendGoal_Response_accepted
{
public:
  Init_PickAndPlace_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_SendGoal_Response_stamp accepted(::cube_msgs::action::PickAndPlace_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_PickAndPlace_SendGoal_Response_stamp(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_SendGoal_Response>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_SendGoal_Response_accepted();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_SendGoal_Event_response
{
public:
  explicit Init_PickAndPlace_SendGoal_Event_response(::cube_msgs::action::PickAndPlace_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_SendGoal_Event response(::cube_msgs::action::PickAndPlace_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_SendGoal_Event msg_;
};

class Init_PickAndPlace_SendGoal_Event_request
{
public:
  explicit Init_PickAndPlace_SendGoal_Event_request(::cube_msgs::action::PickAndPlace_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_PickAndPlace_SendGoal_Event_response request(::cube_msgs::action::PickAndPlace_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_PickAndPlace_SendGoal_Event_response(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_SendGoal_Event msg_;
};

class Init_PickAndPlace_SendGoal_Event_info
{
public:
  Init_PickAndPlace_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_SendGoal_Event_request info(::cube_msgs::action::PickAndPlace_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_PickAndPlace_SendGoal_Event_request(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_SendGoal_Event>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_SendGoal_Event_info();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_GetResult_Request_goal_id
{
public:
  Init_PickAndPlace_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::cube_msgs::action::PickAndPlace_GetResult_Request goal_id(::cube_msgs::action::PickAndPlace_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_GetResult_Request>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_GetResult_Request_goal_id();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_GetResult_Response_result
{
public:
  explicit Init_PickAndPlace_GetResult_Response_result(::cube_msgs::action::PickAndPlace_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_GetResult_Response result(::cube_msgs::action::PickAndPlace_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_GetResult_Response msg_;
};

class Init_PickAndPlace_GetResult_Response_status
{
public:
  Init_PickAndPlace_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_GetResult_Response_result status(::cube_msgs::action::PickAndPlace_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_PickAndPlace_GetResult_Response_result(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_GetResult_Response>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_GetResult_Response_status();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_GetResult_Event_response
{
public:
  explicit Init_PickAndPlace_GetResult_Event_response(::cube_msgs::action::PickAndPlace_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_GetResult_Event response(::cube_msgs::action::PickAndPlace_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_GetResult_Event msg_;
};

class Init_PickAndPlace_GetResult_Event_request
{
public:
  explicit Init_PickAndPlace_GetResult_Event_request(::cube_msgs::action::PickAndPlace_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_PickAndPlace_GetResult_Event_response request(::cube_msgs::action::PickAndPlace_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_PickAndPlace_GetResult_Event_response(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_GetResult_Event msg_;
};

class Init_PickAndPlace_GetResult_Event_info
{
public:
  Init_PickAndPlace_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_GetResult_Event_request info(::cube_msgs::action::PickAndPlace_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_PickAndPlace_GetResult_Event_request(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_GetResult_Event>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_GetResult_Event_info();
}

}  // namespace cube_msgs


namespace cube_msgs
{

namespace action
{

namespace builder
{

class Init_PickAndPlace_FeedbackMessage_feedback
{
public:
  explicit Init_PickAndPlace_FeedbackMessage_feedback(::cube_msgs::action::PickAndPlace_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::cube_msgs::action::PickAndPlace_FeedbackMessage feedback(::cube_msgs::action::PickAndPlace_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_FeedbackMessage msg_;
};

class Init_PickAndPlace_FeedbackMessage_goal_id
{
public:
  Init_PickAndPlace_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickAndPlace_FeedbackMessage_feedback goal_id(::cube_msgs::action::PickAndPlace_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PickAndPlace_FeedbackMessage_feedback(msg_);
  }

private:
  ::cube_msgs::action::PickAndPlace_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::cube_msgs::action::PickAndPlace_FeedbackMessage>()
{
  return cube_msgs::action::builder::Init_PickAndPlace_FeedbackMessage_goal_id();
}

}  // namespace cube_msgs

#endif  // CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__BUILDER_HPP_
