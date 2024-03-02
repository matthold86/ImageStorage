import boto3
import json

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    return response

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
    
    body = json.loads(event['body'])
    bar_name = body['barName']
    drink_name = body['drinkName']
    # file_ext = body['ext']
    bucket_name = 'cocktail-recommendations'
    object_name = f"cocktail-pictures/{bar_name}/{drink_name}.jpg"
    presigned_url = generate_presigned_url(bucket_name, object_name)
    return {
        'statusCode': 200,
        'body': json.dumps({'url': presigned_url})
    }
    # return {
    #     'body': body
    # }