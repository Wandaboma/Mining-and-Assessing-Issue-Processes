#select popular repo with the most issue number
import settings
import pymongo
from pymongo import ASCENDING
import json
import os

# connect to database
client = pymongo.MongoClient("***")
db_issue = client['ghdb']['issue']

# count on how many issues for each project
repo_dict = {}
for log in db_issue.find():
   name = log['index']['repo_name']
   owner = log['index']['repo_owner']
   repo = owner + '/' + name
   if repo not in repo_dict:
       repo_dict[repo] = 1
   else: repo_dict[repo] += 1

# sort by the number of issues and output the top ones
repo_list = repo_dict.items()
result = sorted(repo_list, key=lambda x: x[1], reverse=True)
print(result[:40])
