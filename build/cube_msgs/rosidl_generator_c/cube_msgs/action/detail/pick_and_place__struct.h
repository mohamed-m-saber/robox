// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from cube_msgs:action/PickAndPlace.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "cube_msgs/action/pick_and_place.h"


#ifndef CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__STRUCT_H_
#define CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__STRUCT_H_

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
// Member 'color'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_Goal
{
  /// Where to pick the cube
  geometry_msgs__msg__Pose target_pose;
  /// Color of the cube
  rosidl_runtime_c__String color;
} cube_msgs__action__PickAndPlace_Goal;

// Struct for a sequence of cube_msgs__action__PickAndPlace_Goal.
typedef struct cube_msgs__action__PickAndPlace_Goal__Sequence
{
  cube_msgs__action__PickAndPlace_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_Result
{
  /// True if pick-and-place succeeded
  bool success;
  /// Optional message (e.g., "Cube placed", "Grasp failed")
  rosidl_runtime_c__String message;
} cube_msgs__action__PickAndPlace_Result;

// Struct for a sequence of cube_msgs__action__PickAndPlace_Result.
typedef struct cube_msgs__action__PickAndPlace_Result__Sequence
{
  cube_msgs__action__PickAndPlace_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_Result__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'status'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_Feedback
{
  /// Progress feedback (e.g., "Moving to pick", "Picking", etc.)
  rosidl_runtime_c__String status;
} cube_msgs__action__PickAndPlace_Feedback;

// Struct for a sequence of cube_msgs__action__PickAndPlace_Feedback.
typedef struct cube_msgs__action__PickAndPlace_Feedback__Sequence
{
  cube_msgs__action__PickAndPlace_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "cube_msgs/action/detail/pick_and_place__struct.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  cube_msgs__action__PickAndPlace_Goal goal;
} cube_msgs__action__PickAndPlace_SendGoal_Request;

// Struct for a sequence of cube_msgs__action__PickAndPlace_SendGoal_Request.
typedef struct cube_msgs__action__PickAndPlace_SendGoal_Request__Sequence
{
  cube_msgs__action__PickAndPlace_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} cube_msgs__action__PickAndPlace_SendGoal_Response;

// Struct for a sequence of cube_msgs__action__PickAndPlace_SendGoal_Response.
typedef struct cube_msgs__action__PickAndPlace_SendGoal_Response__Sequence
{
  cube_msgs__action__PickAndPlace_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  cube_msgs__action__PickAndPlace_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  cube_msgs__action__PickAndPlace_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  cube_msgs__action__PickAndPlace_SendGoal_Request__Sequence request;
  cube_msgs__action__PickAndPlace_SendGoal_Response__Sequence response;
} cube_msgs__action__PickAndPlace_SendGoal_Event;

// Struct for a sequence of cube_msgs__action__PickAndPlace_SendGoal_Event.
typedef struct cube_msgs__action__PickAndPlace_SendGoal_Event__Sequence
{
  cube_msgs__action__PickAndPlace_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} cube_msgs__action__PickAndPlace_GetResult_Request;

// Struct for a sequence of cube_msgs__action__PickAndPlace_GetResult_Request.
typedef struct cube_msgs__action__PickAndPlace_GetResult_Request__Sequence
{
  cube_msgs__action__PickAndPlace_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "cube_msgs/action/detail/pick_and_place__struct.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_GetResult_Response
{
  int8_t status;
  cube_msgs__action__PickAndPlace_Result result;
} cube_msgs__action__PickAndPlace_GetResult_Response;

// Struct for a sequence of cube_msgs__action__PickAndPlace_GetResult_Response.
typedef struct cube_msgs__action__PickAndPlace_GetResult_Response__Sequence
{
  cube_msgs__action__PickAndPlace_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  cube_msgs__action__PickAndPlace_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  cube_msgs__action__PickAndPlace_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  cube_msgs__action__PickAndPlace_GetResult_Request__Sequence request;
  cube_msgs__action__PickAndPlace_GetResult_Response__Sequence response;
} cube_msgs__action__PickAndPlace_GetResult_Event;

// Struct for a sequence of cube_msgs__action__PickAndPlace_GetResult_Event.
typedef struct cube_msgs__action__PickAndPlace_GetResult_Event__Sequence
{
  cube_msgs__action__PickAndPlace_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "cube_msgs/action/detail/pick_and_place__struct.h"

/// Struct defined in action/PickAndPlace in the package cube_msgs.
typedef struct cube_msgs__action__PickAndPlace_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  cube_msgs__action__PickAndPlace_Feedback feedback;
} cube_msgs__action__PickAndPlace_FeedbackMessage;

// Struct for a sequence of cube_msgs__action__PickAndPlace_FeedbackMessage.
typedef struct cube_msgs__action__PickAndPlace_FeedbackMessage__Sequence
{
  cube_msgs__action__PickAndPlace_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__action__PickAndPlace_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUBE_MSGS__ACTION__DETAIL__PICK_AND_PLACE__STRUCT_H_
