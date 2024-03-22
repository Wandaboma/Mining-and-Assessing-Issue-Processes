import matplotlib.pyplot as plt
import settings
import numpy as np
import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import statistics
from sklearn.cluster import KMeans
import scipy.stats as stats
import csv
import pandas as pd

# 2024-02-27T22:40Z
def analysis(data, alphabet):
    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    transTimeMatrix = np.zeros((L, L))
    for issue in data:
        for i in range(0, len(issue) - 1):
            for eventLast in issue[i]:
                for eventNext in issue[i + 1]:
                    last = eventLast['role'] + eventLast['event']
                    present = eventNext['role'] + eventNext['event']
                    countMatrix[alphabet[last]][alphabet[present]] += 1
                    time = datetime.strptime(eventNext['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(eventLast['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
                    transTimeMatrix[alphabet[last]][alphabet[present]] += time.days
    
    probMatrix = np.zeros((L, L))
    total = 0
    sumList = []
    timeList = []
    for i in range(L):
        sum = 0
        t = 0
        for j in range(L):
            sum += countMatrix[i][j]
            t += transTimeMatrix[i][j]
        sumList.append(sum)
        if sum == 0: 
            timeList.append(0)
            continue
        else:
            timeList.append(t / sum)
        total += sum
        for j in range(L):
            probMatrix[i][j] = countMatrix[i][j] / sum
    
    entropyList = []
    for i in range(L):
        e = 0
        for j in range(L):
            if probMatrix[i][j] != 0:
                e -= probMatrix[i][j] * math.log(probMatrix[i][j])
        entropyList.append(e)
    # return entropy
    return entropyList, timeList

def issueTimeCount(issue):
    time = datetime.strptime(issue[-1][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
    day = time.days
    for i in range(len(issue) - 1):
        flagA = False
        flagB = False
        for event in issue[i]:
            if 'Close' in event['event']:
                flagA = True
        for event in issue[i + 1]:
            if 'Reopen' in event['event']:
                flagB = True
        if flagA and flagB:
            time = datetime.strptime(issue[i + 1][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[i][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
            day -= time.days
    return day

def averageTotalTime(data):
    totalTime = 0
    sum = 0
    for issue in data:
        time = issueTimeCount(issue)
        sum += 1
        totalTime += time
    if sum == 0: return 0
    else: return totalTime / sum

def efficiency(data):
    eventNumberList = []
    issueLengthList = []
    participantNumList = []
    coreIssueCommentList = []
    normalIssueCommentList = []
    coreAssignList = []
    normalAssignList = []
    coreLabelList = []
    normalLabelList = []
    coreSubscribeList = []
    normalSubscribeList = []

    for issue in data:
        eventDict = {}
        participantDict = {}
        coreIssue = 0
        normalIssue = 0
        coreAssign = 0
        normalAssign = 0
        coreLabel = 0
        normalLabel  = 0
        coreSubscribe = 0
        normalSubscribe = 0
        for group in issue:
            for event in group:
                if event['role'] + event['event'] not in eventDict:
                    eventDict[event['role'] + event['event']] = 1
                if event['actor'] not in participantDict:
                    participantDict[event['actor']] = 1
                if event['event'] == 'IssueComment':
                    if event['role'] == 'Core':
                        coreIssue += 1
                    if event['role'] == 'Normal':
                        normalIssue += 1
                if event['event'] == 'AssignedEvent':
                    if event['role'] == 'Core':
                        coreAssign += 1
                    if event['role'] == 'Normal':
                        normalAssign += 1
                if event['event'] == 'LabeledEvent':
                    if event['role'] == 'Core':
                        coreLabel += 1
                    if event['role'] == 'Normal':
                        normalLabel += 1
                if event['event'] == 'SubscribedEvent':
                    if event['role'] == 'Core':
                        coreSubscribe += 1
                    if event['role'] == 'Normal':
                        normalSubscribe += 1
        eventNumberList.append(len(eventDict))
        issueLengthList.append(len(issue))
        participantNumList.append(len(participantDict))
        coreIssueCommentList.append(coreIssue)
        normalIssueCommentList.append(normalIssue)
        coreAssignList.append(coreAssign)
        normalAssignList.append(normalAssign)
        coreLabelList.append(coreLabel)
        normalLabelList.append(normalLabel)
        coreSubscribeList.append(coreSubscribe)
        normalSubscribeList.append(normalAssign)

    return statistics.mean(eventNumberList), statistics.mean(issueLengthList), statistics.mean(participantNumList), statistics.mean(coreIssueCommentList), statistics.mean(normalIssueCommentList), statistics.mean(coreAssignList), statistics.mean(normalAssignList), statistics.mean(coreLabelList),statistics.mean(normalLabelList),statistics.mean(coreSubscribeList),statistics.mean(normalSubscribeList)

dataPath = settings.path + "data/"
resultPath = "/home/sbh/APSEC/result/"
# path = input("input data path:")
# resultPath += path + '/'


# alphabet = {}
# i = 0
# for repo in settings.repos:
#     print(repo)
#     owner, name = repo.split('/')
#     repoPath = dataPath + owner + '-' + name + '/'
#     filenames = os.listdir(repoPath)
#     for filename in filenames:
#         f = open(repoPath + filename)
#         data = json.load(f)
#         for issue in data:
#             for group in issue:
#                 for event in group:
#                     if event['role'] + event['event'] not in alphabet:
#                         alphabet[event['role'] + event['event']] = i
#                         i += 1
# print(alphabet)
# break
alphabet = {'CoreAssignedEvent': 0, 'CoreLabeledEvent': 1, 'NormalRenamedTitleEvent': 2, 'CoreIssueComment': 3, 'CoreClosedEvent': 4, 'CoreLockedEvent': 5, 'CoreCrossReferencedEvent': 6, 'NormalIssueComment': 7, 'CoreSubscribedEvent': 8, 'NormalSubscribedEvent': 9, 'NormalCrossReferencedEvent': 10, 'CoreMilestonedEvent': 11, 'NormalClosedEvent': 12, 'CoreRenamedTitleEvent': 13, 'CoreReferencedEvent': 14, 'CoreReopenedEvent': 15, 'CoreMarkedAsDuplicateEvent': 16, 'NormalReferencedEvent': 17, 'CoreCommentDeletedEvent': 18, 'BotLockedEvent': 19, 'BotLabeledEvent': 20, 'BotIssueComment': 21, 'BotMilestonedEvent': 22, 'BotClosedEvent': 23, 'BotAssignedEvent': 24, 'CoreConnectedEvent': 25, 'CoreTransferredEvent': 26, 'BotReferencedEvent': 27, 'BotCrossReferencedEvent': 28, 'BotSubscribedEvent': 29, 'CoreAddedToProjectEvent': 30, 'CoreMovedColumnsInProjectEvent': 31, 'CorePinnedEvent': 32, 'NormalLabeledEvent': 33, 'CoreRemovedFromProjectEvent': 34, 'CoreConvertedNoteToIssueEvent': 35, 'BotRenamedTitleEvent': 36, 'NormalConnectedEvent': 37, 'NormalMovedColumnsInProjectEvent': 38, 'BotReopenedEvent': 39, 'NormalAddedToProjectEvent': 40, 'NormalCommentDeletedEvent': 41, 'NormalPinnedEvent': 42, 'BotMovedColumnsInProjectEvent': 43, 'BotAddedToProjectEvent': 44, 'CoreConvertedToDiscussionEvent': 45, 'NormalRemovedFromProjectEvent': 46, 'BotRemovedFromProjectEvent': 47, 'NormalConvertedNoteToIssueEvent': 48}


entropyList = []
timeList = []
eventNumList = []
isssueLenList = []
parNumList = []
projectList = []
eventList = []
cIssueList = []
nIssueList = []
cAssignList = []
nAssignList = []
cLabelList = []
nLabelList = []
cSubList = []
nSubLIst = []
beforeTimeList = []
averageTimeList = []
beforeAverageTransTimeList = []
sliceTimeList = []
clusterSizeList = []
resultPath = '/home/sbh/APSEC/result/2024-03-21T16:30Z/'
with open(resultPath + 'comparison- 0.5.json') as f:
    comparisons = json.load(f)
comparisons = sorted(comparisons, key = lambda x: (x[0], x[1]))
for repo in settings.repos:
    # print(repo)
    beforeTransTimeSum = []
    transCnt = 0
    for p in range(len(alphabet)):
        beforeTransTimeSum.append(0)
    
    beforeIssues = []
    count = 0
    for com in comparisons:
        count += 1
        if com[0] != repo: continue
        filename = com[1]
        if filename < '2020-01-01-small.json': continue
        k = com[4]
        print(repo, filename, k)
        owner, name = repo.split('/')
        repoPath = resultPath + owner + '-' + name + '/'

        with open(repoPath + filename) as f:
            labels = json.load(f)

        dataPath = settings.path + "data/" + owner + '-' + name + '/'
        with open(dataPath + filename) as f:
            data = json.load(f)
        
        #for each cluster, give count result
        beforeTime = averageTotalTime(beforeIssues)
        averageTime = averageTotalTime(data)
        tempEntropy, beforeTransTimeList = analysis(beforeIssues, alphabet) 
        for p in range(k):
            sum = 0
            totalTime = 0
            issues = []
            for i, issue in enumerate(data):
                if labels[i] != p: continue
                issues.append(issue)          
            
            if beforeIssues != []:
                eventNum, issueLen, parNum, cIssue, nIssue, cAssign, nAssign, cLabel, nLabel, cSub, nSub = efficiency(issues)
                entropy, transTime = analysis(issues, alphabet)
                for key, num in alphabet.items(): 
                    if entropy[num] == 0: continue
                    entropyList.append(entropy[num])
                    timeList.append(transTime[num])
                    eventNumList.append(eventNum)
                    isssueLenList.append(issueLen)
                    parNumList.append(parNum)
                    projectList.append(repo)
                    eventList.append(key)
                    cIssueList.append(cIssue)
                    nIssueList.append(nIssue)
                    cAssignList.append(cAssign)
                    nAssignList.append(nAssign)
                    cLabelList.append(cLabel)
                    nLabelList.append(nLabel)
                    cSubList.append(cSub)
                    nSubLIst.append(nSub)
                    beforeTimeList.append(beforeTime)
                    averageTimeList.append(averageTime)
                    beforeAverageTransTimeList.append(beforeTransTimeList[num])
                    sliceTimeList.append(filename.strip('-small.json'))
                    clusterSizeList.append(len(issues))
        beforeIssues += data
    #     if count > 3: break
    # break

c = {"transition_time": timeList, "event_number": eventNumList, 
        "issue_length": isssueLenList, "participant_number": parNumList,
        "entropy": entropyList, "project_name": projectList, "event_name": eventList,
        'core_issue': cIssueList, "normal_issue": nIssueList, "core_assign": cAssignList, "normal_assign": nAssignList,
        "core_label": cLabelList, "normal_label": nLabelList, "core_subscribe": cSubList, "normal_subscribe": nSubLIst,
        "before_average_time": beforeTimeList, "slice_average_time": averageTimeList, "before_trans_time": beforeAverageTransTimeList,
        "slice_time": sliceTimeList, "cluster_size": clusterSizeList}
result = pd.DataFrame(c)
print(result)
result.to_csv(resultPath +'mean_detailed_2020.csv')



