from typing import List
import json
import os
import numpy as np
from queue import PriorityQueue
import math
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool
import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sklearn.cluster import KMeans
import scipy
import statistics
from sklearn.metrics import silhouette_score
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.silhouette import silhouette

def Normalize(data):
    xmin = min(data)
    xmax = max(data)
    for i, x in enumerate(data):
        data[i] = (x - xmin) / (xmax - xmin)
    return data

def analysis(data, alphabet):
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

def calculateMatrix(issue, alphabet):
    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    sum = 0
    for i in range(0, len(issue) - 1):
        for eventLast in issue[i]:
            for eventNext in issue[i + 1]:
                # print(eventLast)
                # print(eventNext)
                last = eventLast['role'] + eventLast['event']
                present = eventNext['role'] + eventNext['event']
                countMatrix[alphabet[last]][alphabet[present]] += 1
                sum += 1

    #changed to overall probability for manhattan distance
    probMatrix = np.zeros((L, L))
    for i in range(L):
        for j in range(L):
            probMatrix[i][j] = countMatrix[i][j] / sum
    return probMatrix.flatten()

def clusterToLabel(clusters, L):
    labels = np.zeros((L))
    for num, cluster in enumerate(clusters):
        for id in cluster:
            labels[id] = num
    return labels

dataPath = settings.path + "data/"
currentTime = datetime.now().strftime('%Y-%m-%d' + 'T' + '%H:%M' + 'Z')
resultPath = settings.path + "result/" + currentTime + "/"
if not os.path.exists(resultPath):
    os.makedirs(resultPath)

manhattan_metric = distance_metric(type_metric.MANHATTAN)
alpha = float(input("input value of alpha:"))
issueType = 'all'
result = []
for repo in settings.repos:
    print(repo)
    owner, name = repo.split('/')
    repoPath = dataPath + owner + '-' + name + '/'
    filenames = os.listdir(repoPath)
    resultRepoPath = resultPath + owner + '-' + name + '/'
    if not os.path.exists(resultRepoPath):
        os.makedirs(resultRepoPath)
    # print(filenames)
    for filename in filenames:
        if 'small' not in filename: continue
        f = open(repoPath + filename)
        # already split data into snapshots and saved in files
        data = json.load(f)
        alphabet = {}
        i = 0
        for issue in data:
            for group in issue:
                for event in group:
                    if event['role'] + event['event'] not in alphabet:
                        alphabet[event['role'] + event['event']] = i
                        i += 1
        # print(alphabet)
        print(filename, len(data))
       
        matrices = []
        for issue in data:
            matrices.append(calculateMatrix(issue, alphabet))
        matrix = np.array(matrices)

        entropyList = []
        deltaEntropyList = []
        scoreList = []
        baseEntropy = analysis(data, alphabet)
        resultLabels = []
        # test for approiate K with Silhouette score and entropy minimization
        for k in range(2, 10):
            print('algorithm:', k)
            initial_centers = kmeans_plusplus_initializer(matrices, k).initialize()
            kmeans_instance = kmeans(matrices, initial_centers, metric = manhattan_metric)
            kmeans_instance.process()
            clusters = kmeans_instance.get_clusters()
            labels = clusterToLabel(clusters, len(data))
            sList = silhouette(matrices, clusters).process().get_score()
            score  = statistics.mean(sList)

            totalEntropy = 0
            originEntropy = 0
            for j in range(k):
                tempData = []
                for p, issue in enumerate(data):
                    if labels[p] == j:
                        tempData.append(issue)
                entropy = analysis(tempData, alphabet)
                originEntropy += len(tempData) / len(data) * entropy
            deltaEntropy = baseEntropy - originEntropy
            
            deltaEntropyList.append(deltaEntropy)
            entropyList.append(originEntropy)
            scoreList.append(score)
            resultLabels.append(list(labels))

        # print(entropyList)
        # print(deltaEntropyList)
        deltaEntropyList = Normalize(deltaEntropyList)
        # print(deltaEntropyList)
        scoreList = Normalize(scoreList)
        metricList = []
        for k in range(len(deltaEntropyList)):
            metricList.append(alpha * deltaEntropyList[k] + (1 - alpha) * scoreList[k])

        maxOriginScore = max(scoreList)
        originalK = scoreList.index(maxOriginScore) + 2

        maxMetric = max(metricList)
        optK = metricList.index(maxMetric) + 2

        result.append([repo, filename, originalK, entropyList[originalK - 2], optK, entropyList[optK -2]])

        with open(resultPath + 'comparison-' + str(alpha)+ '.txt', 'a') as f:
                    f.write(repo + ' ' + str(originalK) + ' ' + str(entropyList[originalK - 2]) + ' ' + str(optK) + ' ' + str(entropyList[optK -2]) + '\n')
        with open(resultRepoPath + filename, 'w') as f:
            json.dump(resultLabels[optK - 2], f)
        print(optK)
        # print(resultLabels[optK - 2])
    #     break
    # break

with open(resultPath + 'comparison- ' + str(alpha) + '.json', 'w') as f:
    json.dump(result, f)
