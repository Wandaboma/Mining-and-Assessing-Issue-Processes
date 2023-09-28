#fetch raw data from database
import settings
import pymongo
from pymongo import ASCENDING
import json
import os
dataPath = settings.path + "data/"
if not os.path.exists(dataPath):
    os.makedirs(dataPath)
client = pymongo.MongoClient("mongodb://root:workwork@172.27.135.32:27017/?authSource=admin")
db_label = client['ghdb']['issueLabel']
db_timeline = client['ghdb']['issueTimeline']

# repos = ['tensorflow/tensorflow', 'pytorch/pytorch']
#find bug type issue
issueType = 'all'
for repo in settings.repos:
    print(repo)
    owner, name = repo.split('/')
    result = []
    for issue in db_label.find({'index.repo_owner': owner,'index.repo_name': name}):
        # if issueType in issue['data']['name']:
        #if any event in this issue data doesn't have actor or time, overlook it
            timeLine = []
            flag = True
            for event in db_timeline.find({'index.repo_owner': owner,
                                                     'index.repo_name': name,
                                                     'index.number': issue['index']['number']},
                                                    projection={'data': True, '_id': False},
                                                    sort=[('data.createdAt', ASCENDING)]):
                if 'createdAt' not in event['data']:
                    flag = False
                    break

                if ('actor' not in event['data']) and ('author' not in event['data']):
                   flag = False
                   break
                
                event['id'] = issue['index']['number']
                timeLine.append(event)
            if timeLine == []:
                continue
            if flag:
                result.append(timeLine)
    with open(dataPath + owner + '-' + name + '_' + issueType + '.json', 'w') as f:
        json.dump(result, f)