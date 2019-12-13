# ECE1779-A3
a trip scheduler made with flask and deployed on aws lambda
## What does it use?
AWS: dynamodb, s3, personalize, lambda
Zappa
JQXscheduler
## How to use it?
### database
There are 5 "tables" in dynamodb:
```
user -> userId
city -> cityId
spot -> spotId
click -> spotId
user-habit -> habitId
```
Get city and spot information via [cityScraper](https://github.com/BiatBang/cityScraper) and data will be automatically inserted into your dynamodb.
### configurations
In app/config, there are configuration file(s). Change the value there to your own configurations.

If you still can't run it on your device, let it go. Cheers.