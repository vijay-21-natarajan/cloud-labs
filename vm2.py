# vm2.py 
# ============================================================
# PART 2: SERVER CONSOLIDATION
# TASK 1: IMPLEMENT SERVER CONSOLIDATION STRATEGY
# ============================================================


# ------------------------------------------------------------
# STEP 1: OPEN VMWARE WORKSTATION AND IDENTIFY VMs
# ------------------------------------------------------------

# 1. Open VMware Workstation.

# 2. Check all available Virtual Machines.

# 3. For each VM:
#    Right Click VM
#    -> Edit Virtual Machine Settings

# 4. Check the following resources:
#    - Memory (RAM)
#    - Processors (CPU)
#    - Hard Disk (Storage)
#    - Network Adapter

# 5. Identify VMs having:
#    - Low CPU usage
#    - Low memory usage
#    - Redundant services
#    - Similar workloads
#    - Unnecessary services


# ------------------------------------------------------------
# STEP 2: SELECT A CONSOLIDATION HOST
# ------------------------------------------------------------

# Select one VM as the Consolidated VM.
#
# Example:
#
# VM1 -> Consolidated Server
# VM2 -> Server to be migrated
#
# The Consolidated VM must have enough:
#    - CPU
#    - RAM
#    - Storage
#
# to run both workloads.


# ------------------------------------------------------------
# STEP 3: CHECK CURRENT RESOURCE UTILIZATION
# ------------------------------------------------------------

# Run the following commands inside the Linux VM:

# Check CPU information:
# lscpu

# Check number of CPU cores:
# nproc

# Check memory usage:
# free -h

# Check disk usage:
# df -h

# Check IP address:
# hostname -I

# Monitor CPU and memory:
# top

# Optional: Install htop for better monitoring:
# sudo apt update
# sudo apt install htop -y

# Run:
# htop


# ------------------------------------------------------------
# STEP 4: ADJUST VM RESOURCES
# ------------------------------------------------------------

# Shut down the VM before changing major hardware settings:
#
# sudo shutdown now
#
# Then in VMware Workstation:
#
# Right Click VM
# -> Edit Virtual Machine Settings
#
# Adjust:
#    Memory -> Increase if required
#    Processors -> Increase if required
#
# Do NOT allocate all host RAM/CPU to the VM.
#
# Example:
#
# Host Laptop -> 8 GB RAM
# Consolidated VM -> 4 GB RAM
#
# Keep sufficient resources for the host OS.


# ------------------------------------------------------------
# STEP 5: INSTALL SERVICE ON VM2
# ------------------------------------------------------------

# Update Ubuntu packages:
# sudo apt update

# Install Apache Web Server:
# sudo apt install apache2 -y

# Start Apache:
# sudo systemctl start apache2

# Enable Apache at startup:
# sudo systemctl enable apache2

# Check Apache status:
# sudo systemctl status apache2


# ------------------------------------------------------------
# STEP 6: CREATE SAMPLE SERVICE/DATA ON VM2
# ------------------------------------------------------------

# Create a directory:
# sudo mkdir -p /var/www/html/consolidation

# Create the webpage:
# sudo nano /var/www/html/consolidation/index.html

# Add the following HTML:
#
# <h1>Server Consolidation Lab</h1>
# <p>This service has been migrated to the consolidated server.</p>

# Save the file:
# Ctrl + O
# Enter
# Ctrl + X

# Test the service:
# curl http://localhost/consolidation/


# ------------------------------------------------------------
# STEP 7: FIND VM2 IP ADDRESS
# ------------------------------------------------------------

# Run on VM2:
# hostname -I

# Example:
# 192.168.1.20

# Note down the IP address of VM2.


# ------------------------------------------------------------
# STEP 8: ENABLE SSH ON VM2
# ------------------------------------------------------------

# Install SSH server:
# sudo apt install openssh-server -y

# Start and enable SSH:
# sudo systemctl enable --now ssh

# Check SSH status:
# sudo systemctl status ssh


# ------------------------------------------------------------
# STEP 9: PREPARE CONSOLIDATED VM (VM1)
# ------------------------------------------------------------

# Start VM1.

# Update packages:
# sudo apt update

# Install Apache:
# sudo apt install apache2 -y

# Start Apache:
# sudo systemctl start apache2

# Enable Apache:
# sudo systemctl enable apache2

# Check status:
# sudo systemctl status apache2

# Create destination directory:
# sudo mkdir -p /var/www/html/consolidation


