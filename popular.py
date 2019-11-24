import threading
import os
from config import clickRecord
from app.utils import awsUtils

filename = clickRecord
threshold = 5

awsSuite = awsUtils.AWSSuite()

def count_popularity(pop_list):
    # set poplular spot last fifteen minutes to 0 in DB
    for spotId in pop_list:
        awsSuite.unsetSpotPop(spotId)

    # count new rounf
    click_dict = {}
    try:
        with open(filename, 'r') as f:
            for spotId in f:
                if click_dict.get(spotId.strip()) == None:
                    click_dict[spotId.strip()] = 1
                else:
                    click_dict[spotId.strip()] += 1
        print(click_dict)
        
        pop_list = []
        for (spotId, count) in click_dict.items():
            if count >= threshold:
                pop_list.append(spotId)
                awsSuite.setSpotPop(spotId)

        os.remove(filename)
    except:
        print('File not exist')

    
    # Set a timer for checking every two minutes
    timer = threading.Timer(20, count_popularity, [pop_list])
    timer.start() 


if __name__ == '__main__':
    pop_list = []
    count_popularity(pop_list)
