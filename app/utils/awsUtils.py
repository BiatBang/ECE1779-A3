import boto3
from app.utils import stringUtils
from boto3.dynamodb.conditions import Key, Attr

SCHEDULEEXISTED = 10000

class AWSSuite():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.userTable = self.dynamodb.Table('user')
        self.spotTable = self.dynamodb.Table('spot')
        self.cityTable = self.dynamodb.Table('city')

    def getUserById(self, userId):
        response = self.userTable.get_item(Key={'userId': userId})
        if 'Item' in response:
            userItem = response['Item']
        else:
            userItem = None
        return userItem

    def getSpotById(self, spotId):    
        response = self.spotTable.get_item(Key={'spotId': spotId})
        if 'Item' in response:
            spotItem = response['Item']
        else:
            spotItem = None
        return spotItem

    def getCityById(self, cityId):
        response = self.cityTable.get_item(Key={'cityId': cityId})
        if 'Item' in response:
            cityItem = response['Item']
        else:
            cityItem = None
        return cityItem

    def getSchedules(self, userId):
        response = self.userTable.get_item(Key={'userId': userId})
        schedulesItems = []
        userItem = None
        if 'Item' in response:
            userItem = response['Item']
            if 'schedules' in userItem:
                schedulesItems = userItem['schedules']
        return schedulesItems

    def getCartByUserId(self, userId):
        response = self.userTable.get_item(Key={'userId': userId})
        cartItem = None
        if 'Item' in response:
            userItem = response['Item']
            if 'cart' in userItem:
                cartItem = userItem['cart']
        return cartItem

    def addSpotToCart(self, userId, spotId):
        response = self.userTable.get_item(Key={'userId': userId})
        cartItem = []
        if 'Item' in response:
            userItem = response['Item']
            if 'cart' in userItem:
                cartItem = userItem['cart']
        if spotId not in cartItem:
            cartItem.append(spotId)
        self.userTable.update_item(Key={'userId': userId},
                          UpdateExpression="SET cart = :val",
                          ExpressionAttributeValues={
                              ":val": cartItem
                          })

    def removeSpotFromCart(self, userId, spotId):
        response = self.userTable.get_item(Key={'userId': userId})
        cartItem = []
        if 'Item' in response:
            userItem = response['Item']
            if 'cart' in userItem:
                cartItem = userItem['cart']
        if spotId in cartItem:
            cartItem.remove(spotId)
        self.userTable.update_item(Key={'userId': userId},
                          UpdateExpression="SET cart = :val",
                          ExpressionAttributeValues={
                              ":val": cartItem
                          })

    def saveSchedule(self, userId, scheduleName, spotSlots, isNewSchedule):
        response = self.userTable.get_item(Key={'userId': userId})
        schedules = []
        if 'Item' in response:
            userItem = response['Item']
            if 'schedules' in userItem:
                schedules = userItem['schedules']
        slots = []
        for schedule in schedules:
            if isNewSchedule and scheduleName == schedule['scheduleName']:
                return SCHEDULEEXISTED
            if scheduleName == schedule['scheduleName']:
                schedules.remove(schedule)    
        for slot in spotSlots:
            sl = {
                'spotId': slot['spotId'],
                'name': slot['name'],
                'description': slot['description'],
                'time': {
                    'date': slot['from'][:10],
                    'timeFrom': slot['from'][11:19],
                    'timeTo': slot['to'][11:19]
                } 
            }
            slots.append(sl)
        dateFrom, dateTo = stringUtils.getDateSlot(spotSlots)
        schedule = {
            'scheduleName': scheduleName,
            'dateFrom': dateFrom,
            'dateTo': dateTo,
            'slots': slots
        }
        schedules.append(schedule)
        print(schedules)
        self.userTable.update_item(Key={'userId': userId},
                          UpdateExpression="SET schedules = :val",
                          ExpressionAttributeValues={
                              ":val": schedules
                          })

    def getSlotsFromScheduleName(self, userId, scheduleName):
        response = self.userTable.get_item(Key={'userId': userId})
        schedules = []
        if 'Item' in response:
            userItem = response['Item']
            if 'schedules' in userItem:
                schedules = userItem['schedules']
        slots = []
        # here change the slot format to appointment format, big project
        """
        var appointment = {
            id: "id1",
            subject: res.name,
            location: res.location,
            description: res.description,
            resourceId: res.spotId,
            start: new Date(year, parseInt(month) - 1, day, sthour, stmin, 0),
            end: new Date(year, parseInt(month) - 1, day, ethour, etmin, 0)
        }
        """
        appointments = []
        for schedule in schedules:
            if scheduleName == schedule['scheduleName']:
                slots = schedule['slots']
                for slot in slots:
                    spotItem = None
                    print("spotId", slot['spotId'])
                    response = self.spotTable.get_item(Key={'spotId': slot['spotId']})
                    if 'Item' in response:
                        spotItem = response['Item']
                    print("location", spotItem['location'])
                    app = {
                        'id': slot['spotId'],
                        'subject': slot['name'],
                        'location': spotItem['location'],
                        'description': slot['description'],
                        'resourceId': slot['spotId'],
                        'start': slot['time']['date']+"-"+slot['time']['timeFrom'],
                        'end': slot['time']['date']+"-"+slot['time']['timeTo']
                    } 
                    appointments.append(app)
        return appointments

    def getCityByName(self, cityName):
        cityItem = self.cityTable.scan(FilterExpression=Key('name').eq(cityName))
        if 'Items' in cityItem and len(cityItem['Items']) > 0:
            return cityItem['Items'][0]
        else:
            return None
                 