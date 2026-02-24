import json
import boto3
import os


runtime = boto3.client('sagemaker-runtime')
ENDPOINT_NAME = os.environ.get('ENDPOINT_NAME', 'fraud-endpoint')




def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    try:
       
        if 'body' in event:
            payload = json.loads(event['body'])
        else:
            payload = event
        
       
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
       
        result = json.loads(response['Body'].read().decode())
        
        return {
            'statusCode': 200,
            'body': json.dumps({'fraud_probability': result})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }