# Mining-and-Assessing-Issue-Processes
Mining and Assessing Issue Processes In Open Source Software Repositories with Information Entropy

## Code
Source code of the experiment is at code folder
### settings.py
arguments setting file

### repo_selection.py
select repository with the most stars from database

### raw_data_fetch.py
fetch original data from database and store the necessary information to local file

### issue_prepocess.py
process issue data to issue sequence

### issue_time_split.py
split issue data into 1 month snapshot

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

## Data
Data and results used in the experiment are stored in data folder. Raw data is omitted due to over limit file size. 
### list_of_events.txt
contain all the event in the data
### mean.csv
data for RQ2
### mean_detailed_2020.csv
data for RQ3
