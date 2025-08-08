#!/bin/bash
# Idempotent script to create OpenTofu state backend

set -e

if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "Error: AWS_ACCOUNT_ID environment variable is required"
    exit 1
fi

BUCKET_NAME="devops1-tfstate-${AWS_ACCOUNT_ID}"
TABLE_NAME="devops1-tfstate-lock"
REGION="us-east-1"

# Create S3 bucket (idempotent)
if aws s3api head-bucket --bucket ${BUCKET_NAME} 2>/dev/null; then
    echo "S3 bucket already exists"
else
    echo "Creating S3 bucket..."
    aws s3 mb s3://${BUCKET_NAME} --region ${REGION}
fi

# Enable versioning
echo "Enabling versioning on S3 bucket..."
aws s3api put-bucket-versioning \
    --bucket ${BUCKET_NAME} \
    --versioning-configuration Status=Enabled

# Create DynamoDB table (idempotent)
if aws dynamodb describe-table --table-name ${TABLE_NAME} --region ${REGION} 2>/dev/null; then
    echo "DynamoDB table already exists"
else
    echo "Creating DynamoDB table for state locking..."
    aws dynamodb create-table \
        --table-name ${TABLE_NAME} \
        --attribute-definitions \
            AttributeName=LockID,AttributeType=S \
        --key-schema \
            AttributeName=LockID,KeyType=HASH \
        --billing-mode PAY_PER_REQUEST \
        --region ${REGION}

    echo "Waiting for DynamoDB table to be active..."
    aws dynamodb wait table-exists --table-name ${TABLE_NAME} --region ${REGION}
fi

echo "Waiting for DynamoDB table to be active..."
aws dynamodb wait table-exists --table-name ${TABLE_NAME} --region ${REGION}

echo "Backend setup complete!"
echo "========================"
echo "Check so your backend in infra/backend.tf matches:"
echo ""
echo "  backend \"s3\" {"
echo "    bucket         = \"${BUCKET_NAME}\""
echo "    key            = \"app/terraform.tfstate\""
echo "    region         = \"${REGION}\""
echo "    dynamodb_table = \"${TABLE_NAME}\""
echo "  }"
echo ""