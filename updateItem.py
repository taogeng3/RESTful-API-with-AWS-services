import boto3

def handler(event, context):
 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('menu')

    for i in event.keys():
        if i != 'menu_id':
            table.update_item(
                Key={'menu_id': event['menu_id']}, 
                UpdateExpression = 'SET ' + i + '= :a',
                ExpressionAttributeValues = {':a' : event[i]}
            )

    table.update_item(
        Key={'menu_id': event['menu_id']}, 
        UpdateExpression = 'SET sequences = :s',
        ExpressionAttributeValues = {':s' : ['selection', 'size']},
        ReturnValues="ALL_NEW"
    )