// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_description:srv/GoToPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "arm_description/srv/go_to_pose.h"


#ifndef ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__STRUCT_H_
#define ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in srv/GoToPose in the package arm_description.
typedef struct arm_description__srv__GoToPose_Request
{
  geometry_msgs__msg__Pose target_pose;
} arm_description__srv__GoToPose_Request;

// Struct for a sequence of arm_description__srv__GoToPose_Request.
typedef struct arm_description__srv__GoToPose_Request__Sequence
{
  arm_description__srv__GoToPose_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_description__srv__GoToPose_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GoToPose in the package arm_description.
typedef struct arm_description__srv__GoToPose_Response
{
  bool success;
  rosidl_runtime_c__String message;
} arm_description__srv__GoToPose_Response;

// Struct for a sequence of arm_description__srv__GoToPose_Response.
typedef struct arm_description__srv__GoToPose_Response__Sequence
{
  arm_description__srv__GoToPose_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_description__srv__GoToPose_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  arm_description__srv__GoToPose_Event__request__MAX_SIZE = 1
};
// response
enum
{
  arm_description__srv__GoToPose_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/GoToPose in the package arm_description.
typedef struct arm_description__srv__GoToPose_Event
{
  service_msgs__msg__ServiceEventInfo info;
  arm_description__srv__GoToPose_Request__Sequence request;
  arm_description__srv__GoToPose_Response__Sequence response;
} arm_description__srv__GoToPose_Event;

// Struct for a sequence of arm_description__srv__GoToPose_Event.
typedef struct arm_description__srv__GoToPose_Event__Sequence
{
  arm_description__srv__GoToPose_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_description__srv__GoToPose_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_DESCRIPTION__SRV__DETAIL__GO_TO_POSE__STRUCT_H_
