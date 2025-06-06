from PySide6.QtWidgets import QMainWindow, QMenu,QWidget, QMessageBox, QLineEdit, QInputDialog

from PySide6.QtGui import QAction


from ui_pro import Ui_MainWindow
from connect_arm_widget import Ui_Form
import os
import  sys
import subprocess
import re



class ConnectArmWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Always start from stackedWidget_3(0)
        self.ui.stackedWidget_3.setCurrentIndex(0)

        # Disable all top buttons manually (except by code)
        for btn in [
            self.ui.pushButton,
            self.ui.pushButton_2,
            self.ui.pushButton_3,
            self.ui.pushButton_4,
            self.ui.pushButton_5,
            self.ui.pushButton_6
        ]:
            btn.setEnabled(False)
            btn.setCheckable(True)  # Needed to change icon to "on" image when checked

        

        # Connect flow buttons to next steps
        self.ui.congigureBtn.clicked.connect(self.config)
        self.ui.roscoreBtn.clicked.connect(self.roscore)
        self.ui.calibrateBtn.clicked.connect(self.calibrate)
        self.ui.launchdriverBtn.clicked.connect(self.driver)
        self.ui.launchmoveitBtn_2.clicked.connect(self.moveit)
        # Map UI buttons to actions
        

        self.ui.pushButton_7.clicked.connect(self.run_half_sphere)
        self.ui.pushButton_8.clicked.connect(self.run_plane)
        

    def config(self):

        pc_ip = self.get_full_ip(self.ui.PC_IP)
        if pc_ip is None:
            return self.ui.stackedWidget_3.setCurrentIndex(0)
        robot_ip = self.get_full_ip(self.ui.Robot_IP)

        if robot_ip is None:
            return self.ui.stackedWidget_3.setCurrentIndex(0)

        password, ok = QInputDialog.getText(self, "Sudo Password", "Enter your sudo password:", QLineEdit.EchoMode.Password)
        if not ok or not password:
            self.ui.output_box.append("Cancelled or no password entered.\n")
            return self.ui.stackedWidget_3.setCurrentIndex(0)

        self.ui.output_box.append(f"\n>>> Configuring IP for {pc_ip} and pinging {robot_ip}\n")

        command = f"ifconfig enp2s0 {pc_ip} netmask 255.255.255.0 up && ping -c 4 {robot_ip}"
        full_cmd = f"echo {password} | sudo -S bash -c \"{command}\""

        try:
            result = subprocess.run(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.ui.output_box.append(result.stdout)
            if result.stderr:
                self.ui.output_box.append(f"Error:\n{result.stderr}")
        except Exception as e:
            self.ui.output_box.append(f"Exception: {str(e)}\n")
            return

        self.ui.stackedWidget_3.setCurrentIndex(5)
        self.ui.pushButton.setChecked(True) 
        
    def roscore(self):

        pc_ip = self.get_full_ip(self.ui.PC_IP)
        robot_ip = self.get_full_ip(self.ui.Robot_IP)

        self.run_command("source /opt/ros/noetic/setup.bash && roscore", "Start ROS Core")
        

        self.ui.stackedWidget_3.setCurrentIndex(4)
        self.ui.pushButton_2.setChecked(True)
        
    def calibrate(self):

        pc_ip = self.get_full_ip(self.ui.PC_IP)
        robot_ip = self.get_full_ip(self.ui.Robot_IP)

        if not robot_ip:
            return

        cmd = f'''
        cd ~/new_ws && \
        source /opt/ros/noetic/setup.bash && \
        source devel/setup.bash && \
        roslaunch ur_calibration calibration_correction.launch \
        robot_ip:={robot_ip} \
        target_filename="$HOME/new_ws/src/Universal_Robots_ROS_Driver/ur_calibration/ur10e_calibration.yaml"
        '''
        self.run_command(cmd, "Launch Calibration")

        self.ui.stackedWidget_3.setCurrentIndex(3)
        self.ui.pushButton_3.setChecked(True)
        

    def driver(self):

        pc_ip = self.get_full_ip(self.ui.PC_IP)
        robot_ip = self.get_full_ip(self.ui.Robot_IP)

        if not robot_ip:
            return

        cmd = f'''
        cd ~/new_ws && \
        source /opt/ros/noetic/setup.bash && \
        source devel/setup.bash && \
        roslaunch ur_robot_driver ur10e_bringup.launch robot_ip:={robot_ip}
        '''
        self.run_command(cmd, "Launch Robot Driver")

        self.ui.stackedWidget_3.setCurrentIndex(2)
        self.ui.pushButton_4.setChecked(True)
        

    def moveit(self):
        pc_ip = self.get_full_ip(self.ui.PC_IP)
        robot_ip = self.get_full_ip(self.ui.Robot_IP)

        cmd = '''
        cd ~/new_ws && \
        source /opt/ros/noetic/setup.bash && \
        source devel/setup.bash && \
        roslaunch ur10e_moveit_config move_group.launch
        '''
        self.run_command(cmd, "Launch MoveIt")
        self.ui.stackedWidget_3.setCurrentIndex(1)
        self.ui.pushButton_5.setChecked(True)

   

    def get_full_ip(self, entry_field):
        ip_address = entry_field.text().strip()
    
    # Regex to validate IP address format
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    
    # Check if IP matches the pattern (three dots and four octets)
        if not re.match(ip_pattern, ip_address):
            QMessageBox.warning(self, "Invalid Input", "Invalid IP address format. Ensure there are 3 dots and 4 octets.")
            return
    
    # Split the IP by dots
        octets = ip_address.split(".")
    
    # Validate each octet is in the range of 0-255
        for octet in octets:
            if not octet.isdigit() or not (0 <= int(octet) <= 255):
                QMessageBox.warning(self, "Invalid Input", f"Each octet must be a number between 0 and 255. Invalid octet: {octet}")
                return
    
    # If all checks are passed, return the full IP address
        return f"192.168.1.{octets[3]}"

    def run_command(self, command, title=""):
        self.ui.terminal_1(f"\n>>> {title or command}\n")
        try:
            subprocess.Popen(
                ['gnome-terminal', '--', 'bash', '-i', '-c', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.ui.terminal_1(f"{title} launched in new terminal.\n")
        except Exception as e:
            self.ui.terminal_1(f"Error: {str(e)}\n")


    
        
       
    def run_plane(self):
        pc_ip = self.get_full_ip(self.ui.PC_IP)
        robot_ip = self.get_full_ip(self.ui.Robot_IP)

        cmd = '''
        cd ~/new_ws && \
        source /opt/ros/noetic/setup.bash && \
        source devel/setup.bash && \
        rosrun ur10e_moveit_config plane.py
        '''
        self.run_command(cmd, "Run plane.py")

    def run_half_sphere(self):
        pc_ip = self.get_full_ip(self.ui.PC_IP)
        robot_ip = self.get_full_ip(self.ui.Robot_IP)

        cmd = '''
        cd ~/new_ws && \
        source /opt/ros/noetic/setup.bash && \
        source devel/setup.bash && \
        rosrun ur10e_moveit_config half_sphere.py
        '''
        self.run_command(cmd, "Run half_sphere.py")

        



        


class MySideBar(QMainWindow,Ui_MainWindow, Ui_Form):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle("SideBar Menu")
            #menu button
            self.menuBtn.clicked.connect(self.toggle_menu)
            # Connect buttons to functions
            self.closeBtn.clicked.connect(self.close_window)
            self.minimizeBtn.clicked.connect(self.minimize_window)
            self.restoreBtn.clicked.connect(self.restore_window)
            #result button 
            self.helpBtn.clicked.connect(self.toggle_center_menu)

            self.pushButton.clicked.connect(self.close_center_menu)
            
            self.centerMenuContainer.setVisible(False)
            self.centralwidget.updateGeometry()

            #change page 
            

            self.connect_camera_sensorBtn.clicked.connect(lambda: self.switch_page(1))
            self.conntct_armBtn.clicked.connect(lambda: self.switch_page(2))
            self.calibrate_Btn.clicked.connect(lambda: self.switch_page(0))

            # Create and add the ConnectArmWidget to index 2 of stackedWidget_2
            self.connect_arm_page = ConnectArmWidget()
            self.stackedWidget_2.insertWidget(2, self.connect_arm_page)



            

        def close_window(self):
                self.close()

        def minimize_window(self):
                self.showMinimized()

        def restore_window(self):
            if self.isFullScreen():
                self.showNormal()
                self.is_maximized = False
            else:
                self.showFullScreen()
                self.is_maximized = True
        # menu logic
        def toggle_menu(self):
        # Get current width of the menu container
            current_width = self.leftMenuContainer.width()

        # Set the target width based on current state
            if current_width == 50:
                new_width = 212  # expanded
            else:
                new_width = 50   # collapsed

            self.leftMenuContainer.setFixedWidth(new_width)

     #result bar toogle

        def toggle_center_menu(self):
            if self.centerMenuContainer.isVisible():
                self.centerMenuContainer.setVisible(False)
            else:
                self.centerMenuContainer.setVisible(True)

        def close_center_menu(self):
            self.centerMenuContainer.setVisible(False)

        def switch_page(self, index):

            
            self.stackedWidget_2.setCurrentIndex(index)

        

          
       





             
            