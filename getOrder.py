import boto3

def handler(event, context):
   
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pizzorder')
    
    response = table.get_item(
        Key = {'order_id': event['order-id']}
    ) 
    item = response['Item']
    return item
  