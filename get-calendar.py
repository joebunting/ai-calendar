import requests
from icalendar import Calendar
import json
from datetime import datetime, timedelta, timezone
from dateutil.rrule import rrulestr
from dateutil.parser import parse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_event_description(summary, start_time, end_time, location, description):
    """Create a natural language description of the event"""
    # Convert times to more readable format
    start = datetime.fromisoformat(start_time).strftime("%A, %B %d, %Y at %I:%M %p")
    end = datetime.fromisoformat(end_time).strftime("%I:%M %p") if end_time else "no end time specified"
    
    text = f"Event: {summary} on {start}"
    if end_time:
        text += f" until {end}"
    if location:
        text += f". Location: {location}"
    if description:
        text += f". Details: {description}"
    
    return text

def get_calendar(ical_url):
    response = requests.get(ical_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to download calendar: {response.status_code}")
    
    cal = Calendar.from_ical(response.text)
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    
    events = []
    for component in cal.walk('VEVENT'):
        start = component.get('dtstart').dt
        
        # Handle recurring events
        if component.get('rrule'):
            # Get recurrence rule
            rrule = component.get('rrule')
            # Make sure start time is timezone-aware
            if isinstance(start, datetime):
                if start.tzinfo is None:
                    start = start.replace(tzinfo=timezone.utc)
            else:
                start = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc)
            
            # Convert to dateutil rrule
            rule = rrulestr(rrule.to_ical().decode('utf-8'), dtstart=start)
            # Get all occurrences between one week ago and a year from now
            future_year = datetime.now(timezone.utc) + timedelta(days=365)
            
            for occurrence in rule.between(one_week_ago, future_year):
                # Make sure occurrence is timezone-aware
                if occurrence.tzinfo is None:
                    occurrence = occurrence.replace(tzinfo=timezone.utc)
                
                if occurrence >= one_week_ago:
                    start_time = occurrence.isoformat()
                    end_time = (occurrence + (component.get('dtend').dt - component.get('dtstart').dt)).isoformat() if component.get('dtend') else None
                    
                    event = {
                        'summary': str(component.get('summary', 'No Title')),
                        'description': str(component.get('description', '')),
                        'start': start_time,
                        'end': end_time,
                        'location': str(component.get('location', '')),
                        'created': component.get('created').dt.isoformat() if component.get('created') else None,
                        'text': create_event_description(
                            str(component.get('summary', 'No Title')),
                            start_time,
                            end_time,
                            str(component.get('location', '')),
                            str(component.get('description', ''))
                        )
                    }
                    events.append(event)
        else:
            # Handle non-recurring events
            if isinstance(start, datetime):
                if start.tzinfo is None:
                    start = start.replace(tzinfo=timezone.utc)
            else:
                start = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc)
            
            if start >= one_week_ago:
                start_time = start.isoformat()
                end_time = component.get('dtend').dt.isoformat() if component.get('dtend') else None
                
                event = {
                    'summary': str(component.get('summary', 'No Title')),
                    'description': str(component.get('description', '')),
                    'start': start_time,
                    'end': end_time,
                    'location': str(component.get('location', '')),
                    'created': component.get('created').dt.isoformat() if component.get('created') else None,
                    'text': create_event_description(
                        str(component.get('summary', 'No Title')),
                        start_time,
                        end_time,
                        str(component.get('location', '')),
                        str(component.get('description', ''))
                    )
                }
                events.append(event)
    
    # Sort events by start time
    events.sort(key=lambda x: x['start'])
    
    # Create Calendars directory if it doesn't exist
    os.makedirs('Calendars', exist_ok=True)
    
    # Get current timestamp for filename
    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f'Calendars/calendar_events_{timestamp}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({'events': events}, f, ensure_ascii=False, indent=2)
    
    return len(events), filename

if __name__ == "__main__":
    # Get calendar URL from environment variables
    calendar_url = os.getenv('CALENDAR_URL')
    
    if not calendar_url:
        print("Error: CALENDAR_URL not found in environment variables")
        exit(1)
    
    try:
        num_events, filename = get_calendar(calendar_url)
        print(f"Successfully downloaded {num_events} events from the past week and future to {filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
