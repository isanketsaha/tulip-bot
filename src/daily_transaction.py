import email
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Union
import traceback

from src.api import TulipApi
from src.models import BankTransaction
from src.services import EmailService
from src.utils import get_text_from_mime_message, filter_english_lines, extract_message, aws_session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TransactionReportHandler:
    def __init__(self):
        self.api = TulipApi()
        self.bucket_name = os.environ.get('bucket_name')
        self.email_service = EmailService()
        self.regex = r"Your A/C (\w+) Credited INR ([\d,]+\.\d{2}) on (\d{2}/\d{2}/\d{2})"
        self.parseRegex = r'Your A/C\s+(?P<account>X{5}\d{6})\s+(?P<transaction>Credited|Debited)\s+INR\s+(?P<amount>[\d,]+\.\d{2})\s+on\s+(?P<date>\d{2}/\d{2}/\d{2})'
        self.expected_sender = os.environ.get('senderEmail')  # Configure this

    def handle_request(self) -> Union[dict[str, Union[str, int]], str]:
        try:
            list_transactions = []
            total_amount = 0.0
            for mime_message in self.get_s3_emails():
                if email.utils.parseaddr(mime_message['from'])[1] == self.expected_sender:
                    body = get_text_from_mime_message(mime_message)
                    logger.info(f"Message Body = {body}")
                    english_lines = [extract_message(line) for line in filter_english_lines(body, self.regex)]
                    # Find bank transaction
                    bank_transaction = next(
                        (BankTransaction(self.parseRegex, line)
                         for line in english_lines if line.startswith("Your A/C")), None)
                    list_transactions.append(bank_transaction)
            if not list_transactions:
                logger.info(f"No email for today or no match sender")
                return {
                    "statusCode": 200,
                    "body": "No email for today or no match sender"
                }
            else:
                total_amount += sum(float(transaction.amount.replace(',', ''))
                                    for transaction in list_transactions
                                    if transaction.type == 'Credited')
                dashboard_amount = self.transaction_detail(list_transactions[0].date)
                diff = total_amount - float(dashboard_amount["portalAmount"])
                dashboard_amount.update({
                    "subject": "ALERT! School Transaction Report",
                    "accountNumber": list_transactions[0].account_number,
                    "amount": f"{total_amount:,}",
                    "date": list_transactions[0].date,
                    "difference": f"{diff:,}"
                })
                logger.info("Email matches criteria.")
                self.email_service.process_email(dashboard_amount, "TransactionReport.html")
                return {
                    "statusCode": 200,
                    "body": "Emails Processed Successfully"
                }
        except Exception as e:
            logger.error(f"Error processing email record: {traceback.format_exc()}")
            return {
                "statusCode": 404,
                "body": "Errors while processing email"
            }

    def transaction_detail(self, date: str) -> dict:
        date = datetime.strptime(date, "%d/%m/%y")
        date = date.strftime("%Y-%m-%d")
        transactions = self.api.get("/report/transaction/" + date)
        total = 0
        totals_by_type = {"fees": 0.0, "purchase": 0.0, "expense": 0.0, "portalAmount": 0.0}
        for txn in transactions:
            if txn["paymentMode"] == "CASH":
                totals_by_type[txn["payType"].lower()] += float(txn["total"])
                totals_by_type["portalAmount"] += txn['total']
        return totals_by_type

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
