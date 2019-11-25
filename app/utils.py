#import mysql.connector
#from flask import g
#import boto3
#from botocore.exceptions import ClientError
#import logging
import hashlib
import random

from app import webapp
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)





def encryptString(string):
    sha_signature = hashlib.sha256(string.encode()).hexdigest()
    return sha_signature

def randomString(length):
    result = ""
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    charactersLength = len(characters)
    for i in range(length):
        result += characters[random.randint(0, charactersLength - 1)]
    print(result)
    return result

