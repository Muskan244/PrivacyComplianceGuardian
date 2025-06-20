from google.adk.agents import Agent
from datetime import datetime
import os
import base64
import shutil

def upload_file(source_path: str) -> dict:
    """
    Copy a local file from the given source_path to watched_dir and generate an event payload.
    Args:
        source_path: The path to the file to copy.
    Returns:
        An event payload for the next agent.
    """
    WATCHED_DIR = "watched_dir"
    os.makedirs(WATCHED_DIR, exist_ok=True)
    filename = os.path.basename(source_path)
    dest_path = os.path.join(WATCHED_DIR, filename)
    shutil.copy2(source_path, dest_path)
    payload = {
        "event_type": "new_file_ingested",
        "file_path": dest_path,
        "timestamp": datetime.now().isoformat()
    }
    return payload

root_agent = Agent(
    name="watchdog_agent",
    model="gemini-2.0-flash",
    description="Agent that detects new data ingestion events and starts the privacy compliance pipeline",
    instruction="You are responsible for monitoring new file ingestion events. When a new file arrives, generate an event payload containing the file path for downstream agents.",
    tools=[upload_file],
)