#!/usr/bin/python3

import time
import subprocess
import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from stem import SocketError
from stem.control import Controller

# Constants
TOR_PORT = 9051

# Check if Colorama has been already installed or not
try:
    from colorama import init, Fore
    print(Fore.LIGHTMAGENTA_EX + "Colorama has been already installed, We have initialized it for you :)")
    time.sleep(5)
except ImportError:
    print(Fore.RED + "Colorama has not been installed. Installing it...")
    subprocess.run(["pip", "install", "colorama"], check=True)
    from colorama import init, Fore
    print(Fore.LIGHTMAGENTA_EX + "Done, Colorama has been installed.")
    time.sleep(3)

# Clear the terminal screen
    os.system("clear")
    time.sleep(1)

def create_3d_banner():
    # Banner text
    banner_text = "YOUTUBE VIEWER"

    try:
        # Use figlet to create ASCII art with mono9 font
        figlet_process = subprocess.Popen(
            ["figlet", "-w", "36", "-f", "mono9", "-c", banner_text],
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
    subprocess.Popen(['service', 'tor', 'start'])

# Call the function to start Tor
start_tor()

def open_video(url, circuit):
    print(Fore.LIGHTYELLOW_EX + f"Opening video: {url} using Tor circuit: {circuit} in the background...")

    # Configure the headless Firefox browser
    options = Options()
    options.headless = True

    # Set up the Tor SOCKS proxy
    tor_proxy = "socks5://localhost:9050"  # Tor proxy address
    capabilities = webdriver.DesiredCapabilities.FIREFOX
    capabilities['proxy'] = {
        'proxyType': 'MANUAL',
        'httpProxy': tor_proxy,
        'ftpProxy': tor_proxy,
        'sslProxy': tor_proxy,
        'noProxy': ''  # bypass proxy for localhost
    }

    # Take user input for the path of Geckodriver
    executable_paths = input(Fore.LIGHTCYAN_EX + "Enter the path of Gecko Driver e.g., /path/to/geckodriver: ")

    # Create a headless Firefox browser instance
    browser = webdriver.Firefox(options=options, executable_path=executable_paths, capabilities=capabilities)

    try:
        # Open the URL in the background
        browser.get(url)

        # Simulate some interactions if needed
        # For example, you can wait for a few seconds
        time.sleep(5)

    finally:
        # Close the browser
        browser.quit()

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

                # Open the video in the background using the new Tor circuit
                open_video(video_url, circuit_name)

                # Watch the video for the specified duration
                watch_video(duration)
    except KeyboardInterrupt:
        pass  # User interrupted with Ctrl+C

    print(Fore.LIGHTMAGENTA_EX + "Exiting the script...")

if __name__ == "__main__":
    
    # Create 3D banner for showcase
    create_3d_banner()

    main()
