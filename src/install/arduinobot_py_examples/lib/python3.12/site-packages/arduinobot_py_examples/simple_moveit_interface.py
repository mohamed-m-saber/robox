import rclpy
from rclpy.logging import get_logger
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState
import numpy as np

def move_robot():
    robot=MoveItPy(node_name="moveit_py")
    robot_arm=robot.get_planning_component("arm")
    robot_gripper=robot.get_planning_component("gripper")

    arm_state=RobotState(robot.get_robot_model())
    gripper_state=RobotState(robot.get_robot_model())


    arm_state.set_joint_group_positions("arm",np.array([1.57,0.0,0.0,0.0]))
    gripper_state.set_joint_group_positions("gripper",np.array([0.0,-1.0,1.0]))


    robot_arm.set_start_state_to_current_state()
    robot_gripper.set_start_state_to_current_state()

    robot_arm.set_goal_state(robot_state=arm_state)
    robot_gripper.set_goal_state(robot_state=gripper_state)

    arm_plan_res=robot_arm.plan()
    gripper_plan_res=robot_gripper.plan()

    if arm_plan_res and gripper_plan_res:
        robot.execute(arm_plan_res.trajectory,controllers=[])
        robot.execute(gripper_plan_res.trajectory,controllers=[])
    else:

        get_logger("rclpy").error("one or more planners failed !")

def main():
    rclpy.init()
    move_robot()
    rclpy.shutdown()


if __name__=="__main__":
    main()    