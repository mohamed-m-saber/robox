// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from arm_description:srv/GoToPose.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "arm_description/srv/detail/go_to_pose__functions.h"
#include "arm_description/srv/detail/go_to_pose__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToPose_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_Request_type_support_ids_t;

static const _GoToPose_Request_type_support_ids_t _GoToPose_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, arm_description, srv, GoToPose_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, arm_description, srv, GoToPose_Request)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &arm_description__srv__GoToPose_Request__get_type_hash,
  &arm_description__srv__GoToPose_Request__get_type_description,
  &arm_description__srv__GoToPose_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace arm_description

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<arm_description::srv::GoToPose_Request>()
{
  return &::arm_description::srv::rosidl_typesupport_cpp::GoToPose_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, arm_description, srv, GoToPose_Request)() {
  return get_message_type_support_handle<arm_description::srv::GoToPose_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__functions.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToPose_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_Response_type_support_ids_t;

static const _GoToPose_Response_type_support_ids_t _GoToPose_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, arm_description, srv, GoToPose_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, arm_description, srv, GoToPose_Response)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &arm_description__srv__GoToPose_Response__get_type_hash,
  &arm_description__srv__GoToPose_Response__get_type_description,
  &arm_description__srv__GoToPose_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace arm_description

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<arm_description::srv::GoToPose_Response>()
{
  return &::arm_description::srv::rosidl_typesupport_cpp::GoToPose_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, arm_description, srv, GoToPose_Response)() {
  return get_message_type_support_handle<arm_description::srv::GoToPose_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__functions.h"
// already included above
// #include "arm_description/srv/detail/go_to_pose__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToPose_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_Event_type_support_ids_t;

static const _GoToPose_Event_type_support_ids_t _GoToPose_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, arm_description, srv, GoToPose_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, arm_description, srv, GoToPose_Event)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &arm_description__srv__GoToPose_Event__get_type_hash,
  &arm_description__srv__GoToPose_Event__get_type_description,
  &arm_description__srv__GoToPose_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace arm_description

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<arm_description::srv::GoToPose_Event>()
{
  return &::arm_description::srv::rosidl_typesupport_cpp::GoToPose_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, arm_description, srv, GoToPose_Event)() {
  return get_message_type_support_handle<arm_description::srv::GoToPose_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "arm_description/srv/detail/go_to_pose__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace arm_description
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToPose_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToPose_type_support_ids_t;

static const _GoToPose_type_support_ids_t _GoToPose_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, arm_description, srv, GoToPose)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, arm_description, srv, GoToPose)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToPose_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<arm_description::srv::GoToPose_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<arm_description::srv::GoToPose_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<arm_description::srv::GoToPose_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<arm_description::srv::GoToPose>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<arm_description::srv::GoToPose>,
  &arm_description__srv__GoToPose__get_type_hash,
  &arm_description__srv__GoToPose__get_type_description,
  &arm_description__srv__GoToPose__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace arm_description

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<arm_description::srv::GoToPose>()
{
  return &::arm_description::srv::rosidl_typesupport_cpp::GoToPose_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, arm_description, srv, GoToPose)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<arm_description::srv::GoToPose>();
}

#ifdef __cplusplus
}
#endif
