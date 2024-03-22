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

def analysis(data):
    alphabet = {}
    i = 0
    for issue in data:
        for group in issue:
            for event in group:
                if event['role'] + event['event'] not in alphabet:
                    alphabet[event['role'] + event['event']] = i
                    i += 1

    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    for issue in data:
        for i in range(0, len(issue) - 1):
            for eventLast in issue[i]:
                for eventNext in issue[i + 1]:
                    last = eventLast['role'] + eventLast['event']
                    present = eventNext['role'] + eventNext['event']
                    countMatrix[alphabet[last]][alphabet[present]] += 1
    
    probMatrix = np.zeros((L, L))
    total = 0
    entropy = 0
    sumList = []
    for i in range(L):
        sum = 0
        for j in range(L):
            sum += countMatrix[i][j]
        sumList.append(sum)
        if sum == 0: continue
        total += sum
        for j in range(L):
            probMatrix[i][j] = countMatrix[i][j] / sum
        
    for i in range(L):
        e = 0
        for j in range(L):
            if probMatrix[i][j] != 0:
                e -= probMatrix[i][j] * math.log(probMatrix[i][j])
        entropy += sumList[i] / total * e
    return entropy

def efficiency(data):
    resolutionTimeList = []
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
        # time = datetime.strptime(issue[-1][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        # resolutionTimeList.append(time.days)
        resolutionTimeList.append(issueTimeCount(issue))
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

    return statistics.mean(resolutionTimeList), statistics.mean(eventNumberList), statistics.mean(issueLengthList), statistics.mean(participantNumList), statistics.mean(coreIssueCommentList), statistics.mean(normalIssueCommentList), statistics.mean(coreAssignList), statistics.mean(normalAssignList), statistics.mean(coreLabelList),statistics.mean(normalLabelList),statistics.mean(coreSubscribeList),statistics.mean(normalSubscribeList)

def averageTotalTime(data):
    totalTime = 0
    sum = 0
    for issue in data:
        time = issueTimeCount(issue)
        # time = datetime.strptime(issue[-1][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        # time.days
        sum += 1
        totalTime += time
    if sum == 0: return 0
    else: return totalTime / sum

# resultPath = "/home/sbh/APSEC/result/"
# path = input("input data path:")
# resultPath += path + '/'
resultPath = '/home/sbh/APSEC/result/2024-03-21T16:30Z/'
with open(resultPath + 'comparison- 0.5.json') as f:
    comparisons = json.load(f)

entropyList = []
timeList = []
eventNumList = []
isssueLenList = []
parNumList = []
projectList = []
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
sliceTimeList = []
clusterSizeList = []
comparisons = sorted(comparisons, key = lambda x: (x[0], x[1]))
for repo in settings.repos:
    beforeIssues = []
    for com in comparisons:
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
        for p in range(k):
            sum = 0
            totalTime = 0
            issues = []
            for i, issue in enumerate(data):
                if labels[i] != p: continue
                issues.append(issue)          
            
            if beforeIssues != []:
                entropy = analysis(issues)
                time, eventNum, issueLen, parNum, cIssue, nIssue, cAssign, nAssign, cLabel, nLabel, cSub, nSub = efficiency(issues)
                entropyList.append(entropy)
                timeList.append(time)
                eventNumList.append(eventNum)
                isssueLenList.append(issueLen)
                parNumList.append(parNum)
                projectList.append(repo)
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
                sliceTimeList.append(filename.strip('-small.json'))
                clusterSizeList.append(len(issues))
        beforeIssues += data
    # break

c = {"resolution_time": timeList, "event_number": eventNumList, 
        "issue_length": isssueLenList, "participant_number": parNumList,
        "entropy": entropyList, "project_name": projectList, 'core_issue': cIssueList,
        "normal_issue": nIssueList, "core_assign": cAssignList, "normal_assign": nAssignList,
        "core_label": cLabelList, "normal_label": nLabelList, "core_subscribe": cSubList, "normal_subscribe": nSubLIst,
        "before_average_time": beforeTimeList, "slice_average_time": averageTimeList, "slice_time": sliceTimeList,
        "cluster_size": clusterSizeList}
result = pd.DataFrame(c)
print(result)
result.to_csv(resultPath +'mean.csv')
