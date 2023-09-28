import json
import numpy as np
import matplotlib.pyplot as plt

def getID(name, coreDict, activityDict):
    if name in coreDict:
        return coreDict[name]
    if name in activityDict:
        return 10
    return 11

repos = ['angular/angular', 'tensorflow/tensorflow', 'microsoft/vscode']
issueType = 'bug'
for repo in repos:
    owner, name = repo.split('/')
    f = open('D:/ASE/data/' + owner + '-' + name + '_' + issueType + '.json')
    issues = json.load(f)
    nameDict = {}
    for issue in issues:
        for event in issue:
            user = ''
            if 'actor' in event['data']:
                user = event['data']['actor']['login']
            elif 'author' in event['data']:
                user = event['data']['author']['login']
            if user in nameDict:
                nameDict[user] += 1
            else: nameDict[user] = 1

#''' count on people '''
    nameList = sorted(nameDict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    coreName = nameList[:10]
    coreDict = {}
    i = 0
    for name, num in coreName:
        coreDict[name] = i
        i += 1
    activityName = nameList[10: int(len(nameList) * 0.1)]
    activityDict = {}
    i = 0
    for name, num in activityName:
        activityDict[name] = i
        i += 1
    # print(coreDict)
    # print(activityDict)
    
    roleMatrix = np.zeros((12, 12))
    for issue in issues:
        for i in range(len(issue) - 1):
            lastUser = ''
            presentUser = ''
            if 'author' in issue[i]['data']:
                lastUser = issue[i]['data']['author']['login']
            if 'author' in issue[i + 1]['data']:
                presentUser = issue[i + 1]['data']['author']['login']
            lastID = getID(lastUser, coreDict, activityDict)
            presentID = getID(presentUser, coreDict, activityDict)
            roleMatrix[lastID][presentID] += 1
    
    fig, ax = plt.subplots()
    im = ax.imshow(roleMatrix)
    
    labels = []
    for name in coreDict:
        labels.append(name)
    labels.append('active')
    labels.append('normal')
    ax.set_xticks(np.arange(len(labels)), labels = labels)
    ax.set_yticks(np.arange(len(labels)), labels = labels)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, roleMatrix[i, j], ha = 'center', va = 'center', color = 'w')
    ax.set_title(repo + '-bug')
    # plt.savefig('D:/ASE/plot/' + owner + '-' + name + '-bug.png')
    plt.show()

#'''count on event '''
    # eventDict = {}
    # for issue in issues:
    #     for event in issue:
    #         eventType = event['data']['__typename']
    #         if eventType in eventDict:
    #             eventDict[eventType] += 1
    #         else:
    #             eventDict[eventType] = 1
    # typeList = sorted(eventDict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    # coreEvent = typeList[:10]
    # eventDict = {}
    # i = 0
    # for event, num in coreEvent:
    #     eventDict[event] = i
    #     i += 1
    # eventMatrix = np.zeros((11, 11))
    # for issue in issues:
    #     for i in range(len(issue) - 1):
    #         lastEvent = issue[i]['data']['__typename']
    #         presentEvent = issue[i + 1]['data']['__typename']
    #         if lastEvent in eventDict:
    #             lastID = eventDict[lastEvent]
    #         else: lastID = 10
    #         if presentEvent in eventDict:
    #             presentID = eventDict[presentEvent]
    #         else: presentID = 10
    #         eventMatrix[lastID][presentID] += 1

    # fig, ax = plt.subplots()
    # im = ax.imshow(eventMatrix)
    
    # labels = []
    # for name in eventDict:
    #     labels.append(name)
    # labels.append('others')
    # ax.set_xticks(np.arange(len(labels)), labels = labels)
    # ax.set_yticks(np.arange(len(labels)), labels = labels)
    # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
    #      rotation_mode="anchor")
    # for i in range(len(labels)):
    #     for j in range(len(labels)):
    #         text = ax.text(j, i, eventMatrix[i, j], ha = 'center', va = 'center', color = 'w')
    # ax.set_title(repo + '-bug')
    # # plt.savefig('D:/ASE/plot/' + owner + '-' + name + '-bug.png')
    # plt.show()

# '''see what event distribution have on different roles'''
    # eventCount = {}
    # for issue in issues:
    #     for event in issue:
    #         eventType = event['data']['__typename']
    #         user = ''
    #         if 'actor' in event['data']:
    #             user = event['data']['actor']['login']
    #         elif 'author' in event['data']:
    #             user = event['data']['author']['login']
    #         # print(eventType)
    #         if user not in activityDict and user not in coreDict:
    #             if eventType in eventCount:
    #                 eventCount[eventType] += 1
    #             else: eventCount[eventType] = 1
    # print(eventCount)
    # countList = sorted(eventCount.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    # print(countList)
    # labels = []
    # sizes = []
    # i = 0
    # for key, value in countList:
    #     labels.append(key)
    #     sizes.append(value)
    #     i += 1
    #     if i > 10: break
    # plt.pie(sizes, labels=labels)
    # plt.show()
