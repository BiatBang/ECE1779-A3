import threading
import os
from config import clickRecord
import boto3
from boto3.dynamodb.conditions import Key, Attr

filename = clickRecord
threshold = 5
updateInterval = 20 # seconds

class AWSSuite():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.spotTable = self.dynamodb.Table('spot')
        self.clickTable = self.dynamodb.Table('click')

    def setSpotPop(self, spotId):
        response = self.spotTable.get_item(Key={'spotId': spotId})
        spotItem = response['Item']
        self.spotTable.update_item(Key={'spotId': spotId},
                            UpdateExpression="SET #count = :val",
                            ExpressionAttributeValues={
                                ":val": 1
                            },
                            ExpressionAttributeNames={
                                "#count": "count"
                            })

    def unsetSpotPop(self, spotId):
        response = self.spotTable.get_item(Key={'spotId': spotId})
        spotItem = response['Item']
        self.spotTable.update_item(Key={'spotId': spotId},
                            UpdateExpression="SET #count = :val",
                            ExpressionAttributeValues={
                                ":val": 0
                            },
                            ExpressionAttributeNames={
                                "#count": "count"
                            })  

    def filterPopSpot(self, threshold):
        response = self.clickTable.scan(
            FilterExpression=Attr('count').gt(threshold)
        )
        if 'Item' in response:
            popSpots = response['Item']
        else:
            popSpots = None
        return popSpots

    def clearClickTable(self):
        scan = self.clickTable.scan()
        with self.clickTable.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(
                    Key={'spotId': each['spotId']}
                )

awsSuite = AWSSuite()
def count_popularity(popSpots):
    # set poplular spot last fifteen minutes to 0 in DB
    if popSpots is not None:
        for spot in popSpots:
            awsSuite.unsetSpotPop(spot['spotId'])

    # retrive popular spot from spot table
    popSpots = awsSuite.filterPopSpot(threshold)

    # clear click table
    awsSuite.clearClickTable()

    # set popular spot to spot table
    if popSpots is not None:
        for spot in popSpots:
            awsSuite.setSpotPop(spot['spotId'])
    print(popSpots)

    # Set a timer for checking every two minutes
    timer = threading.Timer(updateInterval, count_popularity, [popSpots])
    timer.start() 


if __name__ == '__main__':
    popSpots = None
    count_popularity(popSpots)
