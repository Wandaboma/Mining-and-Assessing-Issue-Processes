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

#for graph
# result = []
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

#     leftTime = datetime.strptime('2018-01-01T00:00:00Z', '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#     rightTime = leftTime + relativedelta(months=+settings.windowLength)
    
#     sizeListTime = []
#     sizeListCount = []
#     for i in range(40):
#         print('repo:', repo, 'leftTime: ', leftTime, ' rightTime: ', rightTime)
#         slice = []
#         for issue in data:
#             issueTime = datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#             if (issueTime >= leftTime) and (issueTime < rightTime):
#                 slice.append(issue)

#         print('slice size: ', len(slice))
#         leftTime += relativedelta(months=+settings.stepLength)
#         rightTime = leftTime + relativedelta(months=+settings.windowLength)

#         sizeListTime.append(leftTime.strftime("%Y-%m-%d"))
#         if len(slice) != 0:
#             sizeListCount.append(len(slice))
#         else:
#             sizeListCount.append(np.nan)
#     result.append((repo, sizeListTime, sizeListCount))

# with open(settings.path + 'issue_count.json', 'w') as f:
#     json.dump(result, f)

# f = open(settings.path + 'issue_count.json', 'r')
# data = json.load(f)
# cmap = plt.get_cmap('tab20')
# colors = [cmap(i / len(data)) for i in range(len(data))]
# fig = plt.figure(figsize=(20,15))
# for i, content in enumerate(data):
#     repo, sizeListTime, sizeListCount = content
#     plt.plot(sizeListTime, sizeListCount, label = repo, color = colors[i])
# plt.legend(loc = "best", ncol = 2, fontsize = "15")
# plt.xticks(rotation=90)
# plt.tick_params(axis='x', labelsize = 12)
# plt.savefig(settings.path + '/graph/issue_count.png', dpi = 300)

#for file
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

#     leftTime = datetime.strptime('2016-01-01T00:00:00Z', '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#     rightTime = leftTime + relativedelta(months=+settings.windowLength)
#     while True:
#         print('repo:', repo, 'leftTime: ', leftTime, ' rightTime: ', rightTime)
#         slice = []
#         for issue in data:
#             issueTime = datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#             if (issueTime >= leftTime) and (issueTime < rightTime):
#                 slice.append(issue)
#             if issueTime >= rightTime:
#                 break
#         print('slice size: ', len(slice))
#         leftTime += relativedelta(months=+settings.stepLength)
#         rightTime = leftTime + relativedelta(months=+settings.windowLength)
#         if leftTime > datetime.strptime(data[-1][0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z'):
#             break

#         if len(slice) < 100: continue
#         with open(repoPath + leftTime.strftime("%Y-%m-%d") + '-small.json', 'w') as f:
#             json.dump(slice, f)
    
#         break
#     break

#for issue count
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

    leftTime = datetime.strptime('2020-01-01T00:00:00Z', '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
    # rightTime = datetime.strptime('2021-01-01T00:00:00Z', '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
    count1 = 0
    count2 = 0
    for issue in data:
        issueTime = datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        # if (issueTime >= leftTime) and (issueTime < rightTime):
        #     count1 += 1
        # if issueTime >= rightTime:
        #     count2 += 1
        if issueTime >= leftTime: count1 += 1
    # print('issue after 2018 before 2021:', count1)
    # print('issue after 2021', count2)
    print('issue after 2020:', count1)
