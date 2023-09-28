import settings
import pymongo
from pymongo import ASCENDING
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def timedelta_to_months(td):
    days_in_month = 30.44  # Average number of days in a month over a year
    total_days = td.days + td.seconds / (60 * 60 * 24)  # Convert seconds to days
    total_months = total_days / days_in_month
    return total_months

client = pymongo.MongoClient("mongodb://root:workwork@172.27.135.32:27017/?authSource=admin")
# db_issue = client['ghdb']['issue']
# issueDict = {}
# for repo in settings.repos:
#     issueDict[repo] = 0
# for log in db_issue.find():
#     name = log['index']['repo_name']
#     owner = log['index']['repo_owner']
#     repo = owner + '/' + name
#     if repo in issueDict:
#         issueDict[repo] += 1
# print(issueDict)

dataPath = settings.path + "data/"
for repo in settings.repos:
    alphabet = {}
    owner, name = repo.split('/')
    f = open(dataPath + owner + '-' + name + '_all-Outlier.json')
    data = json.load(f)

    minTime = data[0][0]['time']
    maxTime = data[0][0]['time']
    for issue in data:
        for event in issue:
            if event['time'] < minTime: minTime = event['time']
            if event['time'] > maxTime: maxTime = event['time']
    print(repo)
    time = datetime.strptime(maxTime, '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(minTime, '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
    months = timedelta_to_months(time)
    print(months)
    # break