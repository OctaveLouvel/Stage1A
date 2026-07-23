# Outils
## Node-red
`$ node-red -u node-red`
Permet de faire l'ihm avec un connection Ros directe

## Distrobox
`$ distrobox create --name ros-jazzy --image ubuntu:24.04`
Permet de créer une machine virtuelle simple qui tourne sous ubuntu pour faire tourner ros2

## ROS2
`$ source /opt/ros/jazzy/setup.zsh`
Dépend de votre shell pour l'extention, permet d'utiliser ros2 en ligne de commande

## UR ROS2 Drivers
`https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver`

```sh
sudo apt-get install ros-jazzy-ur
```


# Packets ROS2

Pour lancer les driver du robot et la connection à celui ci
```sh
ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur3e robot_ip:=0.0.0.0 use_mock_hardware:=true launch_rviz:=false
```

Ensuite pour lancer le simulateur movit
```sh
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur3e
```


Setup de la commande en force
```sh
source /opt/ros/jazzy/setup.zsh
colcon build
source install/setup.bash
```

Suite de commande pour faire la commande en force du robot
```sh
ros2 run ur_motion_manager teach_node
ros2 run ur_safety_monitor safety_monitor_node
ros2 run ur_force_controller force_controller_node
ros2 run ur_motion_manager motion_manager_node
```

```sh
ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur3e robot_ip:=0.0.0.0 use_mock_hardware:=true launch_rviz:=false
```


Pour faire tourner l'inverse kinematic
`ros2 run pose_to_moveit pose_to_moveit_node`

# Pour la camera Realsense
```zsh
sudo apt install ros-jazzy-librealsense2
sudo apt install ros-jazzy-realsense2-camera
git clone https://github.com/realsenseai/realsense-ros.git
rosdep install -i --from-path src --rosdistro jazzy --skip-keys=librealsense2 -y
```

To run it `ros2 run realsense2_camera realsense2_camera_node`

Pour afficher la caméra
`sudo apt install ros-jazzy-web-video-server`

```sh ros2
ros2 run web_video_server web_video_server
```
```sh
ros2 launch realsense2_camera rs_launch.py \
    enable_depth:=false \
    rgb_camera.profile:=240x240x2
```

# Pour le mapping avec RTABMAP

```sh
ros2 launch orbbec_camera astra2.launch.py \
    color_width:=800 color_height:=600 \
    depth_width:=800 depth_height:=600
```



```sh
ros2 launch realsense2_camera rs_launch.py \
    enable_accel:=true \
    enable_gyro:=true \
    rgb_camera.color_profile:=640x480x15 \
    depth_module.depth_profile:=640x480x15
```

```sh
ros2 launch rtabmap_launch rtabmap.launch.py \
    frame_id:=camera_link \
    rgb_topic:=/camera/camera/color/image_raw \
    depth_topic:=/camera/camera/depth/image_rect_raw \
    camera_info_topic:=/camera/camera/color/camera_info \
    approx_sync:=true
```

Parametres intrasect