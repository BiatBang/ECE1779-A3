import boto3
# from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr
import threading

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
client = boto3.client('dynamodb')

def count_popularity(click_dict):
    table = dynamodb.Table('spot')

    # find out the popular spots 
    response = table.scan(
        FilterExpression=Attr('count').gte(5),
        ProjectionExpression="spotId"
    )
    items = response['Items']

    # update 'Pop' of these spots to 1
    

    # update all counts to zero

    response = table.update_item(
       Key={
            'count': 4,
        },
        UpdateExpression = "set rating = :r, plot=:p, actors=:a",
        ExpressionAttributeValues = {
           ':r': rating,
           ':p': "Everything happens all at once.",
           ':a': ["Larry", "Moe", "Curly"]
        }

    )
    
    # Set a timer for checking every two minutes
    timer = threading.Timer(60*10, count_popularity, [click_dict])
    timer.start() 


if __name__ == '__main__':
    click_dict = {}
    count_popularity(click_dict)
