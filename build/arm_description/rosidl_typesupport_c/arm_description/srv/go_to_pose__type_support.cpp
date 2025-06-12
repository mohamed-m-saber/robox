// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from arm_description:srv/GoToPose.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "arm_description/srv/detail/go_to_pose__struct.h"
#include "arm_description/srv/detail/go_to_pose__type_support.h"
#include "arm_description/srv/detail/go_to_pose__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GoToPose_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_Request_type_support_ids_t;

static const _GoToPose_Request_type_support_ids_t _GoToPose_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GoToPose_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToPose_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToPose_Request_type_support_symbol_names_t _GoToPose_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, arm_description, srv, GoToPose_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_description, srv, GoToPose_Request)),
  }
};

typedef struct _GoToPose_Request_type_support_data_t
{
  void * data[2];
} _GoToPose_Request_type_support_data_t;

static _GoToPose_Request_type_support_data_t _GoToPose_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToPose_Request_message_typesupport_map = {
  2,
  "arm_description",
  &_GoToPose_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GoToPose_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GoToPose_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToPose_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &arm_description__srv__GoToPose_Request__get_type_hash,
  &arm_description__srv__GoToPose_Request__get_type_description,
  &arm_description__srv__GoToPose_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace arm_description

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, arm_description, srv, GoToPose_Request)() {
  return &::arm_description::srv::rosidl_typesupport_c::GoToPose_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__struct.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__type_support.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GoToPose_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_Response_type_support_ids_t;

static const _GoToPose_Response_type_support_ids_t _GoToPose_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GoToPose_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToPose_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToPose_Response_type_support_symbol_names_t _GoToPose_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, arm_description, srv, GoToPose_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_description, srv, GoToPose_Response)),
  }
};

typedef struct _GoToPose_Response_type_support_data_t
{
  void * data[2];
} _GoToPose_Response_type_support_data_t;

static _GoToPose_Response_type_support_data_t _GoToPose_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToPose_Response_message_typesupport_map = {
  2,
  "arm_description",
  &_GoToPose_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GoToPose_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GoToPose_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToPose_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &arm_description__srv__GoToPose_Response__get_type_hash,
  &arm_description__srv__GoToPose_Response__get_type_description,
  &arm_description__srv__GoToPose_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace arm_description

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, arm_description, srv, GoToPose_Response)() {
  return &::arm_description::srv::rosidl_typesupport_c::GoToPose_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__struct.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__type_support.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GoToPose_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_Event_type_support_ids_t;

static const _GoToPose_Event_type_support_ids_t _GoToPose_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GoToPose_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToPose_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToPose_Event_type_support_symbol_names_t _GoToPose_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, arm_description, srv, GoToPose_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_description, srv, GoToPose_Event)),
  }
};

typedef struct _GoToPose_Event_type_support_data_t
{
  void * data[2];
} _GoToPose_Event_type_support_data_t;

static _GoToPose_Event_type_support_data_t _GoToPose_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToPose_Event_message_typesupport_map = {
  2,
  "arm_description",
  &_GoToPose_Event_message_typesupport_ids.typesupport_identifier[0],
  &_GoToPose_Event_message_typesupport_symbol_names.symbol_name[0],
  &_GoToPose_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToPose_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &arm_description__srv__GoToPose_Event__get_type_hash,
  &arm_description__srv__GoToPose_Event__get_type_description,
  &arm_description__srv__GoToPose_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace arm_description

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, arm_description, srv, GoToPose_Event)() {
  return &::arm_description::srv::rosidl_typesupport_c::GoToPose_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_c
{
typedef struct _GoToPose_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_type_support_ids_t;

static const _GoToPose_type_support_ids_t _GoToPose_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GoToPose_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToPose_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToPose_type_support_symbol_names_t _GoToPose_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, arm_description, srv, GoToPose)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_description, srv, GoToPose)),
  }
};

typedef struct _GoToPose_type_support_data_t
{
  void * data[2];
} _GoToPose_type_support_data_t;

static _GoToPose_type_support_data_t _GoToPose_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToPose_service_typesupport_map = {
  2,
  "arm_description",
  &_GoToPose_service_typesupport_ids.typesupport_identifier[0],
  &_GoToPose_service_typesupport_symbol_names.symbol_name[0],
  &_GoToPose_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GoToPose_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &GoToPose_Request_message_type_support_handle,
  &GoToPose_Response_message_type_support_handle,
  &GoToPose_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    arm_description,
    srv,
    GoToPose
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    arm_description,
    srv,
    GoToPose
  ),
  &arm_description__srv__GoToPose__get_type_hash,
  &arm_description__srv__GoToPose__get_type_description,
  &arm_description__srv__GoToPose__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace arm_description

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, arm_description, srv, GoToPose)() {
  return &::arm_description::srv::rosidl_typesupport_c::GoToPose_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
