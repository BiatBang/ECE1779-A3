import boto3
client = boto3.Session(region_name='us-east-1', profile_name='default').client('dynamodb')
response = client.scan(TableName='city')
print(response)