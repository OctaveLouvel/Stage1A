#!/usr/bin/env python3

import os
import subprocess
import signal
import sys
import time

#####################################
#             SETTINGS
#####################################

# Tout est configurable par variable d'environnement (utilisé par Docker),
# avec les mêmes valeurs par défaut qu'auparavant pour un usage manuel en zsh.

SHELL = os.environ.get("LAUNCHER_SHELL", "zsh")

# Extension des fichiers de setup ROS selon le shell (zsh -> .zsh, sinon .bash)
_SETUP_EXT = "zsh" if SHELL == "zsh" else "bash"

ROS_SETUP = f"source /opt/ros/jazzy/setup.{_SETUP_EXT}"

WORKSPACE_SETUP = f"""
source /opt/ros/jazzy/setup.{_SETUP_EXT}
source ws/install/setup.{_SETUP_EXT}
"""

ROBOT_IP = os.environ.get("ROBOT_IP", "0.0.0.0")
USE_MOCK = os.environ.get("USE_MOCK", "true").lower() in ("1", "true", "yes", "on")

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
        ur_type:=ur3e \
        launch_rviz:=false
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
    ros2 launch realsense2_camera rs_launch.py \
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


_stop_handler = lambda s, f: (stop_all(), sys.exit(0))
signal.signal(signal.SIGINT, _stop_handler)
signal.signal(signal.SIGTERM, _stop_handler)   # arrêt propre via `docker stop`

#####################################
#             MENU
#####################################

profiles = list(PROFILES.keys())

# Profil passé en argument (par ex. par Docker) -> lancement non interactif.
# Accepte un numéro ("2") ou un nom exact ("Robot seul").
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.isdigit():
        choice = int(arg) - 1
    elif arg in profiles:
        choice = profiles.index(arg)
    else:
        print(f"Profil inconnu : {arg!r}")
        print("Profils disponibles :", ", ".join(profiles))
        sys.exit(1)
    selected = profiles[choice]
else:
    print()
    print("========== Launcher ==========")
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