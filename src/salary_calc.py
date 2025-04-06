from datetime import datetime, timedelta
import traceback
import pandas as pd

from package.dateutil.relativedelta import relativedelta
from src.officetime_api import OfficeTimeApi
from src.services import EmailService


def get_previous_month_dates():
    # Get today's date
    today = datetime.today()
    first_day_prev_month = (today - relativedelta(months=1)).replace(day=1)
    last_day_prev_month = first_day_prev_month - timedelta(days=1) + relativedelta(months=1)

    date_range = {
        "Empcode": "ALL",
        "FromDate": first_day_prev_month.strftime("%d/%m/%Y"),
        "ToDate": last_day_prev_month.strftime("%d/%m/%Y")
    }

    return date_range


def group_by_filter(data):
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["DateString"], format="%d/%m/%Y")
    df["DayOfWeek"] = df["Date"].dt.dayofweek  # 0 = Monday, 6 = Sunday
    absent_weekdays = df[
        (df["INTime"] == "--:--") &
        (df["OUTTime"] == "--:--") &
        (df["DayOfWeek"] < 5)  # Monday to Friday
        ]
    # Group by Name and list absent dates
    result = absent_weekdays.groupby("Name")["DateString"].apply(list).to_dict()
    return result


class SalaryCalculator:

    def __init__(self):
        self.office_api = OfficeTimeApi()
        self.email_service = EmailService()

    def calculate(self):
        dates = get_previous_month_dates()
        data = self.office_api.get("/DownloadInOutPunchData", dates)["InOutPunchData"]
        date = datetime.strptime(dates['FromDate'], '%d/%m/%Y')
        leave_data = {
            'subject': 'Employee Monthly Timesheet',
            "month_name": date.strftime("%B"),
            "year": date.strftime("%Y"),
            "leave_summary": group_by_filter(data)
        }
        self.email_service.process_email(leave_data, 'OfficeTime.html')


if __name__ == "__main__":
    SalaryCalculator().calculate()
