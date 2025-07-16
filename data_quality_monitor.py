import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *
import boto3
import json
from datetime import datetime
import re

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Configuration - UPDATE THESE WITH YOUR BUCKET NAMES
INPUT_BUCKET = "smart-processor-input-yourname"
OUTPUT_BUCKET = "smart-processor-output-yourname"
INSIGHTS_BUCKET = "smart-processor-insights-yourname"

class SmartFileProcessor:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.processed_files = []
        
    def categorize_file(self, filename, content_sample):
        """
        Intelligent file categorization based on filename and content analysis
        """
        filename_lower = filename.lower()
        content_lower = content_sample.lower()
        
        # Financial files detection
        financial_keywords = ['invoice', 'receipt', 'payment', 'bill', 'expense', 'cost', 'financial']
        financial_content = ['total', 'amount', 'price', '$', 'invoice', 'payment', 'tax', 'subtotal']
        
        if any(word in filename_lower for word in financial_keywords):
            return 'financial'
        if any(word in content_lower for word in financial_content):
            return 'financial'
            
        # Customer data detection
        customer_keywords = ['customer', 'client', 'contact', 'user', 'member']
        customer_content = ['email', 'phone', 'address', 'customer', 'name', 'contact']
        
        if any(word in filename_lower for word in customer_keywords):
            return 'customer'
        if any(word in content_lower for word in customer_content):
            return 'customer'
            
        # Inventory/Product data detection
        inventory_keywords = ['inventory', 'product', 'stock', 'item', 'catalog', 'sku']
        inventory_content = ['quantity', 'sku', 'product', 'stock', 'inventory', 'warehouse']
        
        if any(word in filename_lower for word in inventory_keywords):
            return 'inventory'
        if any(word in content_lower for word in inventory_content):
            return 'inventory'
            
        # Sales data detection
        sales_keywords = ['sales', 'order', 'transaction', 'purchase', 'revenue']
        sales_content = ['order', 'sold', 'quantity', 'sale', 'revenue', 'commission']
        
        if any(word in filename_lower for word in sales_keywords):
            return 'sales'
        if any(word in content_lower for word in sales_content):
            return 'sales'
            
        # HR/Employee data detection
        hr_keywords = ['employee', 'staff', 'payroll', 'hr', 'personnel']
        hr_content = ['employee', 'salary', 'department', 'hire', 'position']
        
        if any(word in filename_lower for word in hr_keywords):
            return 'hr'
        if any(word in content_lower for word in hr_content):
            return 'hr'
            
        # Marketing data detection
        marketing_keywords = ['marketing', 'campaign', 'lead', 'prospect', 'analytics']
        marketing_content = ['campaign', 'click', 'conversion', 'lead', 'marketing']
        
        if any(word in filename_lower for word in marketing_keywords):
            return 'marketing'
        if any(word in content_lower for word in marketing_content):
            return 'marketing'
            
        return 'general'
    
    def extract_insights(self, df, category, filename):
        """
        Extract business insights based on file category
        """
        insights = {
            'filename': filename,
            'category': category,
            'processed_time': datetime.now().isoformat(),
            'row_count': df.count(),
            'column_count': len(df.columns),
            'columns': df.columns,
            'insights': [],
            'alerts': []
        }
        
        # Category-specific insight extraction
        if category == 'financial':
            insights['insights'] = self.extract_financial_insights(df)
        elif category == 'customer':
            insights['insights'] = self.extract_customer_insights(df)
        elif category == 'sales':
            insights['insights'] = self.extract_sales_insights(df)
        elif category == 'inventory':
            insights['insights'] = self.extract_inventory_insights(df)
        elif category == 'hr':
            insights['insights'] = self.extract_hr_insights(df)
        elif category == 'marketing':
            insights['insights'] = self.extract_marketing_insights(df)
        else:
            insights['insights'] = self.extract_general_insights(df)
            
        # Add data quality alerts
        insights['alerts'] = self.generate_alerts(df, insights)
        
        return insights
    
    def extract_financial_insights(self, df):
        """Extract financial insights and KPIs"""
        insights = []
        
        # Find amount/value columns
        amount_cols = [col for col in df.columns if any(word in col.lower() for word in 
                      ['amount', 'total', 'price', 'cost', 'value', 'revenue', 'expense'])]
        
        for col in amount_cols:
            try:
                # Clean and convert to numeric
                df_numeric = df.withColumn(col + '_clean', 
                    regexp_replace(col(col), '[^0-9.-]', '').cast('double'))
                
                # Calculate statistics
                stats = df_numeric.agg(
                    sum(col + '_clean').alias('total'),
                    avg(col + '_clean').alias('average'),
                    min(col + '_clean').alias('minimum'),
                    max(col + '_clean').alias('maximum'),
                    count(col + '_clean').alias('count')
                ).collect()[0]
                
                if stats['total']:
                    insights.append({
                        'metric': f'Total {col}',
                        'value': f"${stats['total']:,.2f}",
                        'type': 'financial'
                    })
                    insights.append({
                        'metric': f'Average {col}',
                        'value': f"${stats['average']:,.2f}",
                        'type': 'financial'
                    })
                    insights.append({
                        'metric': f'Highest {col}',
                        'value': f"${stats['maximum']:,.2f}",
                        'type': 'financial'
                    })
                    
            except Exception as e:
                print(f"Error processing column {col}: {str(e)}")
                
        # Find date patterns for trend analysis
        date_cols = [col for col in df.columns if any(word in col.lower() for word in 
                    ['date', 'time', 'created', 'updated'])]
        
        for col in date_cols:
            try:
                # Count transactions by month
                monthly_count = df.withColumn('month', month(col(col))).groupBy('month').count().collect()
                if monthly_count:
                    insights.append({
                        'metric': f'Monthly Distribution ({col})',
                        'value': f"{len(monthly_count)} months with data",
                        'type': 'trend'
                    })
            except:
                pass
                
        return insights
    
    def extract_customer_insights(self, df):
        """Extract customer-related insights"""
        insights = []
        
        # Email domain analysis
        email_cols = [col for col in df.columns if 'email' in col.lower()]
        for col in email_cols:
            try:
                domain_df = df.withColumn('domain', 
                    regexp_extract(col(col), '@([^.]+\.[^.]+)', 1))
                
                top_domains = domain_df.filter(col('domain') != '') \
                    .groupBy('domain').count() \
                    .orderBy(desc('count')) \
                    .limit(5).collect()
                
                if top_domains:
                    domain_list = [f"{row['domain']}: {row['count']}" for row in top_domains]
                    insights.append({
                        'metric': 'Top Email Domains',
                        'value': domain_list,
                        'type': 'demographic'
                    })
            except:
                pass
        
        # Geographic analysis
        location_cols = [col for col in df.columns if any(word in col.lower() for word in 
                        ['city', 'state', 'country', 'location', 'address'])]
        
        for col in location_cols:
            try:
                top_locations = df.groupBy(col).count() \
                    .orderBy(desc('count')) \
                    .limit(10).collect()
                
                if top_locations:
                    insights.append({
                        'metric': f'Top {col.title()}s',
                        'value': f"{len(top_locations)} unique locations",
                        'type': 'geographic'
                    })
            except:
                pass
                
        return insights
    
    def extract_sales_insights(self, df):
        """Extract sales performance insights"""
        insights = []
        
        # Quantity analysis
        qty_cols = [col for col in df.columns if any(word in col.lower() for word in 
                   ['quantity', 'qty', 'units', 'sold', 'volume'])]
        
        for col in qty_cols:
            try:
                stats = df.agg(
                    sum(col).alias('total'),
                    avg(col).alias('average'),
                    max(col).alias('maximum')
                ).collect()[0]
                
                if stats['total']:
                    insights.append({
                        'metric': f'Total {col}',
                        'value': f"{stats['total']:,}",
                        'type': 'volume'
                    })
                    insights.append({
                        'metric': f'Average {col}',
                        'value': f"{stats['average']:,.2f}",
                        'type': 'volume'
                    })
            except:
                pass
        
        # Product performance
        product_cols = [col for col in df.columns if any(word in col.lower() for word in 
                       ['product', 'item', 'sku', 'name'])]
        
        for col in product_cols:
            try:
                product_count = df.select(col).distinct().count()
                insights.append({
                    'metric': f'Unique {col}s',
                    'value': f"{product_count:,}",
                    'type': 'product'
                })
            except:
                pass
                
        return insights
    
    def extract_inventory_insights(self, df):
        """Extract inventory management insights"""
        insights = []
        
        # Stock level analysis
        stock_cols = [col for col in df.columns if any(word in col.lower() for word in 
                     ['stock', 'quantity', 'inventory', 'available', 'on_hand'])]
        
        for col in stock_cols:
            try:
                # Low stock alerts (less than 10 units)
                low_stock = df.filter(col(col) < 10).count()
                out_of_stock = df.filter(col(col) == 0).count()
                total_items = df.count()
                
                insights.append({
                    'metric': f'Low Stock Items ({col})',
                    'value': f"{low_stock} out of {total_items} items",
                    'type': 'alert'
                })
                
                if out_of_stock > 0:
                    insights.append({
                        'metric': f'Out of Stock Items ({col})',
                        'value': f"{out_of_stock} items",
                        'type': 'critical'
                    })
                    
                # Average stock level
                avg_stock = df.agg(avg(col)).collect()[0][0]
                if avg_stock:
                    insights.append({
                        'metric': f'Average Stock Level ({col})',
                        'value': f"{avg_stock:.2f} units",
                        'type': 'metric'
                    })
                    
            except:
                pass
                
        return insights
    
    def extract_hr_insights(self, df):
        """Extract HR and employee insights"""
        insights = []
        
        # Department analysis
        dept_cols = [col for col in df.columns if any(word in col.lower() for word in 
                    ['department', 'dept', 'division', 'team'])]
        
        for col in dept_cols:
            try:
                dept_count = df.groupBy(col).count().orderBy(desc('count')).collect()
                if dept_count:
                    insights.append({
                        'metric': f'Departments ({col})',
                        'value': f"{len(dept_count)} departments",
                        'type': 'organizational'
                    })
            except:
                pass
        
        # Salary analysis
        salary_cols = [col for col in df.columns if any(word in col.lower() for word in 
                      ['salary', 'wage', 'pay', 'compensation'])]
        
        for col in salary_cols:
            try:
                salary_stats = df.agg(
                    avg(col).alias('average'),
                    min(col).alias('minimum'),
                    max(col).alias('maximum')
                ).collect()[0]
                
                if salary_stats['average']:
                    insights.append({
                        'metric': f'Average {col}',
                        'value': f"${salary_stats['average']:,.2f}",
                        'type': 'compensation'
                    })
            except:
                pass
                
        return insights
    
    def extract_marketing_insights(self, df):
        """Extract marketing campaign insights"""
        insights = []
        
        # Campaign performance
        campaign_cols = [col for col in df.columns if any(word in col.lower() for word in 
                        ['campaign', 'source', 'medium', 'channel'])]
        
        for col in campaign_cols:
            try:
                campaign_count = df.select(col).distinct().count()
                insights.append({
                    'metric': f'Unique {col}s',
                    'value': f"{campaign_count:,}",
                    'type': 'campaign'
                })
            except:
                pass
        
        # Conversion metrics
        conversion_cols = [col for col in df.columns if any(word in col.lower() for word in 
                          ['conversion', 'click', 'impression', 'view'])]
        
        for col in conversion_cols:
            try:
                total_conversions = df.agg(sum(col)).collect()[0][0]
                if total_conversions:
                    insights.append({
                        'metric': f'Total {col}s',
                        'value': f"{total_conversions:,}",
                        'type': 'performance'
                    })
            except:
                pass
                
        return insights
    
    def extract_general_insights(self, df):
        """Extract general data quality and basic insights"""
        insights = []
        
        # Data quality metrics
        total_rows = df.count()
        
        for col_name in df.columns:
            try:
                null_count = df.filter(col(col_name).isNull() | (col(col_name) == "")).count()
                unique_count = df.select(col_name).distinct().count()
                
                # Data completeness
                completeness = ((total_rows - null_count) / total_rows) * 100
                insights.append({
                    'metric': f'Data Completeness - {col_name}',
                    'value': f"{completeness:.1f}%",
                    'type': 'quality'
                })
                
                # Uniqueness ratio
                uniqueness = (unique_count / total_rows) * 100
                insights.append({
                    'metric': f'Uniqueness - {col_name}',
                    'value': f"{uniqueness:.1f}%",
                    'type': 'quality'
                })
                
            except:
                pass
                
        return insights[:20]  # Limit to top 20 insights
    
    def generate_alerts(self, df, insights):
        """Generate data quality and business alerts"""
        alerts = []
        
        # Data quality alerts
        total_rows = df.count()
        
        for col_name in df.columns:
            try:
                null_count = df.filter(col(col_name).isNull() | (col(col_name) == "")).count()
                null_percentage = (null_count / total_rows) * 100
                
                if null_percentage > 50:
                    alerts.append({
                        'type': 'CRITICAL',
                        'message': f'Column {col_name} has {null_percentage:.1f}% missing values',
                        'severity': 'high'
                    })
                elif null_percentage > 25:
                    alerts.append({
                        'type': 'WARNING',
                        'message': f'Column {col_name} has {null_percentage:.1f}% missing values',
                        'severity': 'medium'
                    })
                    
            except:
                pass
        
        # Business-specific alerts
        category = insights['category']
        
        if category == 'financial':
            # Check for negative amounts
            amount_cols = [col for col in df.columns if any(word in col.lower() for word in 
                          ['amount', 'total', 'price', 'cost'])]
            for col in amount_cols:
                try:
                    negative_count = df.filter(col(col) < 0).count()
                    if negative_count > 0:
                        alerts.append({
                            'type': 'BUSINESS',
                            'message': f'{negative_count} negative values found in {col}',
                            'severity': 'medium'
                        })
                except:
                    pass
        
        elif category == 'inventory':
            # Check for out of stock items
            stock_cols = [col for col in df.columns if any(word in col.lower() for word in 
                         ['stock', 'quantity', 'inventory'])]
            for col in stock_cols:
                try:
                    out_of_stock = df.filter(col(col) == 0).count()
                    if out_of_stock > 0:
                        alerts.append({
                            'type': 'BUSINESS',
                            'message': f'{out_of_stock} items are out of stock',
                            'severity': 'high'
                        })
                except:
                    pass
                    
        return alerts
    
    def clean_and_enhance_data(self, df):
        """Clean and enhance the dataset"""
        cleaned_df = df
        
        # Remove completely empty rows
        cleaned_df = cleaned_df.dropna(how='all')
        
        # Trim whitespace from string columns
        for col_name, col_type in cleaned_df.dtypes:
            if col_type == 'string':
                cleaned_df = cleaned_df.withColumn(col_name, trim(col(col_name)))
        
        # Add processing metadata
        cleaned_df = cleaned_df.withColumn('processed_date', current_timestamp())
        
        return cleaned_df
    
    def save_insights_report(self, all_insights):
        """Save comprehensive insights report"""
        try:
            # Create summary report
            summary = {
                'report_generated': datetime.now().isoformat(),
                'total_files_processed': len(all_insights),
                'categories_found': list(set([insight['category'] for insight in all_insights])),
                'total_rows_processed': sum([insight['row_count'] for insight in all_insights]),
                'critical_alerts': sum([len([alert for alert in insight['alerts'] if alert['severity'] == 'high']) 
                                      for insight in all_insights]),
                'detailed_insights': all_insights
            }
            
            # Save as JSON
            summary_df = spark.createDataFrame([{"report": json.dumps(summary, indent=2)}])
            summary_df.coalesce(1).write.mode('overwrite').json(f"s3://{INSIGHTS_BUCKET}/summary_report")
            
            # Save individual category reports
            for category in summary['categories_found']:
                category_insights = [insight for insight in all_insights if insight['category'] == category]
                category_df = spark.createDataFrame([{"insights": json.dumps(category_insights, indent=2)}])
                category_df.coalesce(1).write.mode('overwrite').json(f"s3://{INSIGHTS_BUCKET}/category_reports/{category}")
            
            return summary
            
        except Exception as e:
            print(f"Error saving insights report: {str(e)}")
            return None

