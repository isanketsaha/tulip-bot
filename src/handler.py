import email
import os
import traceback
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Dict, Union, List

from src.daily_transaction import TransactionReportHandler
from src.stock_alert import StockAnalysis
from src.utils import aws_session, logger


class Handle:

    def handle_request(self, event: Dict, context: Dict):
        try:
            print("Event received")
            print(event)
            invoke = self.handle().get(event['ruleName'], lambda: "Invalid selection")()
            invoke.handle_request()
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

    def handle(self):
        return {
            'Daily_Transaction_Report':  TransactionReportHandler,
            'STOCK_SCAN': StockAnalysis
        }


def lambda_handler(event, context):
    handler = Handle()
    return handler.handle_request({'ruleName' : 'STOCK_SCAN'}, context)


if __name__ == "__main__":
    lambda_handler("", "")
