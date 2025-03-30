import email
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Dict, Union, List

from src.daily_transaction import TransactionReportHandler
from src.utils import aws_session, logger


class Handle:
    def __init__(self):
        self.invoke_type = ""

    def handle_request(self, event: Dict, context: Dict) -> dict[str, Union[str, int]]:
        print("Event received:")
        print(event)
        handler = TransactionReportHandler()
        handler.handle_request(getObject())
        getObject()
        return {
            "statusCode": 200,
            "body": "Success"
        }


def getObject():
    target_date = datetime.now().date() - timedelta(days=1)  # Process yesterday's emails
    logger.info(f"Processing emails for date: {target_date}")

    # List all objects in the bucket
    paginator = aws_session().client('s3').get_paginator('list_objects_v2')
    processed_count = 0

    for page in paginator.paginate(Bucket="email-0a62a9e0"):
        if 'Contents' not in page:
            logger.info("No objects found in bucket")
            continue
        list_of_obj: List = []
        for obj in page['Contents']:
            last_modified = obj['LastModified'].date()  # Get object's modification date

            # Filter objects by the target date
            if last_modified == target_date:
                key = obj['Key']
                logger.info(f"Processing email: {key}")

                # Fetch the email from S3
                response = aws_session().client('s3').get_object(Bucket="email-0a62a9e0", Key=key)
                mime_message = email.message_from_string(response['Body'].read().decode('utf-8', errors='ignore'))
                # if not isinstance(mime_message, EmailMessage):
                #     logger.warning(f"Failed to parse email content for {key}")
                #     continue
                list_of_obj.append(mime_message)
    return list_of_obj


def lambda_handler(event, context):
    handler = Handle()
    return handler.handle_request(event, context)


if __name__ == "__main__":
    lambda_handler("", "")
