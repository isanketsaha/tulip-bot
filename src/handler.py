import email
import os
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Dict, Union, List

from src.daily_transaction import TransactionReportHandler
from src.utils import aws_session, logger


class Handle:
    def __init__(self):
        self.bucket_name = os.environ.get('bucket_name')

    def handle_request(self, event: Dict, context: Dict) -> dict[str, Union[str, int]]:
        print("Event received")
        print(event)
        handler = TransactionReportHandler()
        return handler.handle_request(self.get_s3_emails())

    def get_s3_emails(self):
        target_date = datetime.now().date() - timedelta(days=1)
        logger.info(f"Processing emails for date: {target_date}")
        paginator = aws_session().client('s3').get_paginator('list_objects_v2')

        for page in paginator.paginate(Bucket=self.bucket_name):
            if 'Contents' not in page:
                logger.info("No objects found in bucket")
                continue
            list_of_obj: List = []
            for obj in page['Contents']:
                last_modified = obj['LastModified'].date()

                if last_modified == target_date:
                    key = obj['Key']
                    logger.info(f"Processing email: {key}")
                    response = aws_session().client('s3').get_object(Bucket=self.bucket_name, Key=key)
                    mime_message = email.message_from_string(response['Body'].read().decode('utf-8', errors='ignore'))
                    list_of_obj.append(mime_message)
        return list_of_obj


def lambda_handler(event, context):
    handler = Handle()
    return handler.handle_request(event, context)


if __name__ == "__main__":
    lambda_handler("", "")
