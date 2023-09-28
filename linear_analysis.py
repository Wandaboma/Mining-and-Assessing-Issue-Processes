import os
import pandas as pd
resultPath = "/home/sbh/APSEC/result/2023-09-13T16:31Z/"

df = pd.read_csv(resultPath +'mean_detailed_1.csv')
df['merge'] = df['project_name'] + df['event_name']
print(df)
df.to_csv(resultPath +'mean_detailed_merged.csv')
