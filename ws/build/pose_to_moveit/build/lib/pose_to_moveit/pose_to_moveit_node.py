import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from moveit_msgs.srv import GetPositionIK
from std_msgs.msg import String


class PoseToMoveIt(Node):
    def __init__(self):
        super().__init__("pose_to_moveit")

        # Get target poses
        self.pose_sub = self.create_subscription(
            PoseStamped,
            "/target_pose",
            self.pose_callback,
            10
        )

        # To send trajectories to the controller
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            "/scaled_joint_trajectory_controller/joint_trajectory",
            10
        )

        # To send results back
        self.result_pub = self.create_publisher(
            String,
            "/move_result",
            10
        )

        # Send Inverse Kinematics requests to MoveIt
        self.ik_client = self.create_client(
            GetPositionIK,
            "/compute_ik"
        )

        self.get_logger().info("Waiting for /compute_ik...")

        self.ik_client.wait_for_service()

        self.get_logger().info("/compute_ik is available")
        self.get_logger().info("PoseToMoveIt READY")

    def publish_result(self, text):
        msg = String()
        msg.data = text
        self.result_pub.publish(msg)
        self.get_logger().info(f"Result: {text}")

    def pose_callback(self, pose_msg):
        self.get_logger().info(
            f"Target: "
            f"x={pose_msg.pose.position.x:.3f} "
            f"y={pose_msg.pose.position.y:.3f} "
            f"z={pose_msg.pose.position.z:.3f}"
        )

        req = GetPositionIK.Request()
        req.ik_request.group_name = "ur_manipulator"
        req.ik_request.ik_link_name = "tool0"
        req.ik_request.pose_stamped = pose_msg
        req.ik_request.avoid_collisions = True
        req.ik_request.timeout.sec = 2

        future = self.ik_client.call_async(req)
        future.add_done_callback(self.ik_response_callback)

    def ik_response_callback(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(
                f"IK service failed: {str(e)}"
            )
            self.publish_result(
                f"ERROR: IK service failed ({str(e)})"
            )
            return

        error_code = response.error_code.val

        if error_code != 1:
            self.get_logger().error(
                f"IK failed (error={error_code})"
            )
            # We return the error code as a string so that the web interface can display it
            self.publish_result(
                f"IK failed: {error_code}"
            )
            return

        joint_state = response.solution.joint_state
        traj = JointTrajectory()
        traj.joint_names = list(joint_state.name)
        point = JointTrajectoryPoint()
        point.positions = list(joint_state.position)
        point.time_from_start.sec = 3
        traj.points.append(point)

        self.traj_pub.publish(traj)

        self.get_logger().info(
            "Trajectory published"
        )

        self.publish_result(
            "SUCCESS"
        )


def main():
    rclpy.init()
    node = PoseToMoveIt()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()