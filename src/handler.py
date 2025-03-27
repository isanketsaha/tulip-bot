import email
import json
import logging
import os
from datetime import datetime
from typing import Dict
import traceback

from src.api import TulipApi
from src.models import BankTransaction
from src.services import EmailService
from src.utils import get_text_from_mime_message, filter_english_lines, extract_message

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TransactionReportHandler:
    def __init__(self):
        self.api = TulipApi()
        self.email_service = EmailService()
        self.regex = r"Your A/C (\w+) Credited INR ([\d,]+\.\d{2}) on (\d{2}/\d{2}/\d{2})"
        self.parseRegex = r"Your A/C\s+(?P<account>X{5}\d{6})\s+(?P<transaction>Credited)\s+INR(?P<amount> \d{1,3}(?:,\d{3})*\.\d{2})\s+on\s+(?P<date>\d{2}/\d{2}/\d{2})\s+-Deposit by transfer from\s+(?P<source>[A-Z\s\.]+)\.\s+Avl Bal\s+(?P<balance>INR \d{1,3}(?:,\d{3})*)"
        self.expected_sender = os.environ.get('senderEmail')  # Configure this

    def handle_request(self, event: Dict, context: Dict) -> str:
        logger.info(f"Received input: {event}")
        logger.info(f"Received context: {context}")

        if 'Records' not in event:
            logger.warning("No SNS records found in event")
            return "No records processed"

        for record in event['Records']:
            notification = json.loads(record['Sns']['Message'])
            logger.info(f"SNS records = {notification}")

            try:
                email_content = notification.get('content')
                mime_message = email.message_from_string(email_content)
                logger.info(f"Message Body = {mime_message}",)
                from_addr = email.utils.parseaddr(mime_message['from'])[1]
                body = get_text_from_mime_message(mime_message)
                english_lines = [extract_message(line) for line in filter_english_lines(body, self.regex)]
                # Find bank transaction
                bank_transaction = next(
                    (BankTransaction(self.parseRegex, line)
                     for line in english_lines
                     if line.startswith("Your A/C")),
                    None
                )

                dashboard_amount = self.transaction_detail(bank_transaction.date)
                diff = float(bank_transaction.amount.replace(',', '')) \
                       - float(dashboard_amount["portalAmount"].replace(',', ''))
                if from_addr == self.expected_sender and bank_transaction.type == 'Credited':
                    dashboard_amount.update({
                        "subject": "ALERT! School Transaction Report",
                        "accountNumber": bank_transaction.account_number,
                        "amount": bank_transaction.amount,
                        "date": bank_transaction.date,
                        "difference": f"{diff:,}"
                    })
                    logger.info("Email matches criteria.")
                    self.email_service.process_email(dashboard_amount, "TransactionReport.vm")
                    return "Processed Successfully"
                else:
                    logger.info(f"Email does not match criteria or no amount difference. Ignoring sender - {from_addr}")

            except Exception as e:
                logger.error(f"Error processing SNS record: {traceback.format_exc()}")
                raise

        return "No records processed"

    def transaction_detail(self, date: str) -> dict:
        date = datetime.strptime(date, "%d/%m/%y")
        date = date.strftime("%Y-%m-%d")
        transactions = self.api.get("/report/transaction/" + date)
        total = 0
        totals_by_type = {"fees": 0.0, "purchase": 0.0, "expense": 0.0}
        for txn in transactions:
            if txn["paymentMode"] == "CASH":
                pay_type = txn["payType"].lower()
                total += float(txn["total"])
            if pay_type in totals_by_type:
                totals_by_type[pay_type] += float(txn["total"])
        totals_by_type["portalAmount"] = f"{total:,}"
        return totals_by_type


# Example usage with AWS Lambda
def lambda_handler(event, context):
    handler = TransactionReportHandler()
    return handler.handle_request(event, context)


# For local testing
if __name__ == "__main__":
    # Load the JSON from the file
    with open('test.json', 'r') as file:
        json_data = json.load(file)

    # Sample event for testing
    sample_context = {}
    result = lambda_handler(json_data, sample_context)
    print(result)
