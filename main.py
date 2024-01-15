#!/usr/bin/python3

import sys
import os
import subprocess
import time
import webbrowser
from colorama import init, Fore
from stem import SocketError
from stem.control import Controller

# Constants
TOR_PORT = 9051

def create_3d_banner():
    # Banner text
    banner_text = "YOUTUBE VIEWER"

    try:
        # Use figlet to create ASCII art with mono9 font
        figlet_process = subprocess.Popen(
            ["figlet", "-f", "mono9", banner_text],
            stdout=subprocess.PIPE
        )
        figlet_output, _ = figlet_process.communicate()

        # Use lolcat to add color to the ASCII art
        lolcat_process = subprocess.Popen(["lolcat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        banner_output, _ = lolcat_process.communicate(input=figlet_output)

        # Print the result
        print(banner_output.decode("utf-8"))

    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + "Error: Make sure 'figlet' and 'lolcat' are installed on your system. (Hint: Run ./setup.sh)")
        time.sleep(2)

def is_tor_running():
    try:
        print(Fore.LIGHTYELLOW_EX + "Checking if Tor is already running or not!")
        # Check if the Tor service is running by attempting to create a controller
        with Controller.from_port(port=TOR_PORT) as controller:
            controller.authenticate()
            return True
    except SocketError:
        return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"An error occurred: {e}")
        return False

def start_tor():
    # Start the Tor service
    subprocess.Popen(['tor'])

def open_video(url, circuit):
    print(Fore.LIGHTYELLOW_EX + "Opening default browser using Tor...")
    # Open the video URL in the default web browser using the provided Tor circuit
    webbrowser.get(using='tor_browser').open(url, new=2, autoraise=True)

def watch_video(duration):
    # Wait for the specified duration
    time.sleep(duration)

def main():
    # Check if Tor is already running, if not, start it
    if not is_tor_running():
        print(Fore.LIGHTYELLOW_EX + "Starting Tor service...")
        start_tor()
        time.sleep(8)  # Wait for Tor to start
    
    try:
        while True:
            # Take user input for video URL
            video_url = input(Fore.LIGHTCYAN_EX + "Enter the video URL (or 'quit' to exit): ")

            if video_url.lower() == 'quit':
                print(Fore.LIGHTMAGENTA_EX + "If you liked this script, please consider sharing it with your friends and also giving a star to this repo :)")
                break

            # Take user input for time duration
            try:
                duration = float(input(Fore.LIGHTMAGENTA_EX + "Enter the time duration to watch the video (in seconds): "))
            except ValueError:
                print(Fore.LIGHTRED_EX + "Invalid input. Please enter a valid duration in seconds.")
                continue

            # Take user input for the number of tabs to open
            try:
                num_tabs = int(input(Fore.LIGHTYELLOW_EX + "Enter the number of tabs to open: "))
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid number of tabs.")
                continue

            # Open the video in multiple tabs with different Tor circuits
            for tab_number in range(1, num_tabs + 1):
                circuit_name = f"tab_circuit_{tab_number}"
                with Controller.from_port(port=TOR_PORT) as controller:
                    controller.authenticate()
                    controller.new_circuit(circuit_name, await_build=True)
                    controller.close_circuit(circuit_name)

                # Open the video in the default web browser using the new Tor circuit
                open_video(video_url, circuit_name)

                # Watch the video for the specified duration
                watch_video(duration)
    except KeyboardInterrupt:
        pass  # User interrupted with Ctrl+C

    print(Fore.LIGHTMAGENTA_EX + "Exiting the script...")

if __name__ == "__main__":
    # Initialize colorama
    init(autoreset=True)

    # Clear the terminal screen
    os.system("clear")
    time.sleep(1)

    # Create 3D banner for showcase
    create_3d_banner()

    main()
