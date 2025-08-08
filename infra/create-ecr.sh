#!/bin/bash
# Idempotent script to create ECR repository

set -e

REPOSITORY_NAME="devops1-blog-app"
REGION="us-east-1"

# Check if ECR repository exists (idempotent)
if aws ecr describe-repositories --repository-names ${REPOSITORY_NAME} --region ${REGION} 2>/dev/null; then
    echo "ECR repository '${REPOSITORY_NAME}' already exists"
else
    echo "Creating ECR repository '${REPOSITORY_NAME}'..."
    aws ecr create-repository \
        --repository-name ${REPOSITORY_NAME} \
        --image-tag-mutability MUTABLE \
        --image-scanning-configuration scanOnPush=true \
        --region ${REGION}
fi

# Get repository URI for reference
REPOSITORY_URI=$(aws ecr describe-repositories --repository-names ${REPOSITORY_NAME} --region ${REGION} --query 'repositories[0].repositoryUri' --output text)

echo "ECR repository setup complete!"
echo "========================"
echo "Repository URI: ${REPOSITORY_URI}"
echo ""
echo "You can now build and push images to this repository:"
echo "docker build -t ${REPOSITORY_URI}:tag ."
echo "docker push ${REPOSITORY_URI}:tag"
echo ""