# ------------------------------------------------------------
# STEP 10: MIGRATE SERVICE FROM VM2 TO VM1
# ------------------------------------------------------------

# From VM1, copy the service from VM2:
#
# scp -r username@VM2_IP:/var/www/html/consolidation /tmp/
#
# Example:
#
# scp -r vijay@192.168.1.20:/var/www/html/consolidation /tmp/

# Enter the VM2 password when prompted.

# Copy the migrated service into Apache directory:
# sudo cp -r /tmp/consolidation /var/www/html/

# Restart Apache:
# sudo systemctl restart apache2

# Check Apache:
# sudo systemctl status apache2


# ------------------------------------------------------------
# STEP 11: VERIFY MIGRATED SERVICE
# ------------------------------------------------------------

# Test the migrated service:
# curl http://localhost/consolidation/

# Expected result:
#
# Server Consolidation Lab
# This service has been migrated to the consolidated server.
#
# If the webpage appears, migration was successful.


# ------------------------------------------------------------
# STEP 12: VALIDATE CONSOLIDATED VM RESOURCES
# ------------------------------------------------------------

# Check CPU:
# lscpu

# Check RAM:
# free -h

# Check disk:
# df -h

# Check running processes:
# top

# Or:
# htop

# Verify that CPU and memory usage are within acceptable limits.


# ------------------------------------------------------------
# STEP 13: POWER OFF ORIGINAL VM
# ------------------------------------------------------------

# After confirming the migrated service works on VM1,
# shut down VM2.

# On VM2:
# sudo shutdown now

# OR use VMware Workstation:
#
# Right Click VM2
# -> Power
# -> Shut Down Guest


# ------------------------------------------------------------
# STEP 14: DECOMMISSION UNUSED VM
# ------------------------------------------------------------

# In VMware Workstation:
#
# Right Click VM2
# -> Remove
#
# If you want to keep the VM files safely:
# Choose "Remove from Library".
#
# Do not permanently delete the VM until you are
# completely sure that the migrated service works.


# ============================================================
# PART 3: FAULT TOLERANCE
# TASK 1: IMPLEMENT FAULT-TOLERANT DESIGN
# ============================================================


# ------------------------------------------------------------
# STEP 1: CREATE A FULL CLONE OF PRIMARY VM
# ------------------------------------------------------------

# In VMware Workstation:
#
# Select Primary VM
# -> VM
# -> Manage
# -> Clone
#
# Select:
#    "The current state in the virtual machine"
#
# Select:
#    "Full Clone"
#
# Give the clone a name:
#    Backup-VM
#
# Click Finish.


# ------------------------------------------------------------
# STEP 2: START PRIMARY AND BACKUP VMs
# ------------------------------------------------------------

# Start both:
#
# Primary VM
# Backup VM


# ------------------------------------------------------------
# STEP 3: GIVE PRIMARY AND BACKUP DIFFERENT HOSTNAMES
# ------------------------------------------------------------

# On Primary VM:
# sudo hostnamectl set-hostname primary-server

# On Backup VM:
# sudo hostnamectl set-hostname backup-server

# Restart both VMs:
# sudo reboot


# ------------------------------------------------------------
# STEP 4: CHECK IP ADDRESSES
# ------------------------------------------------------------

# On Primary:
# hostname -I

# On Backup:
# hostname -I

# Example:
#
# Primary -> 192.168.1.10
# Backup  -> 192.168.1.11
#
# Make sure they have different IP addresses.


# ------------------------------------------------------------
# STEP 5: INSTALL RSYNC
# ------------------------------------------------------------

# Run on BOTH Primary and Backup VMs:

# sudo apt update

# sudo apt install rsync -y


# ------------------------------------------------------------
# STEP 6: ENABLE SSH ON BACKUP VM
# ------------------------------------------------------------

# On Backup VM:

# sudo apt install openssh-server -y

# sudo systemctl enable --now ssh

# Check:
# sudo systemctl status ssh


# ------------------------------------------------------------
# STEP 7: TEST CONNECTION FROM PRIMARY TO BACKUP
# ------------------------------------------------------------

# On Primary VM:

# ssh username@BACKUP_IP

# Example:
#
# ssh vijay@192.168.1.11

# Enter the Backup VM password.

# If connection is successful, exit:
# exit


# ------------------------------------------------------------
# STEP 8: CREATE IMPORTANT DATA ON PRIMARY VM
# ------------------------------------------------------------

# Create directory:
# mkdir -p ~/critical-data

