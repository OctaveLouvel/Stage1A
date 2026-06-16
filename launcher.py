#!/usr/bin/env python3

import subprocess
import signal
import sys
import time

#####################################
#             SETTINGS
#####################################

SHELL = "zsh"

ROS_SETUP = "source /opt/ros/jazzy/setup.zsh"

WORKSPACE_SETUP = """
source /opt/ros/jazzy/setup.zsh
source ws/install/setup.zsh
"""

ROBOT_IP = "0.0.0.0"
USE_MOCK = True

#####################################
#         COMMANDES
#####################################

COMMANDS = {

    "NodeRed": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    node-red -u node-red
    """,

    "UR Driver": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 launch ur_robot_driver ur_control.launch.py \
        ur_type:=ur3e \
        robot_ip:={ROBOT_IP} \
        use_mock_hardware:={str(USE_MOCK).lower()} \
        launch_rviz:=false
    """,

    "MoveIt": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 launch ur_moveit_config ur_moveit.launch.py \
        ur_type:=ur3e
    """,

    "PoseToMoveIt": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 run pose_to_moveit pose_to_moveit_node
    """,

    "Teach Node": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 run ur_motion_manager teach_node
    """,

    "Safety Monitor": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 run ur_safety_monitor safety_monitor_node
    """,

    "Force Controller": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 run ur_force_controller force_controller_node
    """,

    "Motion Manager": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 run ur_motion_manager motion_manager_node
    """,

    "RealSense": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 launch realsense2_camerars_launch.py \
        enable_accel:=true \
        enable_gyro:=true \
        rgb_camera.color_profile:=640x480x15 \
        depth_module.depth_profile:=640x480x15
    """,

    "Web Video Server": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 run web_video_server web_video_server
    """,

    "Astra2": f"""
    {ROS_SETUP}
    {WORKSPACE_SETUP}
    ros2 launch orbbec_camera astra2.launch.py \
        color_width:=800 color_height:=600 \
        depth_width:=800 depth_height:=600
    """
}

#####################################
#      PROFILS DE LANCEMENT
#####################################

PROFILES = {

    "NodeRed seul": [
        "NodeRed"
    ],

    "Robot seul": [
        "NodeRed",
        "UR Driver",
        "MoveIt",
        "PoseToMoveIt"
    ],

    "Commande en force": [
        "NodeRed",
        "UR Driver",  
        "Safety Monitor",
        "Force Controller",
        "Motion Manager",
        "Teach Node"
    ],

    "RealSense": [
        "NodeRed",
        "RealSense",
        "Web Video Server"
    ],

    "Astra2": [
        "NodeRed",
        "Astra2",
        "Web Video Server"
    ],

    "Tout": [
        "NodeRed",
        "UR Driver",
        "MoveIt",
        "PoseToMoveIt",
        "Astra2",
        "RealSense"
    ]

}

#####################################
#      LANCEMENT PROCESSUS
#####################################

processes = []

def launch(command):

    cmd = f"""
{command}
"""

    p = subprocess.Popen(
        [SHELL, "-c", cmd],
    )

    processes.append(p)


def stop_all():

    print("\nArrêt des processus...")

    for p in processes:
        try:
            p.terminate()
        except:
            pass

    time.sleep(1)

    for p in processes:
        try:
            p.kill()
        except:
            pass


signal.signal(signal.SIGINT, lambda s, f: (
    stop_all(),
    sys.exit(0)
))

#####################################
#             MENU
#####################################

print()
print("========== Launcher ==========")

profiles = list(PROFILES.keys())

for i, name in enumerate(profiles):
    print(f"[{i+1}] {name}")

print()

choice = int(input("> ")) - 1

selected = profiles[choice]

print(f"\nLancement du profil : {selected}\n")

for cmd in PROFILES[selected]:

    print(f"-> {cmd}")

    launch(COMMANDS[cmd])

print("\nTous les processus sont lancés.")
print("Ctrl+C pour arrêter.")

while True:
    time.sleep(1)