from transformers import pipeline
import json
from deep_translator import GoogleTranslator
import re
import pandas as pd


features = pd.read_csv("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Features_clean.csv", sep=';', usecols=[2,3,7], encoding="latin-1")
definitions = pd.read_excel("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Rating_Definitionen.xlsx", usecols=[0,1,8])

finallist = []

""" for i in range(len(definitions)):

    name = str(definitions["Name"][i])
    print(name)
    definitionEmo = GoogleTranslator(source='auto', target='en').translate(str(definitions["Konzept "][i]))
    definitionNeu = GoogleTranslator(source='auto', target='en').translate(str(definitions["N_Konzept"][i]))
    tmp_emo = []
    tmp_neu = []
    tmp2 = []
    tmp3 = []
    for j in range(len(features)):

        if str(features['features'][j]) != "nan" and str(features['features'][j]) != "Fail" and str(features['features'][j]) != ",":

            if name == str(features["word"][j]) and str(features["emotionality"][j]) == "emo":

                clean = re.sub(r',', '', str(features['features'][j]))
                translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))

                tmp_emo.append(translated_asso)


            #if name == str(features["word"][j]) and str(features["emotionality"]) == "neu":
            else:

                clean = re.sub(r',', '', str(features['features'][j]))
                translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))

                tmp_neu.append(translated_asso)
        
          
    tmp2.append(name)
    tmp2.append("neu")
    tmp2.append(definitionNeu)
    tmp2.append(tmp_neu)
    print(tmp2)
    finallist.append(tmp2)

    tmp3.append(name)
    tmp3.append("emo")
    tmp3.append(definitionEmo)
    tmp3.append(tmp_emo)
    print(tmp3)
    finallist.append(tmp3) """

for i in range(len(definitions)):

    name = str(definitions["Name"][i])
    print(name)
    definitionEmo = GoogleTranslator(source='auto', target='en').translate(str(definitions["Konzept "][i]))
    definitionNeu = GoogleTranslator(source='auto', target='en').translate(str(definitions["N_Konzept"][i]))
    tmp_emo = []
    tmp_neu = []
    tmp2 = []
    tmp3 = []

    name_rows = features.loc[features['word'] == name]

    for j in name_rows.index:

        if str(name_rows['features'][j]) != "nan" and str(name_rows['features'][j]) != "Fail" and str(name_rows['features'][j]) != ",":

            if name == str(name_rows["word"][j]) and str(name_rows["emotionality"][j]) == "emo":

                clean = re.sub(r',', '', str(name_rows['features'][j]))
                translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))

                tmp_emo.append(translated_asso)


            #if name == str(features["word"][j]) and str(features["emotionality"]) == "neu":
            else:

                clean = re.sub(r',', '', str(name_rows['features'][j]))
                translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))

                tmp_neu.append(translated_asso)
        
          
    tmp2.append(name)
    tmp2.append("neu")
    tmp2.append(definitionNeu)
    tmp2.append(tmp_neu)

    finallist.append(tmp2)

    tmp3.append(name)
    tmp3.append("emo")
    tmp3.append(definitionEmo)
    tmp3.append(tmp_emo)

    finallist.append(tmp3)




zero_shot_results = open("zero_shot_english.txt")
zero_shot_results = json.load(zero_shot_results)



for sublist in finallist:

    print(sublist)
    all_scores = []
    average_index = 0

    for i in range(len(zero_shot_results)):

        score = []
        zeroshot = list(zero_shot_results[i].values())
        print(zeroshot)
        

        if zeroshot[0] == sublist[2]:
            k = 0
            for el in sublist[3]:
                try:
                    index = zeroshot[1].index(el)
                    score.append(index)
                    average_index += index
                    k += 1
                except ValueError:
                    pass


            all_scores.append(score)
            average_index = int(average_index / k)
        
    sublist.append(all_scores)
    sublist.append(average_index)


df = pd.DataFrame(finallist, columns=['Name', 'Emotionalität', 'Definition', 'Assoziationen', 'Index der Scores', 'Durchschnittsindex'])

df.to_csv("getIndex.csv", sep='\t', encoding='utf-8')