
import hashlib
import random

from app import webapp
import boto3
import json
import decimal


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

