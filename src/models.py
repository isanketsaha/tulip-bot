import re



class BankTransaction:
    def __init__(self, regex: str, line: str):
        match = re.match(regex, line)
        if match:
            self.account_number = match.group(1)
            self.type = match.group(2)
            self.amount = match.group(3)
            self.date = match.group(4)
            # self.totalAmount = match.group(4)
        else:
            match = re.search(regex, line)
            self.account_number = None
            self.type = None
            self.amount = None
            self.date = None

    def to_dict(self):
        return {
            "accountNumber": self.account_number,
            "type": self.type,
            "amount": self.amount,
            "date": self.date
        }
