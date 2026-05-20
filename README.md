**Stock-Market-Real-Time-Data-Analytics-Pipeline-on-AWS**
Designed and implemented a real-time stock market analysis system using AWS serverless technologies for scalable cloud-based financial data processing.

**Real-Time Stock Market Data Analytics Pipeline on AWS**

**Overview of Project**

This project builds a real-time stock market data analytics pipeline using AWS, leveraging event-driven architecture and serverless technologies. The system is designed to ingest, process, store, and analyze live stock market data efficiently while minimizing infrastructure and operational costs.

The pipeline streams stock market data in real time, processes incoming records using AWS Lambda, stores both raw and processed data in scalable AWS storage services, performs analytical querying using Amazon Athena, visualizes insights using Amazon QuickSight, and generates intelligent alerts for stock market trends and anomalies.


**Key Features**

*  Real-time stock data ingestion
*  Serverless event-driven architecture
*  Real-time analytics and anomaly detection
*  Interactive data visualization using Amazon QuickSight
*  Long-term historical data storage
*  SQL-based querying using Amazon Athena
*  Automated stock trend alerts via SNS
*  Fully scalable AWS cloud architecture


**AWS Services Used**

| AWS Service                 | Purpose                             |
| --------------------------- | ----------------------------------- |
| Amazon Kinesis Data Streams | Real-time stock data streaming      |
| AWS Lambda                  | Data processing & anomaly detection |
| Amazon DynamoDB             | Low-latency processed data storage  |
| Amazon S3                   | Raw stock data storage              |
| Amazon Athena               | Historical data querying            |
| Amazon QuickSight           | Data visualization & dashboards     |
| Amazon SNS                  | Email/SMS stock alerts              |
| AWS IAM                     | Secure permissions & access control |
| Amazon CloudWatch           | Monitoring & logging                |


**Architecture Workflow**

<img width="1536" height="1024" alt="Architecture" src="https://github.com/user-attachments/assets/b83b013d-2077-4dd3-84d5-8551041c2a79" />

Step-by-Step Workflow

**Step 1 — Real-Time Stock Data Ingestion**

Real-time stock market data is fetched using Python libraries such as:

* yfinance
* pandas
* boto3

The producer application continuously retrieves live stock market data and pushes the records into Amazon Kinesis Data Streams.

Services Used

* Python
* Amazon Kinesis Data Streams

**Step 2 — Stream Processing using AWS Lambda**

AWS Lambda is triggered automatically whenever new stock records arrive in Kinesis.

The Lambda function:

* Processes incoming stock data
* Performs transformations
* Detects anomalies and trends
* Filters important stock events

Services Used

* AWS Lambda
* Amazon Kinesis

**Step 3 — Store Processed Data in DynamoDB**

Processed stock records are stored in Amazon DynamoDB for:

* Fast retrieval
* Real-time dashboard querying
* Low-latency access

Services Used

* Amazon DynamoDB


**Step 4 — Store Raw Data in Amazon S3**

Raw incoming stock market data is archived in Amazon S3 for:

* Historical analysis
* Data lake storage
* Long-term analytics

Services Used

* Amazon S3

**Step 5 — Historical Querying using Amazon Athena **

Amazon Athena is used to run SQL queries directly on the stock data stored in S3.

This allows:

* Trend analysis
* Historical comparisons
* Analytical reporting

Services Used

* Amazon Athena


**Step 6 — Data Visualization using Amazon QuickSight **

Amazon QuickSight is connected with Athena datasets to build interactive dashboards and visual analytics for stock market trends.

The dashboard provides:

* Real-time stock insights
* Historical trend visualization
* Interactive charts and graphs
* Comparative stock analysis

Services Used

* Amazon QuickSight
* Amazon Athena

**Step 7 — Real-Time Alerts using SNS**

When stock anomalies or threshold conditions are detected, AWS Lambda triggers Amazon SNS notifications.

Notifications can be sent through:

* Email
* SMS

 Services Used
* AWS Lambda
* Amazon SNS



**Tech Stack**

* Python
* AWS Lambda
* Amazon Kinesis
* Amazon S3
* Amazon DynamoDB
* Amazon Athena
* Amazon QuickSight
* Amazon SNS
* Pandas
* yFinance
* Boto3



Author
Aman Yadav
Cloud & Software Developer passionate about building scalable AWS-based real-time analytics systems.

