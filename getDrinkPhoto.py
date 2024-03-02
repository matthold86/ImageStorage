import json
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Specify your DynamoDB table name
table_name = 'drink_images'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    operation = event['httpMethod']
    if operation == 'OPTIONS':
        # Return a 200 OK response with CORS headers
        return {
            'statusCode': '200',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Specify allowed origin(s) here
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',  # Specify allowed methods here
                'Access-Control-Allow-Headers': 'Content-Type, X-Amz-Date, Authorization, X-Api-Key',  # Specify allowed headers here
            },
            'body': json.dumps({'message': 'CORS preflight response'}),
        }
    
    
    # Parse the incoming JSON payload
    body = json.loads(event['body'])
    bar_name = body['barName']
    drink_name = body['drinkName']
    
    # Query DynamoDB using the Bar Name and Drink Name as keys
    response = table.get_item(
        Key={
            'barName': bar_name,
            'drinkName': drink_name
        }
    )
    
    # Check if the item was found
    if 'Item' in response:
        item = response['Item']
        # Extract the ObjectURL attribute
        object_url = item.get('s3ObjectKey', 'URL not found')
        return {
            'statusCode': 200,
            'body': json.dumps({'s3ObjectKey': object_url}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Item not found'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
