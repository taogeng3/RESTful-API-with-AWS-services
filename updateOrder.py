import boto3
from datetime import datetime, timedelta

state = 0

def handler(event, context):
   
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pizzorder')
    menu_table = dynamodb.Table('menu')

    order_response = table.get_item(
        Key = {'order_id': event['order-id']}
    ) 
    order_item = order_response['Item']
    menu_id = order_item. get('menu_id')

    menu_response = menu_table.get_item(
        Key = {'menu_id': menu_id}
    ) 
    menu_item = menu_response['Item']
    menu_selection = menu_item. get('selection')
    menu_size = menu_item. get('size')
    menu_price = menu_item. get('price')

    global state
    if state == 0: 
        input_selection_index = int(event['input'])-1 
        selection_limit = len(menu_selection)
        if input_selection_index <= selection_limit:
            selection = menu_selection[input_selection_index]
        else:
            return "Please input numbers <= %d" % selection_limit
        
        table.update_item(
            Key={'order_id': event['order-id']}, 
            UpdateExpression = 'SET orders = :s',
            ExpressionAttributeValues = {
                ':s' : {'selection':selection}
            },
            ReturnValues="ALL_NEW"
        )
    
        index = 1
        ms = ''
        for s in menu_size:
            ms += str(index) + '. ' + s + ', '
            index += 1
        menu_size_string = ms[:len(ms)-2]

        response1 = {"Message": "Which size do you want? %s" % menu_size_string}
        state = 1
        return response1
    
    elif state == 1:
        input_size_index = int(event['input'])-1 
        size_limit = len(menu_size)
        if input_size_index <= size_limit:
            size = menu_size[input_size_index]
            costs = menu_price[input_size_index]
        else:
            return "Please input numbers <= %d" % size_limit

        
        table.update_item(
            Key={'order_id': event['order-id']}, 
            UpdateExpression = 'SET orders.size = :i, orders.costs = :c, orders.order_time = :t, order_status = :o',
            ExpressionAttributeValues = {
                ':i': size, 
                ':c': costs,
                ':t': format(datetime.now()+timedelta(hours=-7), '%m-%d-%Y@%H:%M:%S'),
                ':o': 'processing'
            },
            ReturnValues="ALL_NEW"
        )    
        
        update_response = table.get_item(
            Key={'order_id': event['order-id']}
        )
        update_costs = update_response['Item']['orders']['costs']
        response2 = {"Message": ("Your order costs $%s. We will email you when the order is ready. " 
                     "Thank you!" % update_costs)}
        state = 0
        return response2