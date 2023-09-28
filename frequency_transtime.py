from ossaudiodev import control_labels
from urllib import request
import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import numpy as np
resultPath = "/home/sbh/APSEC/result/2023-09-13T16:31Z/"
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
    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    transTimeMatrix = np.zeros((L, L))
    cnt = 0
    for repo in repos:
        print(repo)
        owner, name = repo.split('/')
        f = open(resultPath + owner + '-' + name + '_' +  issueType+ '-with-label.json')
        data = json.load(f)

        for slice in data:
            for record in slice:
                issue = record['issue']
                # print(issue)
                # break
                for i in range(0, len(issue) - 1):
                    cnt += 1
                    last = issue[i]['role'] + issue[i]['event']
                    present = issue[i + 1]['role'] + issue[i + 1]['event']
                    countMatrix[alphabet[last]][alphabet[present]] += 1
                    time = datetime.strptime(issue[i + 1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[i]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
                    transTimeMatrix[alphabet[last]][alphabet[present]] += time.days
            # break
            
    probMatrix = np.zeros((L, L))
    timeList = []
    cntList = []
    for i in range(L):
        sum = 0
        t = 0
        for j in range(L):
            sum += countMatrix[i][j]
            t += transTimeMatrix[i][j]
        if sum == 0: 
            timeList.append(0)
        else:
            timeList.append(t / sum)
        cntList.append(sum)

    result = []
    for key, num in alphabet.items():
        result.append([key, timeList[num], cntList[num]/cnt])
    
    result.sort(key=lambda x: (x[2]), reverse=True)
    print(result)