#!/bin/bash
# Point d'entrée du conteneur : source l'environnement ROS 2 puis lance le
# profil demandé (variable PROFILE) via le launcher, en mode non interactif.
set -e

source /opt/ros/jazzy/setup.bash
source /app/ws/install/setup.bash

cd /app

echo "=============================================="
echo " Plateforme UR3e — démarrage du profil : ${PROFILE}"
echo " Interface disponible sur http://localhost:1880/dashboard"
echo "=============================================="

exec python3 launcher.py "${PROFILE}"
