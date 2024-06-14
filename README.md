# Mining-and-Assessing-Issue-Processes
Mining and Assessing Issue Processes In Open Source Software Repositories with Information Entropy

## Code
Source code of the experiment is at code folder
### settings.py
Arguments setting file, store universal settings that are used in every file.
1. **path** : sets where the data, result and graph save to
2. **repos**: list of repos used for the experiment
3. **issueTypes**: originally designed for different types of issues, can be omitted this time
   
### repo_selection.py
First connect to database that stores issue infomation, then select repository with the most number of issues from database.

In the code we output top 40 repos with the most number of issues.

### raw_data_fetch.py
Fetch original issue timeline data from database and store the necessary information to local file.

Rule out the issue data lack of time info or actor info.

### issue_prepocess.py
Process issue data from original raw file to issue sequence.
1. First, save necessary infomation only, which is time, actor and event information
2. Remove abnormal data with unusual length and unsual resolution time
3. Merge same events, e.g.:Label event and unlabel event
4. Set role for each event actor in the issue, as core developer, non-core developer and bots

### issue_time_split.py
Split issue data into 1 month snapshot and save it to files

### kmeans_clustering.py
augmented kmeans++ clustering algorithm

### entropy-resolution.py
calculate variables for RQ2

### detailed_resolution.py
calculate variables for RQ3

### algorithm_effectiveness.py
single sided Mann-Whitney U test for RQ1

### analysis_marco.r
R file to build GLMM models for RQ2

### analysis_mirco.r
R file to build GLMM models for RQ3

### analysis-event-mirco.r
R file to build GLMM models at event level for RQ3

## Execution
For code execution, run the code in the order above.
1. set the output path and repo list
2. connect to database
3. collect issue data
4. preprocess issue data
5. run clustering algorithm
6. run counting code
7. run linear regression model code
   
## Data
Data and results used in the experiment are stored in data folder. Raw data is omitted due to over limit file size. 
### list_of_events.txt
contain all the event in the data
### mean.csv
data for RQ2
### mean_detailed_2020.csv
data for RQ3
