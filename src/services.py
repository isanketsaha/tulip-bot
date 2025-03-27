import traceback
from botocore.exceptions import ClientError
from typing import Dict
import logging
import os

from jinja2 import Template

from src.utils import logger, aws_session


# logger = logging.getLogger(__name__)


class EmailService:

    def __init__(self, aws_region: str = "ap-south-1"):
        self.ses_client = aws_session().client('ses')
        self.sender = "bot@inbox.tulipschool.co.in"
        self.recipient = os.environ.get('recipientEmail')
        self.template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")

    def process_email(self, data: Dict, template_name: str) -> None:
        logger.info(f"Processing email with data: {data} using template: {template_name}")

        if not self.recipient:
            logger.error("No recipient provided in data.")
            raise ValueError("Recipient email is required.")

        # Load and merge the template
        try:
            template_path = os.path.join(self.template_dir, template_name)
            if not os.path.exists(template_path):
                logger.error(f"Template file not found: {template_path}")
                raise FileNotFoundError(f"Template {template_name} not found in {self.template_dir}")

            with open(template_path, 'r') as file:
                template_content = file.read()
                template = Template(template_content)
                html_body = template.render(data)
            # # Merge template with data
            # body_html = _merge_template(template_content, data)

            # Send the email via SES
            response = self._send_raw_email(self.recipient, data.get("subject"), html_body)
            logger.info(f"Email sent successfully. Message ID: {response['MessageId']}")

        except FileNotFoundError as e:
            logger.error(traceback.format_exc())
            raise
        except ClientError as e:
            logger.error(f"Failed to send email: {e.response['Error']['Message']}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while sending email: {traceback.format_exc()}")
            raise

    def _send_raw_email(self, recipient: str, subject: str, body_html: str) -> Dict:
        """Send a raw email with HTML content via SES."""
        return self.ses_client.send_email(
            Source=self.sender,
            Destination={
                'ToAddresses': [recipient],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    },
                    'Text': {
                        'Data': body_html.replace('<', '').replace('>', ''),  # Simple text fallback
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
