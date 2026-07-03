<a id="readme-top"></a>



<!-- PROJECT PRESENTATION -->
<br/>
<div align="center">
<h3 align="center">UR3e Robot Control with Node Red and ROS2</h3>
  <p align="center">
    A implementaion of node red and ros2 for controlling a UR3e robot with MoveIt and a force controller and more.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is a ROS2 workspace that contains several packages for controlling a UR3e robot with MoveIt and a force controller. 2 different node red flows are provided. It also contains packages for connecting to different sensors such as RealSense and Orbbec cameras. The main aspect of the project is it's use for learning. You can add your own nodes and use the Node Red interface to connect them together.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Node red and ros2 are required for this project. You can also add the UR3e robot and a RealSense or Orbbec camera to the project. The project is designed to be used with a UR3e robot, but it can be adapted to work with other robots as well. The vidéo playback on Node Red is done with the help of the ros2 web video server package.

### Prerequisites

You will need the following software installed:

* Node.js
```sh
sudo apt install nodejs npm
```

* Node Red
```sh
sudo npm install -g node-red
```
* ros2
  [See this link for more detailed instructions](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

```sh
sudo apt install software-properties-common
sudo add-apt-repository universe
```

```sh
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install ros-jazzy-desktop
sudo apt install python3-colcon-common-extensions
```

* UR ros2 driver
```sh
sudo apt install ros-jazzy-ur-robot-driver ros-jazzy-ur-description
```

* RealSense ros2 driver
```sh
sudo apt install ros-jazzy-realsense2-camera
```
[See this link for more detailed instructions](https://github.com/realsenseai/realsense-ros)

* Orbbec ros2 driver
```sh
sudo apt install ros-jazzy-orbbec-camera ros-jazzy-orbbec-description
```
  [See this link for more detailed instructions](https://github.com/orbbec/OrbbecSDK_ROS2)

* Ros Video Server
```sh
sudo apt install ros-jazzy-web-video-server
```
* Rosdep
```sh
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

* MoveIt
```sh
git clone -b jazzy https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git
```


### Installation

1. Clone the repo
```sh
git clone https://github.com/OctaveLouvel/Stage1A.git
```

* MoveIt
```sh
git clone -b jazzy https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git
```

3. Build the workspace
```sh
cd ws/src
git clone -b jazzy https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git
cd ..
sudo apt update && rosdep install -r --from-paths . --ignore-src --rosdistro jazzy -y
source /opt/ros/jazzy/setup.zsh # or bash depending on your shell 
colcon build --symlink-install
source install/setup.zsh # or bash depending on your shell
cd ..
```

2. Install NPM packages for node red
```sh
# You need to have add sourced the ROS2 workspace before running this command
cd node-red
npm install
cd ..
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

You can use this project to connect different ROS2 nodes with the help of Node Red. You can also use it to control a UR3e robot with MoveIt and a force controller. But the main aspect of the project is it's use for learning. Add your nodes and use the Node Red interface to connect them together. You can also use the included nodes to control the robot and visualize the data from the sensors.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Feel free to contribute to this project by adding features or fixing bugs! For example if you wan't to add new ros2 packages to the project, you can do this by following these steps:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Octave Louvel - octavelouvel@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/OctaveLouvel/Stage1A.svg?style=for-the-badge
[contributors-url]: https://github.com/OctaveLouvel/Stage1A/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/OctaveLouvel/Stage1A.svg?style=for-the-badge
[forks-url]: https://github.com/OctaveLouvel/Stage1A/network/members
[stars-shield]: https://img.shields.io/github/stars/OctaveLouvel/Stage1A.svg?style=for-the-badge
[stars-url]: https://github.com/OctaveLouvel/Stage1A/stargazers
[issues-shield]: https://img.shields.io/github/issues/OctaveLouvel/Stage1A.svg?style=for-the-badge
[issues-url]: https://github.com/OctaveLouvel/Stage1A/issues
[license-shield]: https://img.shields.io/github/license/OctaveLouvel/Stage1A.svg?style=for-the-badge
[license-url]: https://github.com/OctaveLouvel/Stage1A/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
