# Smart File Processor (Auto Categorization System)

![AWS](https://img.shields.io/badge/AWS-Free%20Tier-orange) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 📌 What is this?

This project helps you organize and understand your business files automatically. It:

* Sorts files into categories like Sales, Finance, HR, etc.
* Finds useful insights (like total sales, overdue invoices).
* Works fully on AWS (free tier).
* No manual work needed after setup.

## ✅ Features

* 📁 **Auto File Sorting**: Puts files into categories.
* 📊 **Smart Reports**: Shows totals, averages, trends.
* ⚠️ **Warnings**: Alerts if data is missing or something is wrong.
* 🧹 **Data Cleaning**: Cleans data and adds timestamps.
* 📄 **Insight Reports**: Saves results in a separate folder.
* 💸 **Free to Use**: Works in AWS free tier.

## 🔧 Tools Used

* AWS Glue (for processing)
* Amazon S3 (for storage)
* IAM Role (for permissions)

---

## 🧱 System Diagram

```
Input Bucket (Raw Files) ──▶ Glue Job ──▶ Output Bucket (Sorted)
                                  │
                                  ▼
                        Insights Bucket (Reports)
```

---

## 📂 Types of Files It Supports

* CSV (.csv)
* JSON (.json)
* Parquet (.parquet)

## 📁 Categories

| Category  | File Examples      | It Finds...                     |
| --------- | ------------------ | ------------------------------- |
| Financial | invoices, payments | total amount, average, overdue  |
| Sales     | orders, revenue    | sales count, revenue trends     |
| Customer  | leads, contacts    | email domains, locations        |
| Inventory | products, stock    | low stock, out-of-stock alerts  |
| HR        | employees, salary  | departments, average salary     |
| Marketing | campaigns, leads   | top campaigns, conversion rates |

---

## 🛠️ Setup Guide (Step by Step)

### 1. Create 3 S3 Buckets

* Go to AWS Console → S3 → Create 3 buckets:

  * `smart-processor-input-yourname`
  * `smart-processor-output-yourname`
  * `smart-processor-insights-yourname`

### 2. Create IAM Role for Glue

* Go to IAM → Roles → Create Role
* Choose Glue service
* Attach policy: `AWSGlueServiceRole`
* Name it: `SmartProcessorRole`

### 3. Add S3 Access to Role

* In IAM → Roles → SmartProcessorRole
* Click "Add inline policy"
* Use this JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": [
        "arn:aws:s3:::smart-processor-*",
        "arn:aws:s3:::smart-processor-*/*"
      ]
    }
  ]
}
```

### 4. Create the Glue Job

* Go to AWS Glue → Jobs → Create job
* Choose: Spark Script Editor
* Paste the `data_quality_monitor.py` script
* Update the 3 bucket names inside the script
* Job config:

  * Name: `smart-file-processor`
  * IAM Role: `SmartProcessorRole`
  * Language: Python 3
  * Worker Type: G.1X (Free Tier)
  * Workers: 2

### 5. Upload Test Files

* Add `.csv`, `.json` or `.parquet` test files to the input bucket

### 6. Run the Job

* Go to Glue Job → Click Run
* Check output and insights buckets

---

## 🧪 Sample Files

You can upload test files like:

* `sample_invoice.csv`
* `sample_customers.csv`
* `sample_sales.csv`
* `sample_inventory.csv`

These will be categorized automatically and insights generated.

---

## ⚙️ How to Use

* 🟢 Drop files into the input bucket
* ▶️ Run the Glue job manually or set a daily trigger
* 📁 Check results in output and insights buckets

To automate it:

* Go to AWS Glue → Triggers → Create trigger
* Set time and connect to `smart-file-processor`

---

## 📂 Output Folder Structure

### Output Bucket:

```
smart-processor-output-yourname/
├── sales/
├── financial/
├── inventory/
├── customer/
├── hr/
├── marketing/
```

### Insights Bucket:

```
smart-processor-insights-yourname/
├── summary_report/
├── category_reports/
│   ├── sales/
│   ├── inventory/
│   └── ...
```

---

## 💰 Cost (Free Tier)

| AWS Service | Free Limit       | Our Usage      | Cost   |
| ----------- | ---------------- | -------------- | ------ |
| Glue        | 1M objects/month | < 1000 files   | \$0.00 |
| S3 Storage  | 5 GB             | \~100 MB       | \$0.00 |
| S3 Requests | 20K GET, 2K PUT  | \~500 requests | \$0.00 |

It’s free under AWS Free Tier!

---

## 🛠️ Customize

* To add more categories, edit `categorize_file()` method
* To add custom rules, update the `extract_*_insights()` methods

---

## 🔍 Debugging Tips

* Use Glue Logs (Job → Runs → Logs)
* Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Common Problems:

| Issue               | Cause               | Fix                |
| ------------------- | ------------------- | ------------------ |
| Job fails instantly | IAM Role missing S3 | Add S3 permissions |
| Empty results       | No files in input   | Upload files       |
| Out of memory       | Large files         | Use more workers   |

---

## 🔐 Security Tips

* Enable MFA, encryption, and bucket policies
* Don't store sensitive data in plain text

---

## 📈 Boost Performance

* For large files:

```python
df.repartition(10)
df.write.parquet(output_path)
```

* For many files:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

---

Happy Processing! 🎉
