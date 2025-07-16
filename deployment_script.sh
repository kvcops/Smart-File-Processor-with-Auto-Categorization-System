#!/bin/bash

# AWS Glue Job Deployment Script
# Usage: ./deployment_script.sh

set -e

echo "🚀 Starting Smart File Processor deployment..."

# Configuration
REGION="us-east-1"  # Change to your preferred region
UNIQUE_SUFFIX="$(date +%Y%m%d%H%M%S)"

# Create S3 buckets
echo "📦 Creating S3 buckets..."
aws s3 mb s3://smart-processor-input-${UNIQUE_SUFFIX} --region ${REGION}
aws s3 mb s3://smart-processor-output-${UNIQUE_SUFFIX} --region ${REGION}
aws s3 mb s3://smart-processor-insights-${UNIQUE_SUFFIX} --region ${REGION}

# Create IAM role
echo "🔐 Creating IAM role..."
aws iam create-role \
    --role-name SmartProcessorRole \
    --assume-role-policy-document file://trust-policy.json

# Attach policies
aws iam attach-role-policy \
    --role-name SmartProcessorRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole

# Create Glue job
echo "⚙️ Creating Glue job..."
aws glue create-job \
    --name smart-file-processor \
    --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/SmartProcessorRole \
    --command ScriptLocation=s3://your-scripts-bucket/data_quality_monitor.py,Name=glueetl,PythonVersion=3 \
    --glue-version 4.0 \
    --worker-type G.1X \
    --number-of-workers 2 \
    --timeout 60

echo "✅ Deployment complete!"
echo "📁 Input bucket: smart-processor-input-${UNIQUE_SUFFIX}"
echo "📁 Output bucket: smart-processor-output-${UNIQUE_SUFFIX}"
echo "📁 Insights bucket: smart-processor-insights-${UNIQUE_SUFFIX}"
