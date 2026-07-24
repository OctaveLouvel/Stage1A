# Image tout-en-un : ROS 2 Jazzy + driver UR + MoveIt + caméras + Node-RED
# Construite à partir de l'image officielle ROS 2 Jazzy (base légère).
FROM ros:jazzy-ros-base

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# ---------------------------------------------------------------------------
# 1. Dépendances système + paquets ROS 2 (driver UR, MoveIt, caméras, outils)
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        python3-colcon-common-extensions \
        python3-rosdep \
        ros-jazzy-ur-robot-driver \
        ros-jazzy-ur-description \
        ros-jazzy-ur-moveit-config \
        ros-jazzy-realsense2-camera \
        ros-jazzy-orbbec-camera \
        ros-jazzy-orbbec-description \
        ros-jazzy-web-video-server \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# 2. Node.js 22 (requis par Node-RED) + Node-RED
# ---------------------------------------------------------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g node-red \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---------------------------------------------------------------------------
# 3. Compilation du workspace ROS 2 (uniquement les paquets du projet ;
#    les sources caméra sont exclues via .dockerignore, fournies par apt)
# ---------------------------------------------------------------------------
COPY ws/ ws/
RUN source /opt/ros/jazzy/setup.bash \
    && cd ws \
    && rosdep install --from-paths src --ignore-src -y --rosdistro jazzy || true \
    && colcon build --symlink-install

# ---------------------------------------------------------------------------
# 4. Dépendances Node-RED (nœuds ROS 2 + dashboard)
# ---------------------------------------------------------------------------
COPY node-red/ node-red/
RUN source /opt/ros/jazzy/setup.bash \
    && source ws/install/setup.bash \
    && cd node-red \
    && npm install

# ---------------------------------------------------------------------------
# 5. Reste du projet + point d'entrée
# ---------------------------------------------------------------------------
COPY launcher.py ./
COPY fanuc/ fanuc/
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Valeurs par défaut : interface seule (démarrage fiable, sans matériel).
# Surchargées par docker-compose.yml (PROFILE, USE_MOCK, ROBOT_IP).
ENV LAUNCHER_SHELL=bash \
    ROBOT_IP=0.0.0.0 \
    USE_MOCK=true \
    PROFILE="NodeRed seul"

# 1880 = interface Node-RED, 8080 = flux vidéo (web_video_server)
EXPOSE 1880 8080

ENTRYPOINT ["/entrypoint.sh"]
