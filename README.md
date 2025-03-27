# Transaction Report Lambda

AWS Lambda function to process transaction notifications from SNS events.

## Prerequisites
- Python 3.9+ (must match your existing Lambda runtime version)
- AWS CLI configured
- AWS credentials with Lambda and SNS permissions
- Existing Lambda function named `TransactionReportLambda` (update `deploy.sh` if name differs)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd transaction-report-lambda
   ```

2. **Activate a virtual environment**:
   ```bash
   python3 -m venv venv
   
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Deactivate the virtual environment**:
   ```bash
   deactivate
   ```

## Testing

1. **Run unit tests**:
   Navigate to the `tests/` directory and execute the test cases:
   ```bash
   python -m unittest discover -s tests
   ```

   Ensure the virtual environment is activated before running the tests.

2. **Local testing with `handler.py`**:
   You can simulate an SNS event by creating a sample JSON payload and invoking the handler locally:
   ```bash
   python
   >>> from src.handler import lambda_handler
   >>> event = {"key": "value"}  # Replace with actual SNS event structure
   >>> context = {}  # Mock context
   >>> lambda_handler(event, context)
   ```

## Project Structure

```plaintext
transaction-report-lambda/
├── src/                    # Source code
│   ├── __init__.py
│   ├── handler.py         # Main Lambda handler
│   ├── models.py         # Data models
│   ├── services.py       # Service classes
│   └── utils.py          # Utility functions
├── tests/                 # Unit tests
│   ├── __init__.py
│   └── test_handler.py   # Test cases
├── templates/             # Email templates
│   └── TransactionReport.vm  # Velocity template
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── deploy.sh             # Deployment script
```
