#!/bin/bash

echo -e "Checking if the script is running as root!"

# Check if script is running as root user
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Please use 'sudo' along with the command or login as root user."
    sleep 1
    echo "Saving Preferences for next try!"
    sleep 7
    exit 1
fi

# Check if Colorama has been already installed or not
if python3 -c "import colorama" &>/dev/null; then
    echo -e "\033[95mColorama has been already installed, We have initialized it for you :)\033[0m"
    sleep 5
else
    echo -e "\033[91mColorama has not been installed. Installing it...\033[0m"
    pip install colorama
    echo -e "\033[95mDone, Colorama has been installed.\033[0m"
    sleep 3
fi


echo -e "\033[93m\nUpdating your system, wait!\n\033[0m"
sleep 0.5

# Update system
apt update

# Install pip
apt install python3-pip -y

echo -e "\033[96m\nInstalling required dependencies, wait!\n\033[0m"
sleep 0.5

# Install requirements to run the script
pip3 install stem
pip3 install selenium
apt install figlet lolcat tor -y

echo -e "\033[32m\nDone, run the 'main.py' file now!\n\033[0m"
echo -e "\033[95m\nNote that you need to download 'Gecko Driver' which is compatible with your Linux OS before using 'main.py'.\033[0m"
sleep 2

