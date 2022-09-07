#!/usr/bin/env python3
"""
Module Docstring
"""
__author__ = "Aniket Chadalavada"
__version__ = "1.0.0"
__license__ = "MIT"

import requests
import time
from commands import Commands
import os

TITLE = r""" $$$$$$\          $$$$$$\                                  $$\                         
$$  __$$\        $$  __$$\                                 $$ |                        
$$ /  $$ |       $$ /  \__| $$$$$$$\  $$$$$$\  $$\   $$\ $$$$$$\    $$$$$$\   $$$$$$\  
$$ |  $$ |$$$$$$\\$$$$$$\  $$  _____|$$  __$$\ $$ |  $$ |\_$$  _|  $$  __$$\ $$  __$$\ 
$$ |  $$ |\______|\____$$\ $$ /      $$ /  $$ |$$ |  $$ |  $$ |    $$$$$$$$ |$$ |  \__|
$$ $$\$$ |       $$\   $$ |$$ |      $$ |  $$ |$$ |  $$ |  $$ |$$\ $$   ____|$$ |      
\$$$$$$ /        \$$$$$$  |\$$$$$$$\ \$$$$$$  |\$$$$$$  |  \$$$$  |\$$$$$$$\ $$ |      
 \___$$$\         \______/  \_______| \______/  \______/    \____/  \_______|\__|      
     \___|"""

API_BASE = "http://theorangealliance.org/api"

def parse_config():
    """
    Parses config file for (and returns) API Key
    """
    # Create data directory if it doesn't exist
    os.mkdir("data") if not os.path.exists("data") else None
    # Create config file if it doesn't exist
    try:
        with open("./data/.config", "r") as config_file:
            content = config_file.read()
            if "api_key = " not in content:
                raise FileNotFoundError
            return content.split("api_key = ")[1]
    except FileNotFoundError:
        print("\t\tGenerating Config File...")
        with open("./data/.config", "w+") as config_file:
            key = input("\t\tNo API Key Found in Config File, Enter API Key:\n")
            if len(key) != 64:
                print("\t\tKey Invalid, Must be 64 Characters.")
                exit()
            config_file.write(f"api_key = {key}")
            # Return Api Key
            return key

def initialize():
    """
    Initializes the program and does checks
    """
    global HEADERS, SEASON, COMMAND_LIST
    print("\tAccessing API Key...")
    # Get API Key and Write to Headers
    HEADERS = {
    "Content-Type": "application/json",
    "X-TOA-Key": parse_config(), # Returns API Key
    "X-Application-Origin": "Quantitative-Scouter"
    }

    # Test API Access
    print("\tVerifying API Access...")
    try:
        if "The supplied API key was not found." in requests.get(API_BASE, headers=HEADERS).text:
            print("API Key Invalid.")
            exit()
    except requests.exceptions.ConnectionError:
        print("Connection Error.")
        exit()

    # Get Current Season
    print("\tFetching Current Season...")
    seasons = requests.get(f"{API_BASE}/seasons", headers=HEADERS).json()
    if seasons[-1]['is_active']:
        SEASON = seasons[-1]['season_key']
        name = seasons[-1]['description']
    else:
        SEASON = seasons[-2]['season_key']
        name = seasons[-2]['description']

    # Initialize Commands
    print("\tInitializing Commands...")
    commands = Commands(SEASON, API_BASE, HEADERS)
    COMMAND_LIST = {'help': commands.help, 'exit': commands.exit, 'versus': commands.versus}

    return name
    

def title_screen():
    """
    Prints Title Screen
    """
    for line in TITLE.split('\n'):
        time.sleep(0.1)
        print(line)
    print("------------------------")
    

def print_details(name, season):
    """
    Prints Debug Details
    """
    print("------------------------")
    print(f'Operating in Season "{name}" ({season}).')
    print("------------------------")

def process_command(command):
    """
    Processes Commands w/ Commands Class"""
    try:
        COMMAND_LIST[command]()
    except KeyError:
        print("Invalid Command.")

def main():
    """
    Main Program
    """
    title_screen()

    print("Initializing...")
    name = initialize()
    print("Initialization Complete!")

    print_details(name, SEASON)

    print('Type "help" for a list of commands.')
    while True:
        process_command(input(">>> "))
            


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()