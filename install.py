#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import subprocess
from pathlib import Path
import sys

def create_plist_content(paths):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.calendarupdate</string>
    <key>ProgramArguments</key>
    <array>
        <string>{paths['PYTHON_PATH']}</string>
        <string>{paths['SCRIPT_DIR']}/update_calendar_cron.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{paths['SCRIPT_DIR']}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardErrorPath</key>
    <string>{paths['LOG_DIR']}/calendar_service.log</string>
    <key>StandardOutPath</key>
    <string>{paths['LOG_DIR']}/calendar_service.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/Library/Frameworks/Python.framework/Versions/3.13/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>PYTHONPATH</key>
        <string>{paths['SCRIPT_DIR']}</string>
        <key>DOTENV_PATH</key>
        <string>{paths['SCRIPT_DIR']}/.env</string>
        <key>LANG</key>
        <string>en_US.UTF-8</string>
        <key>LC_ALL</key>
        <string>en_US.UTF-8</string>
        <key>HOME</key>
        <string>{os.path.expanduser('~')}</string>
        <key>OPENAI_API_KEY</key>
        <string>{os.getenv('OPENAI_API_KEY')}</string>
    </dict>
</dict>
</plist>
'''

def main():
    print("Installing AI Calendar Launch Agent...")
    
    # Load environment variables
    load_dotenv()
    
    # Get paths from environment
    paths = {
        'PYTHON_PATH': os.getenv('PYTHON_PATH'),
        'SCRIPT_DIR': os.getenv('SCRIPT_DIR'),
        'LOG_DIR': os.getenv('LOG_DIR')
    }
    
    # Verify all paths exist
    for key, path in paths.items():
        if not path:
            print(f"Error: {key} not found in .env file")
            sys.exit(1)
    
    # Create logs directory if it doesn't exist
    os.makedirs(paths['LOG_DIR'], exist_ok=True)
    
    # Create LaunchAgents directory if it doesn't exist
    launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
    os.makedirs(launch_agents_dir, exist_ok=True)
    
    # Generate and write plist file
    plist_path = os.path.join(launch_agents_dir, "com.user.calendarupdate.plist")
    with open(plist_path, 'w') as f:
        f.write(create_plist_content(paths))
    
    # Set correct permissions
    os.chmod(plist_path, 0o644)
    
    # Unload existing launch agent if it exists
    subprocess.run(['launchctl', 'unload', plist_path], capture_output=True)
    
    # Load the new launch agent
    result = subprocess.run(['launchctl', 'load', '-w', plist_path], capture_output=True)
    
    if result.returncode == 0:
        print("Successfully installed and started the AI Calendar service!")
        print(f"Logs will be written to: {paths['LOG_DIR']}")
    else:
        print("Error loading launch agent:", result.stderr.decode())
        sys.exit(1)

if __name__ == "__main__":
    main() 