import boto3


class AWSSuite():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def getUserById(self, userId):
        userTable = self.dynamodb.Table('user')
        response = userTable.get_item(Key={'userId': userId})
        if 'Item' in response:
            userItem = response['Item']
        else:
            userItem = None
        return userItem

    def getSpotById(self, spotId):
        spotTable = self.dynamodb.Table('spot')
        response = spotTable.get_item(Key={'spotId': spotId})
        if 'Item' in response:
            spotItem = response['Item']
        else:
            spotItem = None
        return spotItem


    def addOneClick(self, spotId):
        spotTable = self.dynamodb.Table('spot')
        response = spotTable.get_item(Key={'spotId': spotId})
        response['Item']['count'] += 1