#select popular repo with the most star number
import settings
import pymongo
from pymongo import ASCENDING
import json
import os

client = pymongo.MongoClient("mongodb://root:workwork@172.27.135.32:27017/?authSource=admin")
db_star = client['ghdb']['issue']

repo_dict = {}
for log in db_star.find():
   name = log['index']['repo_name']
   owner = log['index']['repo_owner']
   repo = owner + '/' + name
   if repo not in repo_dict:
       repo_dict[repo] = 1
   else: repo_dict[repo] += 1

repo_list = repo_dict.items()
result = sorted(repo_list, key=lambda x: x[1], reverse=True)
print(result[:40])

# repos = settings.repos
# db_star = client['ghdb']['star']
# starDict = {}
# for repo in repos:
#     starDict[repo] = 0
# for log in db_star.find():
#     name = log['index']['repo_name']
#     owner = log['index']['repo_owner']
#     repo = owner + '/' + name
#     if repo in starDict:
#         starDict[repo] += 1
# print(starDict)

# db_commit = client['ghdb']['commit']
# commitDict = {}
# for repo in repos:
#     commitDict[repo] = 0
# for log in db_commit.find():
#     name = log['index']['repo_name']
#     owner = log['index']['repo_owner']
#     repo = owner + '/' + name
#     if repo in commitDict:
#         commitDict[repo] += 1
# print(commitDict)

# db_PR = client['ghdb']['pullRequest']
# PRDict = {}
# for repo in repos:
#     PRDict[repo] = 0
# for log in db_PR.find():
#     name = log['index']['repo_name']
#     owner = log['index']['repo_owner']
#     repo = owner + '/' + name
#     if repo in PRDict:
#         PRDict[repo] += 1
# print(PRDict)
# #
# db_issue = client['ghdb']['issue']
# issueDict = {}
# for repo in repos:
#     issueDict[repo] = 0
# for log in db_issue.find():
#     name = log['index']['repo_name']
#     owner = log['index']['repo_owner']
#     repo = owner + '/' + name
#     if repo in issueDict:
#         issueDict[repo] += 1
# print(issueDict)

# participant = {}
# for repo in repos:
#     nameDict = {}
#     for log in db_issue.find():
#         name = log['index']['repo_name']
#         owner = log['index']['repo_owner']
#         repoNow = owner + '/' + name
#         if repoNow == repo:
#             issue = log['data']['repository']['issue']
#             if 'author' not in issue: continue
#             author = issue['author']
#             if 'login' in author:
#                 name = author['login']
#                 if name not in nameDict:
#                     nameDict[name] = 1
#                 else:
#                     nameDict[name] += 1
    
#     for log in db_PR.find():
#         name = log['index']['repo_name']
#         owner = log['index']['repo_owner']
#         repoNow = owner + '/' + name
#         if repoNow == repo:
#             PR = log['data']['repository']['pullRequest']
#             if 'author' not in PR: continue
#             author = PR['author']
#             if 'login' in author:
#                 name = author['login']
#                 if name not in nameDict:
#                     nameDict[name] = 1
#                 else:
#                     nameDict[name] += 1
    
#     for log in db_commit.find():
#         name = log['index']['repo_name']
#         owner = log['index']['repo_owner']
#         repoNow = owner + '/' + name
#         if repoNow == repo:
#             issue = log['data']['repository']['object']
#             if 'author' not in issue: continue
#             author = issue['author']
#             if 'user' in author:
#                 user = author['user']
#                 if 'login' in user:
#                     name = user['login']
#                     if name not in nameDict:
#                         nameDict[name] = 1
#                     else:
#                         nameDict[name] += 1
#     participant[repo] = len(nameDict)
# print(participant)
# used to count repo, star, fork, commit, pr, issue, participant
# Project, Stars, Commits, Pull-requests, Issues, Participants

