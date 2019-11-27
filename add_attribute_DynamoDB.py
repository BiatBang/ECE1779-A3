import boto3

dynamodb = boto3.resource('dynamodb')
spot_table = dynamodb.Table('spot')
user_table = dynamodb.Table('user')

# Add new attribute for all items
# spot: rating avg, rating num, review num, reviews (finished)
# user: ratings:{spotId: rating, ...] num: 1-5
# function: add review, del review

response = spot_table.scan(ProjectionExpression='spotId')

items = response['Items']
for item in items:
    reponse = spot_table.update_item(
        Key=item,
        UpdateExpression='SET #rAvg = :ratingAvg, #rNum = :ratingNum, #reviewNum = :reviewNum, #reviews = :reviews',
        ExpressionAttributeNames={
            '#rAvg': 'ratingAvg',
            '#rNum': 'ratingNum',
            '#reviewNum': 'reviewNum',
            '#reviews': 'reviews'
        },
        ExpressionAttributeValues={
            ':ratingAvg': 0,
            ':ratingNum': 0,
            ':reviewNum': 0,
            ':reviews': {}
        }
    )
