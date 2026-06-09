#!/usr/bin/env bash

# Load ROS 2
source /opt/ros/jazzy/setup.bash

# Send joint trajectory
ros2 topic pub --once \
/scaled_joint_trajectory_controller/joint_trajectory \
trajectory_msgs/msg/JointTrajectory "{
  joint_names: [
    elbow_joint,
    shoulder_lift_joint,
    shoulder_pan_joint,
    wrist_1_joint,
    wrist_2_joint,
    wrist_3_joint
  ],
  points: [
    {
      positions: [
        0.5309880415545862,
       -1.488652915959694,
        0.2993168234825134,
       -0.22730668008837895,
       -1.7598522345172327,
       -3.5968595186816614
      ],
      time_from_start: {sec: 0}
    },
    {
      positions: [
        0.5309880415545862,
       -1.488652915959694,
        0.3193168234825134,
       -0.22730668008837895,
       -1.7598522345172327,
       -3.5968595186816614
      ],
      time_from_start: {sec: 4}
    }
  ]
}"
