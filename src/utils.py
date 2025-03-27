import email
import logging
import os
import re
from typing import List

import boto3

logger = logging.getLogger(__name__)


def aws_session():
    # Check if running locally by checking a custom environment variable
    if os.getenv("AWS_EXECUTION_ENV") is None:
        # Running locally, use profile
        return boto3.Session(profile_name="tulip-test")
    else:
        # Running in AWS Lambda, use default session
        return boto3


# Add utility functions here as needed
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def filter_english_lines(body: str, english_pattern: str) -> List[str]:
    return [line.strip() for line in body.split('\r\n')
            if re.findall(english_pattern, line, re.IGNORECASE) and line.strip()]


def extract_message(text):
    # Define the start and end markers
    start_marker = "Your A/C XXXXX729063"
    end_marker = "-SBI"

    # Find the starting position
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return None

    # Find the ending position (after the start marker)
    end_idx = text.find(end_marker, start_idx) + len(end_marker)
    if end_idx == -1:
        return None

    # Extract the substring
    return text[start_idx:end_idx]

def get_text_from_mime_message(message: email.message.Message) -> str:
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                return part.get_payload(decode=True).decode()
            elif content_type == 'text/html':
                return part.get_payload(decode=True).decode()  # Optionally strip HTML
    else:
        return message.get_payload(decode=True).decode()
    return ""
