import os
import pandas as pd
# import utility function for sample data path
from pymer4.utils import get_resource_path
resultPath = "/home/sbh/APSEC/result/2023-08-03T10:56Z(0.4)/"

df = pd.read_csv(resultPath +'mean_1.csv')
print(df)
