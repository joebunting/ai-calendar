import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def upload_calendar_to_openai(json_file):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    assistant_id = os.getenv('CALENDAR_ASSISTANT_ID')
    
    if not assistant_id:
        print("Error: CALENDAR_ASSISTANT_ID not found in environment variables")
        return False
    
    try:
        # List and delete old vector stores
        try:
            vector_stores = client.beta.vector_stores.list()
            if vector_stores and hasattr(vector_stores, 'data'):
                for store in vector_stores.data:
                    if store.name and store.name.startswith('Calendar Events'):
                        print(f"Removing old vector store: {store.id}")
                        client.beta.vector_stores.delete(store.id)
        except Exception as e:
            print(f"Warning: Could not list/delete old vector stores: {str(e)}")
        
        # Create a new vector store for the calendar
        vector_store = client.beta.vector_stores.create(
            name=f"Calendar Events {datetime.now().strftime('%Y-%m-%d')}"
        )
        print(f"Created vector store: {vector_store.id}")
        
        # Upload the file to the vector store
        with open(json_file, 'rb') as f:
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id,
                files=[f]
            )
        
        print(f"File batch status: {file_batch.status}")
        print(f"File counts: {file_batch.file_counts}")
        
        # Update the assistant to use the vector store
        client.beta.assistants.update(
            assistant_id=assistant_id,
            tools=[{"type": "file_search"}],  # Changed from 'retrieval' to 'file_search'
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store.id]
                }
            }
        )
        
        print("Successfully updated assistant with new vector store")
        return True
        
    except Exception as e:
        print(f"Error uploading to OpenAI: {str(e)}")
        return False

if __name__ == "__main__":
    # Get current timestamp for finding the latest calendar file
    timestamp = datetime.now().strftime('%Y-%m-%d')
    calendar_file = f'Calendars/calendar_events_{timestamp}.json'
    
    if not os.path.exists(calendar_file):
        print(f"Error: Calendar file not found: {calendar_file}")
        exit(1)
    
    if upload_calendar_to_openai(calendar_file):
        print("Successfully uploaded and updated calendar data")
    else:
        print("Failed to upload calendar data to OpenAI")
