#process data into standard formats
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import settings
import os
import matplotlib.pyplot as plt
import numpy as np

issueType = 'all'
dataPath = settings.path + "data/"

# split issue data into 1 month snapshot
for repo in settings.repos:
    print(repo)
    repo_owner, repo_name = repo.split('/')
    repoPath = dataPath + repo_owner + '-' + repo_name + '/'
    if not os.path.exists(repoPath):
        os.makedirs(repoPath)
    f = open(dataPath + repo_owner + '-' + repo_name + '_' + issueType + '-Outlier.json', 'r')
    data = json.load(f)
    data = sorted(data, key = lambda x : x[0][0]['time'])
    print('total issue num:', len(data))

    leftTime = datetime.strptime('2016-01-01T00:00:00Z', '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
    rightTime = leftTime + relativedelta(months=+settings.windowLength)
    while True:
        print('repo:', repo, 'leftTime: ', leftTime, ' rightTime: ', rightTime)
        slice = []
        for issue in data:
            issueTime = datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
            if (issueTime >= leftTime) and (issueTime < rightTime):
                slice.append(issue)
            if issueTime >= rightTime:
                break
        print('slice size: ', len(slice))
        leftTime += relativedelta(months=+settings.stepLength)
        rightTime = leftTime + relativedelta(months=+settings.windowLength)
        if leftTime > datetime.strptime(data[-1][0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z'):
            break

        if len(slice) < 100: continue
        with open(repoPath + leftTime.strftime("%Y-%m-%d") + '-small.json', 'w') as f:
            json.dump(slice, f)
    
        break
    break

#for issue count
# for repo in settings.repos:
#     print(repo)
#     repo_owner, repo_name = repo.split('/')
#     repoPath = dataPath + repo_owner + '-' + repo_name + '/'
#     if not os.path.exists(repoPath):
#         os.makedirs(repoPath)
#     f = open(dataPath + repo_owner + '-' + repo_name + '_' + issueType + '-Outlier.json', 'r')
#     data = json.load(f)
#     data = sorted(data, key = lambda x : x[0][0]['time'])
#     print('total issue num:', len(data))

#     leftTime = datetime.strptime('2020-01-01T00:00:00Z', '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#     # rightTime = datetime.strptime('2021-01-01T00:00:00Z', '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#     count1 = 0
#     count2 = 0
#     for issue in data:
#         issueTime = datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#         # if (issueTime >= leftTime) and (issueTime < rightTime):
#         #     count1 += 1
#         # if issueTime >= rightTime:
#         #     count2 += 1
#         if issueTime >= leftTime: count1 += 1
#     # print('issue after 2018 before 2021:', count1)
#     # print('issue after 2021', count2)
#     print('issue after 2020:', count1)
