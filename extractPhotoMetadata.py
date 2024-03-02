import boto3
import urllib.parse

# Initialize the S3 and DynamoDB clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Specify your DynamoDB table name
table_name = 'drink_images'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Extract bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    
    # Extract "Bar Name" and "Drink Name" from the object key
    # Assuming the object key format is "some/path/Bar Name/Drink Name.extension"
    key_parts = object_key.split('/')
    bar_name = key_parts[-2]  # Bar Name is second last
    drink_name_with_extension = key_parts[-1]
    drink_name = '.'.join(drink_name_with_extension.split('.')[:-1])  # Remove the file extension
    
    # Check if item exists
    response = table.get_item(
        Key={
            'barName': bar_name,
            'drinkName': drink_name
        }
    )
    
    # If item exists, update it, otherwise put a new item
    if 'Item' in response:
        # Update existing item
        table.update_item(
            Key={
                'BarName': bar_name,
                'DrinkName': drink_name
            },
            UpdateExpression='SET s3ObjectKey = :val1',
            ExpressionAttributeValues={
                ':val1': object_url
            }
        )
    else:
        # Insert new item
        table.put_item(
            Item={
                'barName': bar_name,
                'drinkName': drink_name,
                's3ObjectKey': object_url
            }
        )
    
    return {
        'statusCode': 200,
        'body': f"Successfully processed {object_key}."
    }
