import pandas as pd
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from deep_translator import GoogleTranslator


##########################################################################################
# Features_clean Datei extrahieren und dem Modell übergeben
##########################################################################################

def feature_results():

    df = pd.read_csv("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\Features_clean.csv", sep=';', usecols=[2,3,7], encoding="latin-1")
    result = []
    texte = []
    scores = []
    k = 0
    for i in range(len(df["features"])):
        if str(df['features'][i]) != "nan" and str(df['features'][i]) != "Fail" and str(df['features'][i]) != ",":
            text = GoogleTranslator(source='auto', target='en').translate(str(df['features'][i]))
            replaced = re.sub(r'\+', ' + ', text)
            texte.append(replaced)
            sia = SentimentIntensityAnalyzer()
            score = sia.polarity_scores(str(replaced))
            scores.append(score)
            if score.get("compound") < 0.5 and score.get("compound") > -0.5:
                result.append("neutral")
            else:
                result.append("emotional")
            print(k)
            k+=1
        else:
            print("-------nan")
    print("done")
    j = 0
    with open('C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\features_results.tsv', 'wt', encoding='utf-8') as out_file:
        for i in range(len(df["features"])):
            if str(df['features'][i]) != "nan" and str(df['features'][i]) != "Fail" and str(df['features'][i]) != ",":
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([df['emotionality'][i], str(df['features'][i]), scores[j], result[j]])    #texte[j],
                j += 1
            else:
                print("secondnan")


##########################################################################################
# Stimuli_clean_emotional Datei extrahieren und dem Modell übergeben
##########################################################################################


def stimuli_resultate_emotional():
    stimuli = pd.read_excel("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\emotional.xlsx", usecols=[0,2,3,4,5,6])
    resultate =[]
    situationen = []
    punktzahl = []
    
    for j in range(1,6):
        for i in range(len(stimuli["Pseudowort"])):
            text = GoogleTranslator(source='auto', target='en').translate(str(stimuli[f'Situation emotional {j}'][i]))
            situationen.append(text)
            sia = SentimentIntensityAnalyzer()
            score = sia.polarity_scores(str(text))
            punktzahl.append(score)
            if score.get("compound") < 0.5 and score.get("compound") > -0.5:
                resultate.append("neutral")
            else:
                resultate.append("emotional")

    m = 0
    with open('C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\stimuli_resultate_emotional.tsv', 'wt', encoding='utf-8') as out_file:
        for k in range(1,6):
            for i in range(len(stimuli["Pseudowort"])):
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([stimuli['Pseudowort'][i], str(stimuli[f'Situation emotional {k}'][i]), situationen[m], punktzahl[m], resultate[m]])
                m += 1



##########################################################################################
# Stimuli_clean_neutral Datei extrahieren und dem Modell übergeben
##########################################################################################


def stimuli_resultate_neutral():
    stimuli = pd.read_excel("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\Stimuli_clean.xlsx", usecols=[0,2,3,4,5,6])
    resultate =[]
    situationen = []
    punktzahl = []

    for j in range(1,6):    
        for i in range(len(stimuli["Pseudwort"])):
            text = GoogleTranslator(source='auto', target='en').translate(str(stimuli[f'Situation neutral {j}'][i]))
            situationen.append(text)
            sia = SentimentIntensityAnalyzer()
            score = sia.polarity_scores(str(text))
            punktzahl.append(score)
            if score.get("compound") < 0.5 and score.get("compound") > -0.5:
                resultate.append("neutral")
            else:
                resultate.append("emotional")

    m = 0
    with open('C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\stimuli_resultate_neutral.tsv', 'wt', encoding='utf-8') as out_file:
        for k in range(1,6):
            for i in range(len(stimuli["Pseudwort"])):
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([stimuli['Pseudwort'][i], str(stimuli[f'Situation neutral {k}'][i]), situationen[m], punktzahl[m], resultate[m]])
                m += 1


#feature_results()
#stimuli_resultate_emotional()
stimuli_resultate_neutral()