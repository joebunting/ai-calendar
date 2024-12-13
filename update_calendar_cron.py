import schedule
import time
import subprocess
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get log directory from environment
LOG_DIR = os.getenv('LOG_DIR', os.path.dirname(__file__))

# Set up logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'calendar_service.log'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def send_notification(title, message):
    """Send a Mac notification"""
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(message, title))

def update_calendar():
    try:
        # Log and notify start of update
        logging.info("Starting calendar update")
        send_notification("Calendar Update", "Starting calendar update...")
        
        # Run get-calendar.py first
        result = subprocess.run(['python3', 'get-calendar.py'], capture_output=True, text=True)
        if result.returncode != 0:
            error_msg = f"Error running get-calendar.py: {result.stderr}"
            logging.error(error_msg)
            send_notification("Calendar Update Error", error_msg)
            return
        logging.info(result.stdout.strip())
        
        # Then run calendar-to-openai.py
        result = subprocess.run(['python3', 'calendar-to-openai.py'], capture_output=True, text=True)
        if result.returncode != 0:
            error_msg = f"Error running calendar-to-openai.py: {result.stderr}"
            logging.error(error_msg)
            send_notification("Calendar Update Error", error_msg)
            return
        logging.info(result.stdout.strip())
        
        # Log and notify success
        success_msg = f"Calendar update completed at {datetime.now().strftime('%I:%M %p')}"
        logging.info(success_msg)
        send_notification("Calendar Update Success", success_msg)
        
    except Exception as e:
        error_msg = f"Error during calendar update: {str(e)}"
        logging.error(error_msg)
        send_notification("Calendar Update Error", error_msg)

def main():
    # Send startup notification
    send_notification("Calendar Update Service", "Calendar update service started")
    
    # Run once when started
    update_calendar()
    
    # Schedule to run every hour
    schedule.every().hour.do(update_calendar)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute for scheduled tasks

if __name__ == "__main__":
    print("Starting calendar update service...")
    print("Press Ctrl+C to stop")
    main() 