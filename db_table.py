import boto3
from app.utils import *
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

table = dynamodb.Table('city')
table.put_item(
            Item={
           'cityId':randomString(10) ,
           'name': "Toronto",
           'country':"Canada"
           }
         )
table.put_item(
            Item={
           'cityId':randomString(10) ,
           'name': "Vancouver",
           'country':"Canada"
           }
         )