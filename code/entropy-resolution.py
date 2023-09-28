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

def analysis(data):
    alphabet = {}
    i = 0
    for issue in data:
        for event in issue:
            if event['role'] + event['event'] not in alphabet:
                alphabet[event['role'] + event['event']] = i
                i += 1

    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    for issue in data:
        for i in range(0, len(issue) - 1):
            last = issue[i]['role'] + issue[i]['event']
            present = issue[i + 1]['role'] + issue[i + 1]['event']
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
        time = datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        resolutionTimeList.append(time.days)
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
        for event in issue:
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

def calculateMatrix(issue, alphabet):
    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    for i in range(0, len(issue) - 1):
        last = issue[i]['role'] + issue[i]['event']
        present = issue[i + 1]['role'] + issue[i + 1]['event']
        countMatrix[alphabet[last]][alphabet[present]] += 1
    
    probMatrix = np.zeros((L, L))
    for i in range(L):
        sum = 0
        for j in range(L):
            sum += countMatrix[i][j]
        if sum == 0: continue
        for j in range(L):
            probMatrix[i][j] = countMatrix[i][j] / sum
    return probMatrix.flatten()

resultPath = "/home/sbh/APSEC/result/2023-09-13T16:31Z/"
if not os.path.exists(resultPath):
    os.makedirs(resultPath)

graphPath = settings.path + "graph/"
if not os.path.exists(graphPath):
    os.makedirs(graphPath)

repos = settings.repos
for issueType in settings.issueTypes:
    print('issue type: ' + issueType)
    alphabet = {}
    i = 0
    # for repo in repos:
    #     print(repo)
    #     owner, name = repo.split('/')
    #     f = open(resultPath + owner + '-' + name + '_' +  issueType+ '-with-label.json')
    #     data = json.load(f)
    #     for slice in data:
    #         for line in slice:
    #             issue = line['issue']
    #             for event in issue:
    #                 if event['role'] + event['event'] not in alphabet:
    #                     alphabet[event['role'] + event['event']] = i
    #                     i += 1
        # print(alphabet)

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
    for repo in repos:
        print(repo)
        owner, name = repo.split('/')
        f = open(resultPath + owner + '-' + name + '_' +  issueType+ '-with-label.json')
        data = json.load(f)

        for i, slice in enumerate(data):
            if i == 0: continue
            sum = 0
            totalTime = 0
            for j in range(i):
                tempSlice = data[j]
                tempK = tempSlice[0]['K']
                for k in range(tempK):
                    issues = []
                    for line in tempSlice:
                        label = line['label']
                        if label != k: continue
                        issues.append(line['issue'])
                    # print(len(issues))
                    if len(issues) > 100:
                        for issue in issues:
                            time = datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
                            sum += 1
                            totalTime += time.days
            if sum == 0: continue
            beforeTime = totalTime / sum

            K = slice[0]['K']
            sum = 0
            totalTime = 0
            for k in range(K):
                issues = []
                for line in tempSlice:
                    label = line['label']
                    if label != k: continue
                    issues.append(line['issue'])
                # print(len(issues))
                if len(issues) > 100:
                    for issue in issues:
                        time = datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
                        sum += 1
                        totalTime += time.days
            if sum == 0: continue
            averageTime = totalTime / sum

            for k in range(K):
                issues = []
                for line in slice:
                    label = line['label']
                    if label != k: continue
                    issues.append(line['issue'])
                # print(len(issues))
                if len(issues) > 100:
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
    
    c = {"resolution_time": timeList, "event_number": eventNumList, 
            "issue_length": isssueLenList, "participant_number": parNumList,
            "entropy": entropyList, "project_name": projectList, 'core_issue': cIssueList,
            "normal_issue": nIssueList, "core_assign": cAssignList, "normal_assign": nAssignList,
            "core_label": cLabelList, "normal_label": nLabelList, "core_subscribe": cSubList, "normal_subscribe": nSubLIst,
            "before_average_time": beforeTimeList, "slice_average_time": averageTimeList}
    result = pd.DataFrame(c)
    print(result)
    result.to_csv(resultPath +'mean_1.csv')