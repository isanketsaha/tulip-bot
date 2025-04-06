import os

from src.api import TulipApi
from src.services import EmailService


class StockAnalysis:

    def __init__(self):
        self.threshold = 7
        self.api = TulipApi()
        self.email_service = EmailService()

    def handle_request(self):
        low_stock = []
        for item in self.get_catalog_and_check_stock():
            if item['availableQty'] <= self.threshold:
                low_stock.append(item)
        if len(low_stock) > 0:
            self.email_service.process_email({
                'low_stock_items': low_stock,
                'subject': "ALERT! School Stock Report"
            }, "LowStock.html")

    def get_catalog_and_check_stock(self):
        catalog = self.api.get("/report/inventory")
        return catalog
