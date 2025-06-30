// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice
#include "cube_msgs/msg/detail/color_pose_stamped__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `color`
#include "rosidl_runtime_c/string_functions.h"

bool
cube_msgs__msg__ColorPoseStamped__init(cube_msgs__msg__ColorPoseStamped * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    cube_msgs__msg__ColorPoseStamped__fini(msg);
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    cube_msgs__msg__ColorPoseStamped__fini(msg);
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__init(&msg->color)) {
    cube_msgs__msg__ColorPoseStamped__fini(msg);
    return false;
  }
  return true;
}

void
cube_msgs__msg__ColorPoseStamped__fini(cube_msgs__msg__ColorPoseStamped * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // color
  rosidl_runtime_c__String__fini(&msg->color);
}

bool
cube_msgs__msg__ColorPoseStamped__are_equal(const cube_msgs__msg__ColorPoseStamped * lhs, const cube_msgs__msg__ColorPoseStamped * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->color), &(rhs->color)))
  {
    return false;
  }
  return true;
}

bool
cube_msgs__msg__ColorPoseStamped__copy(
  const cube_msgs__msg__ColorPoseStamped * input,
  cube_msgs__msg__ColorPoseStamped * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__copy(
      &(input->color), &(output->color)))
  {
    return false;
  }
  return true;
}

cube_msgs__msg__ColorPoseStamped *
cube_msgs__msg__ColorPoseStamped__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cube_msgs__msg__ColorPoseStamped * msg = (cube_msgs__msg__ColorPoseStamped *)allocator.allocate(sizeof(cube_msgs__msg__ColorPoseStamped), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(cube_msgs__msg__ColorPoseStamped));
  bool success = cube_msgs__msg__ColorPoseStamped__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
cube_msgs__msg__ColorPoseStamped__destroy(cube_msgs__msg__ColorPoseStamped * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    cube_msgs__msg__ColorPoseStamped__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
cube_msgs__msg__ColorPoseStamped__Sequence__init(cube_msgs__msg__ColorPoseStamped__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cube_msgs__msg__ColorPoseStamped * data = NULL;

  if (size) {
    data = (cube_msgs__msg__ColorPoseStamped *)allocator.zero_allocate(size, sizeof(cube_msgs__msg__ColorPoseStamped), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = cube_msgs__msg__ColorPoseStamped__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        cube_msgs__msg__ColorPoseStamped__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
cube_msgs__msg__ColorPoseStamped__Sequence__fini(cube_msgs__msg__ColorPoseStamped__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      cube_msgs__msg__ColorPoseStamped__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

cube_msgs__msg__ColorPoseStamped__Sequence *
cube_msgs__msg__ColorPoseStamped__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cube_msgs__msg__ColorPoseStamped__Sequence * array = (cube_msgs__msg__ColorPoseStamped__Sequence *)allocator.allocate(sizeof(cube_msgs__msg__ColorPoseStamped__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = cube_msgs__msg__ColorPoseStamped__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
cube_msgs__msg__ColorPoseStamped__Sequence__destroy(cube_msgs__msg__ColorPoseStamped__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    cube_msgs__msg__ColorPoseStamped__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
cube_msgs__msg__ColorPoseStamped__Sequence__are_equal(const cube_msgs__msg__ColorPoseStamped__Sequence * lhs, const cube_msgs__msg__ColorPoseStamped__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!cube_msgs__msg__ColorPoseStamped__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
cube_msgs__msg__ColorPoseStamped__Sequence__copy(
  const cube_msgs__msg__ColorPoseStamped__Sequence * input,
  cube_msgs__msg__ColorPoseStamped__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(cube_msgs__msg__ColorPoseStamped);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    cube_msgs__msg__ColorPoseStamped * data =
      (cube_msgs__msg__ColorPoseStamped *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!cube_msgs__msg__ColorPoseStamped__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          cube_msgs__msg__ColorPoseStamped__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!cube_msgs__msg__ColorPoseStamped__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
