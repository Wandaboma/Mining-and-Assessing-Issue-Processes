import json
from sre_constants import _NamedIntConstant
import numpy as np
import math
import settings
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import random
from scipy.spatial.distance import cdist
from datetime import datetime
import statistics
import scipy.stats as stats

def analysis(data, cluster):
    alphabet = {}
    i = 0
    for issue in data:
        for event in issue:
            if event['role'] + event['event'] not in alphabet:
                alphabet[event['role'] + event['event']] = i
                i += 1

    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    timeMatrix = np.zeros((L, L))
    for issue in data:
        for i in range(0, len(issue) - 1):
            last = issue[i]['role'] + issue[i]['event']
            present = issue[i + 1]['role'] + issue[i + 1]['event']
            time = datetime.strptime(issue[i + 1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[i]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
            countMatrix[alphabet[last]][alphabet[present]] += 1
            timeMatrix[alphabet[last]][alphabet[present]] += time.days
    
    timeList = []
    for i in range(L):
        s = 0
        count = 0
        for j in range(L):
            s += timeMatrix[i][j]
            count += countMatrix[i][j]
        if count == 0: timeList.append(0)
        else: timeList.append(s / count)

    probMatrix = np.zeros((L, L))
    total = 0
    entropy = 0
    sumList = []
    x = []
    entropyList = []
    for i in range(L):
        sum = 0
        x.append(i)
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
                e -= probMatrix[i][j] * math.log2(probMatrix[i][j])
        entropyList.append(e * 10)
        # with weight
        # entropy += sumList[i] / total * e
        # without weight
        entropy += e
    # r,p = stats.pearsonr(entropyList, timeList) 
    # print('r = %6.3f p = %6.3f'%(r,p))
    # print(cluster, ':', entropy)

    eList = []
    # for issue in data:
        # # print(type(datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')))
        # delta = datetime.strptime(issue[-1]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z') - datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        # eList.append(delta.days)
    # print(eList)
    # plt.boxplot(eList)

    # plt.scatter(x, entropyList, label = 'entropy -' + str(k))
    # plt.scatter(x, timeList,  label = 'resolution time -' + str(k))
    # plt.legend()
    # plt.show()
    # plt.cla()
    print(entropy)
    return entropy, eList

def organization(data):
    startDict = {}
    endDict = {}
    for issue in data:
        start = issue[0]['actor']
        end = issue[-1]['actor']
        if start not in startDict:
            startDict[start] = 1
        else: startDict[start] += 1
        if end not in endDict:
            endDict[end] = 1
        else: endDict[end] += 1
    
    org = 0
    L = len(data)
    for start in startDict:
        for end in endDict:
            sum = 0
            for issue in data:
                if issue[0]['actor'] == start and issue[-1]['actor'] == end:
                    sum += 1
            if sum != 0:
                org += sum / L * math.log2(sum * L / (startDict[start] * endDict[end]))
    return org
        

dataPath = settings.path + "data/"
if not os.path.exists(dataPath):
    os.makedirs(dataPath)

resultPath = settings.path + "result/"
if not os.path.exists(resultPath):
    os.makedirs(resultPath)

for issueType in settings.issueTypes:
    print('issue type: ' + issueType)
    x = []
    t = 0
    entropyList = []
    organizationList = []
    efficiencyList = []
    for repo in settings.repos:
        print(repo)
        owner, name = repo.split('/')
        for k in range(3):
            f = open(resultPath + owner + '-' + name + '_' +  issueType+ '-label' + str(k) + '_outlier.json')
            data = json.load(f)
            
            # entropyList.append(analysis(data, k))
            # organizationList.append(organization(data))

            entropy, efficiency = analysis(data, k)

            entropyList.append(entropy)
            efficiencyList.append(efficiency)

            x.append(t)
            t += 1

plt.scatter(x, entropyList, c = 'red')
# plt.scatter(x, organizationList, c = 'blue')
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_axes([0.08, 0.08, 0.9, 0.9])
# bp = ax.boxplot(efficiencyList)
# plt.show()
plt.savefig(resultPath + 'result.jpg')

        
