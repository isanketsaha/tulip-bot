#!/bin/bash
set -e

# Define variables
VENV_DIR="venv"
PACKAGE_DIR="package"
ZIP_FILE="report-lambda.zip"
LAMBDA_NAME="TulipReport"

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "Installing dependencies..."
# Install dependencies into the package directory
pip install -r requirements.txt --target $PACKAGE_DIR/

echo "Packaging Lambda function..."

# Navigate to the package directory and zip dependencies
cd $PACKAGE_DIR
zip -r ../$ZIP_FILE .
cd ..

# Add source code and templates to the zip file
zip -g $ZIP_FILE src/* templates/*

echo "Uploading to AWS Lambda..."
aws lambda update-function-code \
   --function-name $LAMBDA_NAME \
   --zip-file fileb://$ZIP_FILE \
   --p tulip-test

rm -r $PACKAGE_DIR

rm -f $ZIP_FILE
echo "Deployment complete!"
