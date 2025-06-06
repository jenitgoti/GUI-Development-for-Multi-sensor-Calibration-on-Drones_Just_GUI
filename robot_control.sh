#!/bin/bash

ACTION=$1
PC_IP=$2
ROBOT_IP=$3
$SUDO_PASS=$4
source /opt/ros/noetic/setup.bash

case $ACTION in
  config_ip)
    echo -e "\n>>> Configuring IP for $PC_IP and pinging $ROBOT_IP"

   
    ifconfig enp2s0 "$PC_IP" netmask 255.255.255.0 up
    ping "$ROBOT_IP"

    ;;
  
  start_roscore)
    echo -e "\n>>> Starting ROS Core"
    roscore
    ;;

  calibrate_robot)
    echo -e "\n>>> Launching Calibration"
    cd ~/new_ws
    source devel/setup.bash
    roslaunch ur_calibration calibration_correction.launch \
      robot_ip:=$ROBOT_IP \
      target_filename="$HOME/new_ws/src/Universal_Robots_ROS_Driver/ur_calibration/ur10e_calibration.yaml"
    ;;

  launch_driver)
    echo -e "\n>>> Launching Robot Driver"
    cd ~/new_ws
    source devel/setup.bash
    roslaunch ur_robot_driver ur10e_bringup.launch robot_ip:=$ROBOT_IP
    ;;

  launch_moveit)
    echo -e "\n>>> Launching MoveIt"
    cd ~/new_ws
    source devel/setup.bash
    roslaunch ur10e_moveit_config move_group.launch
    ;;

  run_plane)
    echo -e "\n>>> Running plane.py"
    cd ~/new_ws
    source devel/setup.bash
    rosrun ur10e_moveit_config plane.py
    ;;

  run_half_sphere)
    echo -e "\n>>> Running half_sphere.py"
    cd ~/new_ws
    source devel/setup.bash
    rosrun ur10e_moveit_config half_sphere_2.py
    ;;

  *)
    echo "Unknown action: $ACTION"
    exit 1
    ;;
esac
