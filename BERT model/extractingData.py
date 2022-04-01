import re
import pandas as pd

features = pd.read_csv("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Features_clean.csv", sep=';', usecols=[0,2,3,5,7], encoding="latin-1")   # HIER CONFIG EINFÜGEN
definitions = pd.read_excel("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Rating_Definitionen.xlsx", usecols=[0,1,8])   # HIER CONFIG EINFÜGEN


vpCode = []
word = []
emotionality = []
group = []
associations = []
definition = []

for i in range(len(features)):

    if str(features['features'][i]) != "nan" and str(features['features'][i]) != "Fail" and str(features['features'][i]) != ",":

        clean_association = re.sub(r',', '', features['features'][i])
        clean_association = re.sub(r'\s*\+\s*', ' + ', clean_association)

        vpCode.append(features['VP_Code'][i])
        word.append(features['word'][i])
        emotionality.append(features['emotionality'][i])
        group.append(features['group'][i])
        associations.append(clean_association)

        if features['emotionality'][i] == 'emo':

            name_rows = definitions.loc[definitions['Name'] == features['word'][i]]
            definition.append(definitions['Konzept '][name_rows.index[0]])

        else: 

            name_rows2 = definitions.loc[definitions['Name'] == features['word'][i]]
            definition.append(definitions['N_Konzept'][name_rows2.index[0]])


finallist = []

for i in range(len(vpCode)):

    finallist.append([vpCode[i], word[i], emotionality[i], definition[i], group[i], associations[i]])


df = pd.DataFrame(finallist, columns=['VP_Code', 'word', 'emotionality', 'definition', 'group', 'features'])


df.to_csv("newData.csv", sep='\t', encoding='utf-8')   # HIER CONFIG EINFÜGEN