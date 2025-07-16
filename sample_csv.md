# Smart File Processor - Simple Guide

This project helps you automatically process CSV/JSON/Parquet files in AWS S3, clean the data, categorize the files, and generate insights.

## 🔧 What You Need

- AWS account
- AWS Glue Job setup
- S3 buckets (for input, output, and insights)

## 📁 S3 Bucket Setup

Create 3 buckets:

- `smart-processor-input-yourname` → Put your input files here
- `smart-processor-output-yourname` → Processed files go here
- `smart-processor-insights-yourname` → Insights and reports go here

Update these names in the code if needed.

## 🛠 How It Works

1. The job reads each file from the input bucket
2. It checks the file type (.csv/.json/.parquet)
3. It categorizes the file (like financial, sales, etc.)
4. It cleans the data and adds a processed timestamp
5. It saves cleaned files in the output bucket under folders by category
6. It generates insights and alerts (like totals, averages, missing values)
7. It saves summary and category-wise reports in the insights bucket

## ▶️ How to Run It

1. Upload files to your input S3 bucket.
2. Start the Glue job from the AWS console.
3. After it's done:
   - Cleaned files will be in `smart-processor-output-yourname/`
   - Reports will be in `smart-processor-insights-yourname/`

## 📂 Sample Files

Use these to test:
- `sample_invoice.csv`
- `sample_customers.csv`
- `sample_sales.csv`
- `sample_inventory.csv`

## 📦 Python Requirements

These are already available in AWS Glue, but if you're testing locally:
```
boto3
pyspark
awscli
```

## 💡 Tips
- Works best with clean, tabular data
- File name and content help decide the category
- Add more logic in `SmartFileProcessor` if needed

## 🧠 What It Can Detect
- Missing data alerts
- Financial trends
- Sales performance
- Customer insights
- Inventory levels
- HR and marketing data

---

Happy processing! 🎉