def main():
    """Main processing function"""
    processor = SmartFileProcessor()
    
    print("🚀 Starting Smart File Processor...")
    print(f"📁 Input Bucket: {INPUT_BUCKET}")
    print(f"📁 Output Bucket: {OUTPUT_BUCKET}")
    print(f"📁 Insights Bucket: {INSIGHTS_BUCKET}")
    
    try:
        # List all files in input bucket
        response = processor.s3.list_objects_v2(Bucket=INPUT_BUCKET)
        
        if 'Contents' not in response:
            print("❌ No files found in input bucket")
            return
        
        all_insights = []
        processed_count = 0
        error_count = 0
        
        print(f"📊 Found {len(response['Contents'])} objects to process")
        
        for obj in response['Contents']:
            file_key = obj['Key']
            
            # Skip folders
            if file_key.endswith('/'):
                continue
            
            print(f"\n🔄 Processing: {file_key}")
            
            try:
                # Read file based on extension
                input_path = f"s3://{INPUT_BUCKET}/{file_key}"
                
                if file_key.lower().endswith('.csv'):
                    df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)
                elif file_key.lower().endswith('.json'):
                    df = spark.read.json(input_path)
                elif file_key.lower().endswith('.parquet'):
                    df = spark.read.parquet(input_path)
                else:
                    print(f"⚠️  Skipping unsupported file format: {file_key}")
                    continue
                
                # Basic validation
                if df.count() == 0:
                    print(f"⚠️  Empty file: {file_key}")
                    continue
                
                # Get sample content for categorization
                sample_rows = df.limit(5).collect()
                sample_content = ' '.join([str(row) for row in sample_rows])
                
                # Categorize the file
                category = processor.categorize_file(file_key, sample_content)
                print(f"📂 Categorized as: {category}")
                
                # Extract insights
                insights = processor.extract_insights(df, category, file_key)
                all_insights.append(insights)
                
                # Clean and enhance data
                cleaned_df = processor.clean_and_enhance_data(df)
                
                # Save categorized file to output bucket
                output_path = f"s3://{OUTPUT_BUCKET}/{category}/{file_key}"
                cleaned_df.coalesce(1).write.mode('overwrite').option("header", "true").csv(output_path)
                
                processed_count += 1
                
                print(f"✅ Success! Found {len(insights['insights'])} insights")
                if insights['alerts']:
                    print(f"⚠️  {len(insights['alerts'])} alerts generated")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error processing {file_key}: {str(e)}")
                continue
        
        # Generate and save comprehensive report
        if all_insights:
            print(f"\n📋 Generating comprehensive insights report...")
            summary = processor.save_insights_report(all_insights)
            
            if summary:
                print(f"\n🎉 PROCESSING COMPLETE!")
                print(f"✅ Successfully processed: {processed_count} files")
                print(f"❌ Errors: {error_count} files")
                print(f"📊 Total rows processed: {summary['total_rows_processed']:,}")
                print(f"📂 Categories found: {', '.join(summary['categories_found'])}")
                print(f"🚨 Critical alerts: {summary['critical_alerts']}")
                print(f"\n📁 Check your buckets:")
                print(f"   • Organized files: s3://{OUTPUT_BUCKET}/")
                print(f"   • Insights reports: s3://{INSIGHTS_BUCKET}/")
            else:
                print("❌ Error generating summary report")
        else:
            print("❌ No files were successfully processed")
            
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()

# Commit the job
job.commit()
