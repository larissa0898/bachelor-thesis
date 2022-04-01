import json
from deep_translator import GoogleTranslator
import re
import pandas as pd


features = pd.read_csv("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Features_clean.csv", sep=';', usecols=[2,3,7], encoding="latin-1")   # HIER CONFIG EINFÜGEN
definitions = pd.read_excel("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Rating_Definitionen.xlsx", usecols=[0,1,8])    # HIER CONFIG EINFÜGEN

finallist = []

for i in range(len(definitions)):

    name = str(definitions["Name"][i])

    definitionEmo = GoogleTranslator(source='auto', target='en').translate(str(definitions["Konzept "][i]))
    definitionNeu = GoogleTranslator(source='auto', target='en').translate(str(definitions["N_Konzept"][i]))

    tmp_associations_emo = []
    tmp_associations_neu = []
    tmp_sublist_neu = []
    tmp_sublist_emo = []

    name_rows = features.loc[features['word'] == name]

    for j in name_rows.index:

        if str(name_rows['features'][j]) != "nan" and str(name_rows['features'][j]) != "Fail" and str(name_rows['features'][j]) != ",":

            if name == str(name_rows["word"][j]) and str(name_rows["emotionality"][j]) == "emo":

                clean = re.sub(r',', '', str(name_rows['features'][j]))
                translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))

                tmp_associations_emo.append(translated_asso)


            else:

                clean = re.sub(r',', '', str(name_rows['features'][j]))
                translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))

                tmp_associations_neu.append(translated_asso)
        
          
    tmp_sublist_neu.append(name)
    tmp_sublist_neu.append("neu")
    tmp_sublist_neu.append(definitionNeu)
    tmp_sublist_neu.append(tmp_associations_neu)

    finallist.append(tmp_sublist_neu)

    tmp_sublist_emo.append(name)
    tmp_sublist_emo.append("emo")
    tmp_sublist_emo.append(definitionEmo)
    tmp_sublist_emo.append(tmp_associations_emo)

    finallist.append(tmp_sublist_emo)




zero_shot_results = open("zero_shot_english_MultiLabel.txt")    # HIER CONFIG EINFÜGEN
zero_shot_results = json.load(zero_shot_results)

overall_avg_score = 0

for sublist in finallist:

    all_indices = []
    all_scores = []
    average_index = 0
    average_score = 0

    for i in range(len(zero_shot_results)):

        indices = []
        scores = []
        zeroshot = list(zero_shot_results[i].values())
        

        if zeroshot[0] == sublist[2]:
            k = 0
            for el in sublist[3]:
                try:
                    index = zeroshot[1].index(el)
                    indices.append(index)

                    score = zeroshot[2][index]
                    scores.append(score)

                    average_index += index
                    average_score += score
                    k += 1
                except ValueError:
                    pass


            all_indices.append(indices)
            all_scores.append(scores)
            average_index = int(average_index / k)
            average_score = average_score / k
        
    sublist.append(all_indices)
    sublist.append(average_index)
    sublist.append(all_scores)
    sublist.append(average_score)
    overall_avg_score += average_score

overall_avg_score = overall_avg_score/(len(finallist)-1)



df = pd.DataFrame(finallist, columns=['Name', 'Emotionalität', 'Definition', 'Assoziationen', 'Index der Scores', 'Durchschnittsindex', 'Scores', 'Durchschnittsscore'])

#df['Gesamtdurchschnittsscore'] = [overall_avg_score]*len(finallist)

df.to_csv("getIndexMultiLable_new.csv", sep='\t', encoding='utf-8')   # HIER CONFIG EINFÜGEN