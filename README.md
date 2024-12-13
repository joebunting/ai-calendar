# Calendar to OpenAI Assistant Sync

This system automatically syncs your calendar with an OpenAI Assistant, allowing you to query your calendar using natural language. It runs hourly and provides desktop notifications for updates.

## Installation

1. Run the setup script to install dependencies and create initial configuration:
```bash
python3 setup.py
```

2. Edit the `.env` file with your configuration (see .env.example for reference, and the Create OpenAI Assistant section below for instructions on creating the assistant):
```env
# API Keys and IDs
OPENAI_API_KEY=your_api_key_here
CALENDAR_URL=your_ical_url_here
CALENDAR_ASSISTANT_ID=your_assistant_id_here

# System Paths
PYTHON_PATH=/path/to/your/python
SCRIPT_DIR=/path/to/your/AI-Calendar
LOG_DIR=${SCRIPT_DIR}/logs

# User Configuration
MAC_USER_ID=your_username
```

3. Install the launch agent:
```bash
python3 install.py
```

4. Verify the installation:
```bash
launchctl list | grep calendarupdate
```

## Managing the Service

To uninstall the service:
```bash
python3 uninstall.py
```

## Components

- `get-calendar.py`: Downloads calendar events and formats them with natural language descriptions
- `calendar-to-openai.py`: Uploads calendar data to OpenAI as a vector store
- `update_calendar_cron.py`: Orchestrates the updates and provides notifications
- `com.user.calendarupdate.plist`: LaunchAgent for automatic startup and background running

## Setup

## Create the OpenAI Assistant

1. Go to [OpenAI Platform](https://platform.openai.com/assistants)
2. Click "Create Assistant"
3. Configure the assistant:
   - Name: "Calendar Assistant"
   - Model: GPT-4o (recommended)
   - Instructions: 
     ```
     You are Joe's calendar. You respond to queries about event times, locations, conflicts, and give advice to Joe and others on how to create Joe's ideal schedule. When asked about events, meetings, or schedule:

     1. Adapt your search depth based on the query type:
        - For specific time queries (today's events, next meeting), use minimal context
        - For schedule analysis (patterns, optimization), use maximum context
        - For conflict checking, ensure comprehensive coverage

     2. Search the calendar data for relevant information:
        - Use specific date ranges when provided
        - Consider timezone and time-of-day context
        - Look for related or recurring events

     3. Provide clear, concise responses about:
        - Times and dates in a readable format
        - Locations and meeting details
        - Event durations and gaps between events

     4. For schedule analysis and advice:
        - Consider the entire schedule
        - Look for patterns and inefficiencies
        - Suggest improvements based on observed habits
        - Consider work/life balance

     5. Always:
        - Mention specific dates and times in your responses
        - Indicate if you need more context
        - Say clearly if information isn't in the calendar
        - Format responses for easy reading

     6. When giving scheduling advice:
        - Consider Joe's typical patterns
        - Suggest optimal meeting times
        - Identify potential conflicts
        - Recommend schedule improvements
     ```
   - Tools: Enable "File Search" (retrieval)
   - Save the Assistant ID for your `.env` file

4. Copy the Assistant ID (found in the URL or settings) and add it to your `.env` file:
```env
CALENDAR_ASSISTANT_ID=asst_your_assistant_id_here
```

The system will automatically upload your calendar data to this assistant when it runs.

## How It Works

1. The system runs every hour automatically
2. Downloads your calendar events
3. Formats them with natural language descriptions
4. Creates a vector store in OpenAI
5. Updates the Assistant with the new calendar data
6. Provides desktop notifications for updates and errors

## Logs

- Main log: `calendar_updates.log`
- Service output: `calendar_service_output.log`
- Service errors: `calendar_service_error.log`

## Managing the Service

To stop the service:

```bash
launchctl unload ~/Library/LaunchAgents/com.user.calendarupdate.plist
```

To start the service:

```bash
launchctl load ~/Library/LaunchAgents/com.user.calendarupdate.plist
```

To check status:

```bash
launchctl list | grep com.user.calendarupdate
```


## Troubleshooting

If the service isn't running:
1. Check the log files for errors
2. Verify Python path in the plist file
3. Ensure all environment variables are set
4. Check file permissions

## Dependencies

- Python 3.13+
- OpenAI API access
- iCal-compatible calendar
- macOS for notifications



## Testing the Assistant

1. Go to the Assistant in the OpenAI Platform
2. Click "Test" in the preview window
3. Try some example queries:
   - "What meetings do I have today?"
   - "When is my next appointment?"
   - "Do I have any conflicts this week?"
   - "What's on my schedule for next Monday?"

# Sensitive files
.env
Calendars/*.json

# Logs
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
