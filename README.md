# GUI-Development-for-Multi-sensor-Calibration-on-Drones
This repository contains the PyQt-based graphical user interface (GUI) for a multi-sensor calibration system. It is designed to interact with a ROS 2 backend, which handles the calibration logic and remains part of a private project. The goal here is to create a user-friendly interface for visualizing and managing sensor calibration workflows.

# My PySide6 Project

This is a basic project using **PySide6** (Qt for Python) to build a desktop GUI application.
## 🛠️ Requirements

- Python 3.7+
- PySide6
- Access to drone hardware with:
  - One or more cameras
  - sensors like IMU and LiDAR 
  - UR10e robotic arm (Ethernet connection)


## Installation

First, make sure you have Python installed. Then install the required dependency:


<pre>
```bash
pip install PySide6

</pre>


## 📁 Project Structure & Description

The application is organized into the following three main sections:

### 1. Connect Camera and Sensors
This section handles:
- Initializing the camera feed
- Connecting to environmental or positional sensors
- Displaying real-time data from sensors
- Managing connection status and error handling for input devices

### 2. Connect the Arm
This part is responsible for:
- Establishing communication with a robotic arm UR10e for now
- Sending commands and receiving feedback from the arm
- Enabling manual or automatic control of the arm from the UI

### 3. Calibrate
This section helps with:
- Calibrating the robotic arm alignment with the drone's body
- Adjusting for sensor offsets, positional drift, and camera perspective
- Running calibration routines to ensure precise and synchronized movement


### 🔍 Result Section
At the bottom of the interface:
- Displays the final processed data
- Shows status indicators, success/failure messages, and logs
- May include export or save options for the results

---
---

## 🚫 Limitations & Access Notice

> ⚠️ **Important:**  
This repository **only includes the GUI portion** of the system.  
The **backend logic for arm motion, sensor calibration, and hardware control (developed using ROS 2)** is **not included** and **not publicly available**.

This means:

- You **can explore the full GUI**, see how components are structured, and how the UI is designed.
- However, **you will not be able to execute any real calibration or robotic arm control**, unless you have access to the proprietary backend implementation.

---


