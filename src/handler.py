import json
import traceback
from typing import Dict

from src.daily_transaction import TransactionReportHandler
from src.stock_alert import StockAnalysis
from src.utils import logger


def handle() -> Dict:
    return {
        'Daily_Transaction_Report': TransactionReportHandler,
        'STOCK_SCAN': StockAnalysis
    }


def handle_request(event: Dict, context: Dict):
    try:
        event = json.loads(event)
        print(f"Event value = {event['ruleName']}")
        rules = handle()
        invoke = rules.get(event['ruleName'], lambda: "Invalid selection")()
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


def lambda_handler(event, context):
    return handle_request(event, context)


if __name__ == "__main__":
    lambda_handler({'ruleName': 'Daily_Transaction_Report'}, "")
