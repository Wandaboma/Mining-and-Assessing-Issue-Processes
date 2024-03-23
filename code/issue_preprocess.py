#process data into standard formats
import json
from pymongo import MongoClient
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import settings
import os
import statistics

dataPath = settings.path + "data/"
if not os.path.exists(dataPath):
    os.makedirs(dataPath)

bot_re_list = [re.compile(".*\[[Bb][Oo][Tt]\].*"),
               re.compile(".*-[Bb][Oo][Tt][^A-Za-z]*.*"),
               re.compile(".*[\W0-9_][Bb][Oo][Tt]$"),
               re.compile("^[Bb][Oo][Tt][\W0-9_].*"),
               re.compile(".*[\W0-9_][Bb][Oo][Tt][\W0-9_].*")]

bot_list = ['google-ml-butler', 'github-actions']
def __is_bot(login):
    '''
        helper function, return true if login is bot
    '''
    for botre in bot_re_list:
        if re.match(botre, login):
            return True
    for specialName in bot_list:
        if specialName == login:
            return True
    return False

# repos = ['angular/angular', 'tensorflow/tensorflow', 'microsoft/vscode']
# repos = ['tensorflow/tensorflow', 'pytorch/pytorch']
issueType = 'all'
for repo in settings.repos:
    print(repo)
    repo_owner, repo_name = repo.split('/')
    f = open(dataPath + repo_owner + '-' + repo_name + '_' + issueType + '.json', 'r')
    data = json.load(f)
    print('total issue num:', len(data))

    #only keep time, actor, event information
    result = []
    for issue in data:
        resultIssue = []
        for event in issue:
            if 'actor' in event['data']:
                name = event['data']['actor']['login']
            else:
                name = event['data']['author']['login']
            time = event['data']['createdAt']
            eventType = event['data']['__typename']
            newEvent = {'actor': name, 'time': time, 'event': eventType, 'id': event['id']}
            resultIssue.append(newEvent)
        result.append(resultIssue)
    data = result

    # remove issue with unusual length and unsual resolution time
    issueLengthList = []
    resolutionTimeList = []
    for issue in data:
        issueLengthList.append(len(issue))
        issuetime = datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        resolutionTimeList.append(issuetime.days)
    quantiles = statistics.quantiles(issueLengthList, n=4, method='inclusive')
    Q1 = quantiles[0]
    Q3 = quantiles[2]
    upper = Q3 + 1.5 * (Q3 - Q1)
    lower = Q1 - 1.5 * (Q3 - Q1)
    print('issue length bound: ', upper, '   ', lower)
    result = []
    for issue in data:
        if len(issue) > upper or len(issue) < lower:
            continue
        result.append(issue)
    data = result

    quantiles = statistics.quantiles(resolutionTimeList, n=4, method='inclusive')
    Q1 = quantiles[0]
    Q3 = quantiles[2]
    upper = Q3 + 1.5 * (Q3 - Q1)
    lower = Q1 - 1.5 * (Q3 - Q1)
    print('issue resolution time bound: ', upper, '   ', lower)
    result = []
    for issue in data:
        issuetime = (datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')).days
        if issuetime > upper or issuetime < lower:
            continue
        result.append(issue)
    data = result
    print('issue num without:', len(data))

    #merge same event
    mergeCaseDict = {'AssignedEvent': 'AssignedEvent', 'UnassignedEvent': 'AssignedEvent',
                     'LabeledEvent': 'LabeledEvent', 'UnlabeledEvent': 'LabeledEvent',
                     'MilestonedEvent': 'MilestonedEvent', 'DemilestonedEvent': 'MilestonedEvent',
                     'LockedEvent': 'LockedEvent', 'UnlockedEvent': 'LockedEvent',
                     'MarkedAsDuplicateEvent': 'MarkedAsDuplicateEvent',
                     'UnmarkedAsDuplicateEvent': 'MarkedAsDuplicateEvent',
                     'PinnedEvent': 'PinnedEvent', 'UnpinnedEvent': 'PinnedEvent',
                     'SubscribedEvent': 'SubscribedEvent', 'UnsubscribedEvent': 'SubscribedEvent',
                     'MentionedEvent': 'SubscribedEvent',
                     'ConnectedEvent': 'ConnectedEvent', 'DisconnectedEvent': 'ConnectedEvent'}
    for issue in data:
        for event in issue:
            if event['event'] in mergeCaseDict:
                event['event'] = mergeCaseDict[event['event']]
   
    #get role
    CONNECTION_STRING = "**"
    client = MongoClient(CONNECTION_STRING)
    _db = client['ghdb']
    issueCollection = _db['issue']
    issueCreator = {}
    for issue in data:
        # print(issue)
        num = issue[0]['id']
        for result in issueCollection.find({'index.repo_owner': repo_owner, 'index.repo_name': repo_name, 'index.number': num}):
            if 'author' in result['data']['repository']['issue']:
                name = result['data']['repository']['issue']['author']['login']
                issueCreator[result['index']['number']] = name


    writeAccess = {'LabeledEvent', 'ClosedEvent', 'ReopenedEvent', 'AssignedEvent', 'MilestonedEvent',
                   'MarkedAsDuplicateEvent', 'TransferredEvent', 'LockedEvent'}
    nameDict = {}
    for issue in data:
        for event in issue:
            eventType = event['event']
            name = event['actor']
            if eventType in writeAccess:
                if eventType == 'ClosedEvent' or eventType == 'LabeledEvent':
                    flag = False
                    if event['id'] not in issueCreator:
                        flag = False
                    elif issueCreator[event['id']] == name:
                        flag = True
                    if flag == False:
                        nameDict[name] = 1
                else:
                    nameDict[name] = 1

    print('elite people number: ' + str(len(nameDict)))
    eliteTimetable = {}
    nameList = list(nameDict.keys())
    for i in range(len(nameDict)):
        name = nameList[i]
        timeList = []
        for issue in data:
            for event in issue:
                if event['actor'] != name: continue
                eventType = event['event']
                if eventType in writeAccess:
                    if eventType == 'ClosedEvent' or eventType == 'LabeledEvent':
                        flag = False
                        if event['id'] not in issueCreator:
                            flag = False
                        elif issueCreator[event['id']] == name:
                            flag = True
                        if flag == False:
                            timeList.append(event['time'])
                    else:
                        timeList.append(event['time'])
        timeList = list(set(timeList))
        timeList.sort()
        #merge time slots so it can be quicker
        mergedTimeList = []
        leftTime = datetime.strptime(timeList[0], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        rightTime = leftTime + relativedelta(months=+3)
        for i in range(1, len(timeList)):
            nowTime = datetime.strptime(timeList[i], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
            if (leftTime <= nowTime) and (nowTime <= rightTime):
                rightTime = nowTime + relativedelta(months=+3)
            elif nowTime > rightTime:
                mergedTimeList.append((leftTime, rightTime))
                leftTime = nowTime
                rightTime = leftTime + relativedelta(months=+3)
        mergedTimeList.append((leftTime, rightTime))
        eliteTimetable[name] = mergedTimeList

    print('start to classify roles')
    for issue in data:
        for event in issue:
            name = event['actor']
            event['role'] = 'Normal'
            if name in eliteTimetable:
                flag = False
                eventTime = datetime.strptime(event['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
                for leftTime, rightTime in eliteTimetable[name]:
                    # leftTime = datetime.strptime(time, '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
                    # rightTime = leftTime + relativedelta(months=+3)
                    if (leftTime <= eventTime) and (eventTime <= rightTime):
                        flag = True
                        break
                    elif eventTime < leftTime:
                        break
                if flag:
                    event['role'] = 'Core'
            if __is_bot(name):
                event['role'] = 'Bot'
    
    # rule out issue doesn't satisfy the requirement
    print('rule out too short issues')
    result = []
    for issue in data:
        if len(issue) < 3: continue
        botDict = {}
        humanDict = {}
        for event in issue:
            if event['role'] == 'Bot':
                botDict[event['actor']] = 1
            else:
                humanDict[event['actor']] = 1
        if len(humanDict) < 2: continue
        result.append(issue)
    data = result

    # data = [[{'actor': 'alan-agius4', 'time': '2022-02-12T19:18:37Z', 'event': 'IssueComment'}, 
    #          {'actor': 'alan-agius4', 'time': '2022-02-12T19:18:37Z', 'event': 'MilestonedEvent'},
    #            {'actor': 'alan-agius4', 'time': '2022-02-12T19:18:37Z', 'event': 'LabeledEvent'}, 
    #            {'actor': 'alan-agius4', 'time': '2022-02-12T19:16:37Z', 'event': 'IssueComment'}]]
    #sort parallel event，reorganize the data
    result = []
    for issue in data:
        i = 0
        L = len(issue)
        timeLine = []
        while i < L:
            time = issue[i]['time']
            name = issue[i]['actor']
            group = []
            group.append(issue[i])
            j = i + 1
            while j < L:
                nowTime = issue[j]['time']
                nowName = issue[j]['actor']
                if (nowTime == time) and (nowName == name):
                    group.append(issue[j])
                    j = j + 1
                else:
                    break
            timeLine.append(group)
            i = j
        result.append(timeLine)   
    data = result

    with open(dataPath + repo_owner + '-' + repo_name + '_' + issueType + '-Outlier.json', 'w') as f:
        json.dump(data, f)


