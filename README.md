# Smart File Processor with Auto-Categorization System

[![AWS](https://img.shields.io/badge/AWS-Free%20Tier-orange)](https://aws.amazon.com/free/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🚀 Overview

The **Smart File Processor** is an intelligent, automated system that categorizes, processes, and extracts business insights from various file formats using only AWS Glue, S3, and IAM. It's designed to solve the common problem of manually sorting and analyzing business files.

### ✨ Key Features

* **🤖 Automatic File Categorization**: Intelligently sorts files into categories (Financial, Sales, Customer, Inventory, HR, Marketing)
* **📊 Business Intelligence**: Extracts meaningful insights and KPIs from each file type
* **🚨 Smart Alerts**: Generates data quality alerts and business warnings
* **🔀 Data Cleaning**: Automatically cleans and enhances datasets
* **📈 Comprehensive Reporting**: Creates detailed insights reports with trends and analytics
* **💰 Cost-Effective**: Runs entirely on AWS Free Tier
* **⚡ Zero Manual Effort**: Fully automated after setup

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input Bucket  │───▶│   AWS Glue Job  │───▶│  Output Bucket  │
│  (Raw Files)    │    │  (Processing)   │    │ (Categorized)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│
▼
┌─────────────────┐
│ Insights Bucket │
│   (Reports)     │
└─────────────────┘
```

## 🎯 Supported File Types

* **CSV Files** (.csv)
* **JSON Files** (.json)
* **Parquet Files** (.parquet)

## 📂 File Categories

| Category      | Examples                        | Insights Generated                                   |
| ------------- | ------------------------------- | ---------------------------------------------------- |
| **Financial** | invoices, receipts, payments    | Revenue totals, average amounts, payment trends      |
| **Sales**     | orders, transactions, revenue   | Sales volume, product performance, conversion rates  |
| **Customer**  | contacts, leads, profiles       | Demographics, email domains, geographic distribution |
| **Inventory** | stock levels, products          | Low stock alerts, inventory turnover, availability   |
| **HR**        | employees, payroll, departments | Salary analysis, department distribution, headcount  |
| **Marketing** | campaigns, analytics, leads     | Campaign performance, conversion metrics, ROI        |

## 🛠️ Prerequisites

* AWS Account with Free Tier access
* Basic understanding of AWS Console
* Files in supported formats (CSV, JSON, Parquet)

## 📋 Setup Instructions

### Step 1: Create S3 Buckets

Create three S3 buckets in your AWS Console:

```bash
# Replace [your-unique-suffix] with your chosen suffix
smart-processor-input-[your-unique-suffix]
smart-processor-output-[your-unique-suffix]
smart-processor-insights-[your-unique-suffix]
```

**Detailed Steps:**

* Navigate to S3 in AWS Console
* Click Create bucket
* Enter bucket name (must be globally unique)
* Choose your preferred region
* Leave other settings as default
* Click Create bucket
* Repeat for all three buckets

### Step 2: Create IAM Role

* Go to IAM → Roles → Create role
* Select AWS service → Glue
* Click Next: Permissions
* Attach the following policies:

  * AWSGlueServiceRole
* Click Next: Tags (skip)
* Click Next: Review
* Role name: `SmartProcessorRole`
* Click Create role

### Step 3: Add S3 Permissions to IAM Role

* Go to IAM → Roles → `SmartProcessorRole`
* Click Add permissions → Create inline policy
* Click **JSON** tab and paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::smart-processor-*",
        "arn:aws:s3:::smart-processor-*/*"
      ]
    }
  ]
}
```

* Click Review policy
* Name: `SmartProcessorS3Policy`
* Click Create policy

### Step 4: Create Glue Job

* Go to AWS Glue → Jobs → Create job
* Select Spark script editor
* Choose "Upload and edit an existing script"
* Copy and paste the `data_quality_monitor.py` script
* **Update the bucket names in the script:**

```python
INPUT_BUCKET = "smart-processor-input-[your-unique-suffix]"
OUTPUT_BUCKET = "smart-processor-output-[your-unique-suffix]"
INSIGHTS_BUCKET = "smart-processor-insights-[your-unique-suffix]"
```

### Step 5: Configure Job Settings

**Job Details:**

* Name: `smart-file-processor`
* IAM Role: `SmartProcessorRole`
* Glue version: 4.0
* Language: Python 3

**Advanced Properties:**

* Worker type: G.1X (Free tier eligible)
* Number of workers: 2
* Job timeout: 60 minutes
* Number of retries: 0

### Step 6: Save and Test

* Click Save
* Upload test files to your input bucket
* Click Run to test the job

## 📊 Sample Test Data

Sample files to test the system:

* `sample_invoice.csv`
* `sample_customers.csv`
* `sample_inventory.csv`
* `sample_sales.csv`

*(Include the CSV content as per original)*

## 🚀 Usage

### Basic Usage

1. **Upload Files**: Drop your files into the input bucket
2. **Run Job**: Execute the Glue job manually or via schedule
3. **Check Results**: Review organized files and insights

### Automated Processing

Set up a trigger for automatic processing:

* Go to AWS Glue → Triggers → Create trigger
* Name: `daily-file-processor`
* Type: Schedule
* Frequency: Daily
* Start time: 02:00 UTC (adjust for your timezone)
* Associate with job: `smart-file-processor`

### Manual Execution

```bash
# Via AWS CLI
aws glue start-job-run --job-name smart-file-processor
```

## 📈 Output Structure

**Output Bucket Structure**

```
smart-processor-output-[suffix]/
├── financial/
├── customer/
├── sales/
├── inventory/
├── hr/
├── marketing/
└── general/
```

**Insights Bucket Structure**

```
smart-processor-insights-[suffix]/
├── summary_report/
├── category_reports/
├── daily_insights/
```

## 📊 Sample Insights Output

*(Include JSON example for Financial, Customer, Inventory as in original)*

## 💰 Cost Breakdown (AWS Free Tier)

| Service     | Free Tier Limit  | Estimated Usage | Cost       |
| ----------- | ---------------- | --------------- | ---------- |
| AWS Glue    | 1M objects/month | \~1000 files    | \$0.00     |
| S3 Storage  | 5GB              | \~100MB         | \$0.00     |
| S3 Requests | 20K GET, 2K PUT  | \~500 requests  | \$0.00     |
| **Total**   |                  |                 | **\$0.00** |

**Scaling Beyond Free Tier:**

* AWS Glue: \$0.44/DPU-hour
* S3 Storage: \$0.023/GB/month
* Data Transfer: First 1GB free, then \$0.09/GB

## 🔧 Customization

**Adding New Categories:**

```python
# Add in categorize_file method
if any(word in filename_lower for word in ['legal', 'contract', 'agreement']):
    return 'legal'
```

**Custom Insights:**

```python
def extract_legal_insights(self, df):
    """Extract legal document insights"""
    insights = []
    # Add logic here
    return insights
```

**Alert Thresholds:**

```python
# Change from 50% to 30%
if null_percentage > 30:
    alerts.append({
        'type': 'CRITICAL',
        'message': f'Column {col_name} has {null_percentage:.1f}% missing values',
        'severity': 'high'
    })
```

## 🔍 Monitoring & Troubleshooting

**Job Monitoring:**

* AWS Glue Console: Job logs and metrics
* CloudWatch: Alarms for job failures
* S3 Events: Monitor uploads

**Common Issues:**

| Issue              | Cause              | Solution              |
| ------------------ | ------------------ | --------------------- |
| Job fails          | IAM permissions    | Check role S3 access  |
| No files processed | Empty input bucket | Upload test files     |
| Out of memory      | Large files        | Increase worker count |
| Schema errors      | Mixed data types   | Add data validation   |

**Debugging:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Security Best Practices

**IAM:**

* Least privilege principle
* Rotate access keys
* Enable MFA

**S3:**

* Enable bucket versioning
* Use encryption
* Setup access policies

**Data Protection:**

* Avoid storing sensitive data in plaintext
* Use encryption at rest
* Enable CloudTrail for logs

## 📊 Performance Optimization

**For Large Files (>100MB)**

```python
df.repartition(10)
df.write.mode('overwrite').parquet(output_path)
```

**For High Volume Processing**

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```
