import boto3

def handler(event, context):
 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('menu')

    table.delete_item(
           Key={'menu_id': event['menu-id']}
    )
      