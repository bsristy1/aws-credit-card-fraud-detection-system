****AWS Serverless Fraud Detection System****

A completely serverless, end-to-end machine learning pipeline that detects fraud credit card transactions in real time. This system ingests transaction data via an API, processes it using AWS Lambda, evaluates it against an XGBoost model hosted on Amazon SageMaker, and stores the results for analytics in QuickSight.


## Architecture
Flow: User/App → API Gateway → AWS Lambda → SageMaker Endpoint → S3 → Athena → QuickSight
 → User submits a transaction via API Gateway 
 → AWS Lambda receives the payload and invokes the ML model.
 → Amazon SageMaker (XGBoost) predicts the probability of fraud.
 → Transaction data and fraud scores are saved to Amazon S3.
 → Amazon Athena queries historical logs.
 → Amazon QuickSight displays fraud trends and risk distribution.

## Features
Real-Time Inference: fraud probability scoring.
Serverless Infrastructure: Zero server management using Lambda/API Gateway.
Data Lake Integration: All predictions are automatically archived in S3 for auditing.
SQL Analytics: Query fraud patterns instantly using standard SQL via Athena.
Dashboarding: Visual insights into high risk merchants/transaction spikes.

## Tools & Services
Cloud Provider: Amazon Web Services (AWS)
Machine Learning: XGBoost, Scikit-Learn, Pandas
Compute: AWS Lambda (Serverless), SageMaker (Inference)
Storage & Database: Amazon S3, AWS Glue, Amazon Athena
API Management: Amazon API Gateway
Visualization: Amazon QuickSight
