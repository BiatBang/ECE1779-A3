from app.utils import awsUtils

awsSuite = awsUtils.AWSSuite()

awsSuite.deleteSchedule('123qwe', 'plan2')