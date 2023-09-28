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

def analysis(data, alphabet):
    # alphabet = {}
    # i = 0
    # for issue in data:
    #     for event in issue:
    #         if event['role'] + event['event'] not in alphabet:
    #             alphabet[event['role'] + event['event']] = i
    #             i += 1

    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    transTimeMatrix = np.zeros((L, L))
    for issue in data:
        for i in range(0, len(issue) - 1):
            last = issue[i]['role'] + issue[i]['event']
            present = issue[i + 1]['role'] + issue[i + 1]['event']
            countMatrix[alphabet[last]][alphabet[present]] += 1
            time = datetime.strptime(issue[i + 1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[i]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
            transTimeMatrix[alphabet[last]][alphabet[present]] += time.days
    
    probMatrix = np.zeros((L, L))
    total = 0
    entropy = 0
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
        entropy += sumList[i] / total * e
    # return entropy
    return entropyList, timeList

# def efficiency(data):
#     resolutionTimeList = []
#     eventNumberList = []
#     issueLengthList = []
#     participantNumList = []

#     for issue in data:
#         time = datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
#         resolutionTimeList.append(time.days)
#         eventDict = {}
#         participantDict = {}
#         for event in issue:
#             if event['role'] + event['event'] not in eventDict:
#                 eventDict[event['role'] + event['event']] = 1
#             if event['actor'] not in participantDict:
#                 participantDict[event['actor']] = 1
#         eventNumberList.append(len(eventDict))
#         issueLengthList.append(len(issue))
#         participantNumList.append(len(participantDict))

#     return statistics.mean(resolutionTimeList), statistics.mean(eventNumberList), statistics.mean(issueLengthList), statistics.mean(participantNumList)

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
    for repo in repos:
        print(repo)
        owner, name = repo.split('/')
        f = open(resultPath + owner + '-' + name + '_' +  issueType+ '-with-label.json')
        data = json.load(f)
        for slice in data:
            for line in slice:
                issue = line['issue']
                for event in issue:
                    if event['role'] + event['event'] not in alphabet:
                        alphabet[event['role'] + event['event']] = i
                        i += 1
    print(alphabet)
    # break

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
    for repo in repos:
        print(repo)
        owner, name = repo.split('/')
        f = open(resultPath + owner + '-' + name + '_' +  issueType+ '-with-label.json')
        data = json.load(f)

        sum = 0
        totalTime = 0
        beforeTransTimeSum = []
        for p in range(len(alphabet)):
            beforeTransTimeSum.append(0)
        print(len(data))
        for i, slice in enumerate(data):
            if i == 0: continue
            # if i > 5: break
            print(i)
            tempSlice = data[i - 1]
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
                        entropy, transTime = analysis(issues, alphabet)
                        for p in range(len(alphabet)):
                            beforeTransTimeSum[p] += transTime[p]
            if sum == 0: continue
            beforeTime = totalTime / sum
            beforeTransTimeList = []
            for p in range(len(alphabet)):
                beforeTransTimeList.append(beforeTransTimeSum[p] / sum)

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
        
            K = slice[0]['K']
            for k in range(K):
                issues = []
                for line in slice:
                    label = line['label']
                    if label != k: continue
                    issues.append(line['issue'])

                if len(issues) > 100:
                    entropy, transTime = analysis(issues, alphabet)
                    # time, eventNum, issueLen, parNum = efficiency(issues)
                    time, eventNum, issueLen, parNum, cIssue, nIssue, cAssign, nAssign, cLabel, nLabel, cSub, nSub = efficiency(issues)
                    for key, num in alphabet.items(): 
                        if transTime[num] == 0:
                            continue
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
    
    c = {"transition_time": timeList, "event_number": eventNumList, 
            "issue_length": isssueLenList, "participant_number": parNumList,
            "entropy": entropyList, "project_name": projectList, "event_name": eventList,
            'core_issue': cIssueList,
            "normal_issue": nIssueList, "core_assign": cAssignList, "normal_assign": nAssignList,
            "core_label": cLabelList, "normal_label": nLabelList, "core_subscribe": cSubList, "normal_subscribe": nSubLIst,
            "before_average_time": beforeTimeList, "slice_average_time": averageTimeList, "before_trans_time": beforeAverageTransTimeList}
    result = pd.DataFrame(c)
    result.to_csv(resultPath +'mean_detailed_with_before_transtime.csv')
    # for key, num in alphabet.items():
    #     print('processing..' + key)
    #     plt.figure(dpi = 300, figsize=(10, 7))
    #     plt.title(key)
    #     plt.xlabel("entropy")
    #     plt.ylabel("average issue resolution time (days)")
    #     for repo in repos:
    #         entropyList = []
    #         timeList = []
    #         for id, cluster in result.iterrows():
    #             # print(cluster)
    #             if cluster['event_name'] == key and cluster['project_name'] == repo:
    #                 entropyList.append(cluster['entropy'])
    #                 timeList.append(cluster['transition_time'])
    #         plt.scatter(entropyList, timeList, s = 1, label = repo)
    #     plt.legend(fontsize = 5)
    #     plt.savefig(graphPath + key)
    #     plt.close()



