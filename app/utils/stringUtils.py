import random
from datetime import datetime
import hashlib

def randomString(length):
    result = ""
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    charactersLength = len(characters)
    for i in range(length):
        result += characters[random.randint(0, charactersLength - 1)]
    return result

def encryptString(string):
    sha_signature = hashlib.sha256(string.encode()).hexdigest()
    return sha_signature

def getDateSlot(spotSlots):
    # given spotslots, get a start date and end date
    dates = []
    for slot in spotSlots:
        dates.append(slot['from'][:10])
    if not dates:
        return None, None
    dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    return dates[0], dates[-1]