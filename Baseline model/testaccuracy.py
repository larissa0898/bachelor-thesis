import pandas as pd
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')


def calculatePercentages(file):
    neu_neutral = 0
    neu_emotional = 0
    emo_emotional = 0
    emo_neutral = 0
    gesamt = 0
    
    richtiggroesserNull = []
    richtigkleinerNull = []
    falschgroesserNull = []
    falschkleinerNull = []


    for i in range(len(file["Wort"])):

        if file['Modeleinschätzung'][i] == 'neutral':

            if file['Emotionalität'][i] == 'neu':
                neu_neutral +=1
            else:
                emo_neutral +=1

        if file['Modeleinschätzung'][i] == 'emotional':

            if file['Emotionalität'][i] == 'emo':
                emo_emotional +=1
                if file['Sentiment Score'][i] > 0:
                    richtiggroesserNull.append(file['Sentiment Score'][i])
                else:
                    richtigkleinerNull.append(file['Sentiment Score'][i])
            else:
                neu_emotional +=1
                if file['Sentiment Score'][i] > 0:
                    falschgroesserNull.append(file['Sentiment Score'][i])
                else:
                    falschkleinerNull.append(file['Sentiment Score'][i])
        gesamt += 1


    print("neu und neutral interpretiert: ", neu_neutral)
    print("neu und emotional interpretiert: ", neu_emotional)
    print("emo und emotional interpretiert: ", emo_emotional)
    print("emo und neutral interpretiert: ", emo_neutral)
    print("GESAMT: ", gesamt)
    acc = (emo_emotional + neu_neutral) / gesamt * 100

    print("Accuracy: ", acc)
    

    print('EMOTIONAL RICHTIG')
    print('größer Null', sum(richtiggroesserNull)/len(richtiggroesserNull))
    print('kleiner Null', sum(richtigkleinerNull)/len(richtigkleinerNull))

    print('EMOTIONAL FALSCH')
    print('größer Null', sum(falschgroesserNull)/len(falschgroesserNull))
    print('kleiner Null', sum(falschkleinerNull)/len(falschkleinerNull))




featuresFile = pd.read_csv(config['PATHS']['SentimentScoreFeatures'], sep='\t', encoding="utf-8")   # HIER CONFIG EINFÜGEN
situationsFile = pd.read_csv(config['PATHS']['SentimentScoreSituationen'], sep='\t', encoding="utf-8")   # HIER CONFIG EINFÜGEN


#calculatePercentages(featuresFile)
calculatePercentages(situationsFile)