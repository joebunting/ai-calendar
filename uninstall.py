#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    print("Uninstalling AI Calendar Launch Agent...")
    
    # Path to launch agent
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.user.calendarupdate.plist")
    
    # Check if launch agent exists
    if not os.path.exists(plist_path):
        print("Launch agent not found. Nothing to uninstall.")
        return
    
    # Unload the launch agent
    result = subprocess.run(['launchctl', 'unload', plist_path], capture_output=True)
    
    if result.returncode == 0:
        # Remove the plist file
        os.remove(plist_path)
        print("Successfully uninstalled the AI Calendar service!")
    else:
        print("Error unloading launch agent:", result.stderr.decode())
        sys.exit(1)

if __name__ == "__main__":
    main() 