#!/bin/bash

echo -e "Checking if the script is running as root!"

# Check if script is running as root user
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Please use 'sudo' or login as root."
    exit 1
fi

echo -e "\nUpdating your system, please wait\n"
sleep 0.5

# Update system
apt update

# Install pip
apt install python3-pip -y

echo -e "\nInstalling required dependencies, please wait!\n"
sleep 0.5

# Install requirements to run the script
pip3 install stem
pip3 install selenium
apt install figlet lolcat tor -y

echo -e "\nDone, run the 'main.py' file now!\n"
echo -e "\nNote that you need to download 'Gecko Driver' which is compatible with your Linux OS before using 'main.py'."
sleep 2

