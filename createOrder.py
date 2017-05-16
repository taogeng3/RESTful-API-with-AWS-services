import boto3

def handler(event, context):
 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pizzorder')
    menu_table = dynamodb.Table('menu')

    menu_id = event['menu_id']
    menu_response = menu_table.get_item(
        Key = {'menu_id': menu_id}
    ) 
    menu_item = menu_response['Item']
   
    if menu_item:
        table.put_item(
            Item = {
                'menu_id':menu_id,
                'order_id':event['order_id'],
                'customer_name':event['customer_name'],
                'customer_email':event['customer_email']
            }
        )
    else:
        return "Wrong menu_id!"

    index = 1
    selection = ''
    for s in menu_item. get('selection'):
        selection += str(index) + '. ' + s + ', '
        index += 1
    selection = selection[:len(selection)-2]

    response = {
        "Message": "Hi %s, please choose one of these selection: %s" % (event['customer_name'], selection)
               }
    return response