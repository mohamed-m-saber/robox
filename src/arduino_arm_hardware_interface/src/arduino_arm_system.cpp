#include "arduino_arm_hardware_interface/arduino_arm_system.hpp"
#include <pluginlib/class_list_macros.hpp>
#include <sstream>

namespace arduino_arm_hardware_interface
{

hardware_interface::CallbackReturn ArduinoArmSystem::on_init(const hardware_interface::HardwareInfo & info)
{
  if (hardware_interface::SystemInterface::on_init(info) != hardware_interface::CallbackReturn::SUCCESS) {
    return hardware_interface::CallbackReturn::ERROR;
  }

  hw_positions_.resize(info.joints.size(), 0.0);
  hw_commands_.resize(info.joints.size(), 0.0);

  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn ArduinoArmSystem::on_configure(const rclcpp_lifecycle::State & /*previous_state*/)
{
  try {
    serial_.Open("/dev/ttyACM0");
    serial_.SetBaudRate(LibSerial::BaudRate::BAUD_57600);
    RCLCPP_INFO(rclcpp::get_logger("ArduinoArmSystem"), "✅ Connected to Arduino");
  }
  catch (const LibSerial::OpenFailed &) {
    RCLCPP_ERROR(rclcpp::get_logger("ArduinoArmSystem"), "❌ Failed to open serial port.");
    return hardware_interface::CallbackReturn::ERROR;
  }

  return hardware_interface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface> ArduinoArmSystem::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;

  for (size_t i = 0; i < info_.joints.size(); ++i) {
    state_interfaces.emplace_back(hardware_interface::StateInterface(
      info_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_positions_[i]));
  }

  return state_interfaces;
}

std::vector<hardware_interface::CommandInterface> ArduinoArmSystem::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  for (size_t i = 0; i < info_.joints.size(); ++i) {
    command_interfaces.emplace_back(hardware_interface::CommandInterface(
      info_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_commands_[i]));
  }

  return command_interfaces;
}

hardware_interface::return_type ArduinoArmSystem::read(const rclcpp::Time &, const rclcpp::Duration &)
{
  // Optionally read feedback if needed
  return hardware_interface::return_type::OK;
}
hardware_interface::return_type ArduinoArmSystem::write(const rclcpp::Time &, const rclcpp::Duration &)
{
  if (!serial_.IsOpen()) {
    RCLCPP_ERROR(rclcpp::get_logger("ArduinoArmSystem"), "❌ Serial port is closed.");
    return hardware_interface::return_type::ERROR;
  }

  std::ostringstream command;
  command << "D";

  for (size_t i = 0; i < hw_commands_.size(); ++i) {
    command << "," << static_cast<int>(hw_commands_[i] * 100);
  }

  command << ",AX\n";

  serial_ << command.str();
  serial_.FlushOutputBuffer();  // ✅ fixed

  RCLCPP_INFO(rclcpp::get_logger("ArduinoArmSystem"), "Sent: %s", command.str().c_str());

  return hardware_interface::return_type::OK;
}


}  // namespace arduino_arm_hardware_interface

PLUGINLIB_EXPORT_CLASS(arduino_arm_hardware_interface::ArduinoArmSystem, hardware_interface::SystemInterface)
