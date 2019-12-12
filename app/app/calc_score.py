import pandas as pd
from sklearn import preprocessing
import numpy as np

df = pd.read_csv("crime_data.csv")

header_list = list(df['Primary Type'].unique())

dictionary = {
               "DECEPTIVE PRACTICE": 3,
               "OFFENSE INVOLVING CHILDREN": 2,
               "SEX OFFENSE": 2,
               "CRIM SEXUAL ASSAULT": 2,
               "BATTERY": 4,
               "CRIMINAL DAMAGE": 7,
               "MOTOR VEHICLE THEFT": 9,
               "THEFT": 8,
               "OTHER OFFENSE": 5,
               "ASSAULT": 6,
               "BURGLARY": 8,
               "WEAPONS VIOLATION": 9,
               "CRIMINAL TRESPASS": 5,
               "NARCOTICS": 2,
               "ROBBERY": 7,
               "LIQUOR LAW VIOLATION": 2,
               "HOMICIDE": 8,
               "PUBLIC PEACE VIOLATION": 5,
               "INTERFERENCE WITH PUBLIC OFFICER": 4,
               "STALKING": 3,
               "INTIMIDATION": 1,
               "ARSON": 5,
               "HUMAN TRAFFICKING": 1,
               "GAMBLING": 1,
               "KIDNAPPING": 2,
               "PROSTITUTION": 1,
               "NON-CRIMINAL": 1,
               "OBSCENITY": 2,
               "CONCEALED CARRY LICENSE VIOLATION": 6,
               "PUBLIC INDECENCY": 1,
               "NON-CRIMINAL (SUBJECT SPECIFIED)": 1,
               "OTHER NARCOTIC VIOLATION": 1
               }

for i in range(len(df)):
    for j in header_list:
        if df.iloc[i]['Primary Type'] == j:
            df.set_value(i, 'Score', dictionary.get(j))

df.to_excel('crime.xlsx')

grouped = df.groupby(['Block'])['Score'].sum()

grouped.to_excel('crime_son.xlsx')

x_array = np.array(grouped['Score'])
normalized_X = preprocessing.normalize([x_array])
xyz = pd.DataFrame(normalized_X)
zyx = xyz.transpose()
zyx.to_excel('normalize.xlsx')
