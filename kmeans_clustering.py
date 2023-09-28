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

dataPath = settings.path + "data/"
if not os.path.exists(dataPath):
    os.makedirs(dataPath)

currentTime = datetime.now().strftime('%Y-%m-%d' + 'T' + '%H:%M' + 'Z')

resultPath = settings.path + "result/" + currentTime + "/"
if not os.path.exists(resultPath):
    os.makedirs(resultPath)

graphPath = settings.path + "graph/"
if not os.path.exists(graphPath):
    os.makedirs(graphPath)

def calculateMatrix(issue, alphabet):
    L = len(alphabet)
    countMatrix = np.zeros((L, L))
    sum = 0
    for i in range(0, len(issue) - 1):
        last = issue[i]['role'] + issue[i]['event']
        present = issue[i + 1]['role'] + issue[i + 1]['event']
        countMatrix[alphabet[last]][alphabet[present]] += 1
        sum += 1
    
    # probMatrix = np.zeros((L, L))
    # for i in range(L):
    #     sum = 0
    #     for j in range(L):
    #         sum += countMatrix[i][j]
    #     if sum == 0: continue
    #     for j in range(L):
    #         probMatrix[i][j] = countMatrix[i][j] / sum

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

manhattan_metric = distance_metric(type_metric.MANHATTAN)
for issueType in settings.issueTypes:
    np.seterr(invalid='ignore')
    print('issue type: ' + issueType)

    for repo in settings.repos:
        alphabet = {}
        owner, name = repo.split('/')
        f = open(dataPath + owner + '-' + name + '_' + issueType + '-Outlier.json')
        data = json.load(f)
        i = 0
        for issue in data:
            for event in issue:
                if event['role'] + event['event'] not in alphabet:
                    alphabet[event['role'] + event['event']] = i
                    i += 1
        print(repo, ' ', len(data))
        data = sorted(data, key = lambda x : x[0]['time'])
        result = []

        leftTime = datetime.strptime(data[0][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
        rightTime = leftTime + relativedelta(months=+settings.windowLength)
        topElbow = 0
        lowElbow = 10
        topScore = 0
        lowScore = 10
        alpha = 0.4
        while True:
            print('repo:', repo, 'leftTime: ', leftTime, ' rightTime: ', rightTime)
            slice = []
            for issue in data:
                issueTime = datetime.strptime(issue[0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z')
                if (issueTime >= leftTime) and (issueTime < rightTime):
                    slice.append(issue)
                if issueTime >= rightTime:
                    break
            print('slice size: ', len(slice))
            if len(slice) > 100:
                matrices = []
                for issue in slice:
                    matrices.append(calculateMatrix(issue, alphabet))
                matrix = np.array(matrices)

                elbowList = []
                scoreList = []
                originEntropyList = []
                baseEntropy = analysis(slice)

                # test for approiate K with Silhouette score and entropy minimization
                for k in range(2, 11):
                    entropyList = []
                    # kmeans = KMeans(init = 'k-means++', n_clusters=k)
                    # kmeans.fit(matrices)
                    # labels = kmeans.labels_
                    # score = silhouette_score(matrices, labels)
                    initial_centers = kmeans_plusplus_initializer(matrices, k).initialize()
                    kmeans_instance = kmeans(matrices, initial_centers, metric = manhattan_metric)
                    kmeans_instance.process()
                    clusters = kmeans_instance.get_clusters()
                    labels = clusterToLabel(clusters, len(slice))
                    sList = silhouette(matrices, clusters).process().get_score()
                    score  = statistics.mean(sList)
                    # print(labels)
                    # print(score)
                    # break

                    totalEntropy = 0
                    originEntropy = 0
                    for j in range(k):
                        tempData = []
                        for p, issue in enumerate(slice):
                            if labels[p] == j:
                                tempData.append(issue)
                        entropy = analysis(tempData)
                        originEntropy += len(tempData) / len(slice) * entropy
                        totalEntropy += (baseEntropy - entropy) / max(baseEntropy, entropy) * len(tempData) / len(slice)
                    
                    elbowList.append(totalEntropy)
                    scoreList.append(score)
                    originEntropyList.append(originEntropy)

                elbowList = Normalize(elbowList)
                scoreList = Normalize(scoreList)
                metricList = []
                for k in range(len(elbowList)):
                    metricList.append(alpha * elbowList[k] + (1 - alpha) * scoreList[k])
                # print(metricList)

                optMetric = -1
                optK = 2
                for k in range(len(metricList)):
                    if metricList[k] > optMetric:
                        optMetric = metricList[k]
                        optK = k

                optK += 2
                # kmeans = KMeans(init = 'k-means++', n_clusters = optK) 
                # kmeans.fit(matrices)
                # labels = kmeans.labels_
                initial_centers = kmeans_plusplus_initializer(matrices, optK).initialize()
                kmeans_instance = kmeans(matrices, initial_centers, metric = manhattan_metric)
                kmeans_instance.process()
                clusters = kmeans_instance.get_clusters()
                labels = clusterToLabel(clusters, len(slice))

                sliceResult = []
                for number, issue in enumerate(slice):
                    info = {}
                    info['issue'] = issue
                    info['label'] = int(labels[number])
                    info['K'] = optK
                    sliceResult.append(info)

                # print('chosen K: ', optK)
                result.append(sliceResult)

                sMetric = -1
                originK = 0
                for k in range(len(scoreList)):
                    if scoreList[k] > sMetric:
                        sMetric = scoreList[k]
                        originK = k
                originK += 2
                initial_centers = kmeans_plusplus_initializer(matrices, originK).initialize()
                kmeans_instance = kmeans(matrices, initial_centers, metric = manhattan_metric)
                kmeans_instance.process()
                clusters = kmeans_instance.get_clusters()
                labels = clusterToLabel(clusters, len(slice))
                originEntropy = 0
                for j in range(originK):
                    tempData = []
                    for p, issue in enumerate(slice):
                        if labels[p] == j:
                            tempData.append(issue)
                    entropy = analysis(tempData)
                    originEntropy += len(tempData) / len(slice) * entropy
                # originEntropy = analysis(slice)
                print(repo + ' ' + str(originK) + ' ' + str(originEntropy) + ' ' + str(optK) + ' ' + str(originEntropyList[optK - 2]))
                with open(resultPath + 'comparison.txt', 'a') as f:
                    f.write(repo + ' ' + str(originK) + ' ' + str(originEntropy) + ' ' + str(optK) + ' ' + str(originEntropyList[optK - 2]) + '\n')

            leftTime += relativedelta(months=+settings.stepLength)
            rightTime = leftTime + relativedelta(months=+settings.windowLength)
            if leftTime > datetime.strptime(data[-1][0]['time'], '%Y-%m-%d' + 'T' + '%H:%M:%S' + 'Z'):
                break
            # break

        with open(resultPath + owner + '-' + name + '_' +  issueType+ '-with-label.json', 'w') as f:
            json.dump(result, f)
   


        