# Create important file:
# echo "Important Server Data" > ~/critical-data/data.txt

# Check the file:
# cat ~/critical-data/data.txt


# ------------------------------------------------------------
# STEP 9: SYNCHRONIZE DATA USING RSYNC
# ------------------------------------------------------------

# Run on Primary VM:

# rsync -av ~/critical-data/ username@BACKUP_IP:~/critical-data/

# Example:
#
# rsync -av ~/critical-data/ vijay@192.168.1.11:~/critical-data/

# Enter Backup VM password if requested.


# ------------------------------------------------------------
# STEP 10: VERIFY DATA ON BACKUP VM
# ------------------------------------------------------------

# Connect to Backup:
# ssh vijay@192.168.1.11

# Check directory:
# ls ~/critical-data

# Check file:
# cat ~/critical-data/data.txt

# Expected:
#
# Important Server Data


# ------------------------------------------------------------
# STEP 11: MODIFY DATA ON PRIMARY
# ------------------------------------------------------------

# Exit Backup:
# exit

# On Primary, add new data:
# echo "New Data Added" >> ~/critical-data/data.txt

# Check:
# cat ~/critical-data/data.txt


# ------------------------------------------------------------
# STEP 12: SYNCHRONIZE AGAIN
# ------------------------------------------------------------

# Run on Primary:

# rsync -av ~/critical-data/ vijay@192.168.1.11:~/critical-data/


# ------------------------------------------------------------
# STEP 13: VERIFY UPDATED DATA ON BACKUP
# ------------------------------------------------------------

# Connect to Backup:
# ssh vijay@192.168.1.11

# Check:
# cat ~/critical-data/data.txt

# Expected:
#
# Important Server Data
# New Data Added


# ============================================================
# SNAPSHOT / QUICK RECOVERY
# ============================================================


# ------------------------------------------------------------
# STEP 14: TAKE VM SNAPSHOT
# ------------------------------------------------------------

# In VMware Workstation:
#
# Select Primary VM
# -> VM
# -> Snapshot
# -> Take Snapshot
#
# Snapshot Name:
#    Pre-Consolidation Snapshot
#
# Description:
#    Snapshot before major configuration changes.
#
# Click:
#    Take Snapshot


# ------------------------------------------------------------
# STEP 15: VERIFY SNAPSHOT
# ------------------------------------------------------------

# In VMware Workstation:
#
# VM
# -> Snapshot
# -> Snapshot Manager
#
# Verify that:
#
# Pre-Consolidation Snapshot
#
# is present.


# ============================================================
# FINAL VALIDATION
# ============================================================

# PART 2:
#
# 1. Service was running on VM2.
# 2. Service was copied to VM1.
# 3. Service was started on VM1.
# 4. Service was successfully tested on VM1.
# 5. VM2 was powered off.
# 6. VM2 was decommissioned.
# 7. CPU and RAM usage were checked on VM1.


# PART 3:
#
# 1. Primary VM was cloned.
# 2. Backup VM was created using Full Clone.
# 3. Primary and Backup have different hostnames/IPs.
# 4. rsync was installed.
# 5. Data was synchronized from Primary to Backup.
# 6. Updated data was synchronized again.
# 7. VMware Snapshot was created.
# 8. Snapshot can be used for quick recovery.


# ============================================================
# IMPORTANT COMMANDS FOR LAB EXAM
# ============================================================

# Resource Monitoring:
# lscpu
# nproc
# free -h
# df -h
# hostname -I
# top
# htop

# Apache:
# sudo apt update
# sudo apt install apache2 -y
# sudo systemctl start apache2
# sudo systemctl enable apache2
# sudo systemctl status apache2
# sudo systemctl restart apache2

# SSH:
# sudo apt install openssh-server -y
# sudo systemctl enable --now ssh
# sudo systemctl status ssh

# Service Migration:
# scp -r username@VM2_IP:/var/www/html/consolidation /tmp/
# sudo cp -r /tmp/consolidation /var/www/html/
# curl http://localhost/consolidation/

# Fault Tolerance:
# sudo hostnamectl set-hostname primary-server
# sudo hostnamectl set-hostname backup-server
# sudo apt install rsync -y
# mkdir -p ~/critical-data
# echo "Important Server Data" > ~/critical-data/data.txt
# rsync -av ~/critical-data/ username@BACKUP_IP:~/critical-data/
# ssh username@BACKUP_IP
# cat ~/critical-data/data.txt

# Shutdown:
# sudo shutdown now

# Reboot:
# sudo reboot