import pandas as pd
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')



def loadData():
    return pd.read_csv(config['PATHS']['SentimentScoreSituationen'], sep='\t', encoding="utf-8")


def getWords(df):
    words = set()

    for i in range(len(df["Wort"])):

        words.add(df["Wort"][i])
    
    return words


def saveDataToFile(df):
    df.to_csv(config['PATHS']['VergleichSituationEmo_Neu'], sep='\t', encoding='utf-8')


def getAverageScoresAndSetDataframe(df):
    words = getWords(df)
    finallist = []

    for word in words:
        
        wordRows = df.loc[df['Wort'] == word]

        emoSentLst = []
        neuSentLst = []

        for i in wordRows.index:

            if df['Emotionalität'][i] == 'emo':

                emoSentLst.append(df['Sentiment Score'][i])  
        
            if df['Emotionalität'][i] == 'neu':

                neuSentLst.append(df['Sentiment Score'][i])  
        
        sumEmo = 0
        sumNeu = 0

        for i in range(len(emoSentLst)):
            sumEmo += abs(emoSentLst[i])
            sumNeu += abs(neuSentLst[i])

        finallist.append([word, list(zip(emoSentLst, neuSentLst)), round(sumEmo/len(emoSentLst), 4), round(sumNeu/len(neuSentLst), 4)]) 

    return pd.DataFrame(finallist, columns=['Wort', 'Sentimentscores der Beschreibungen (emo,neu)', 'Durchschnittsscore Emo', 'Durchschnittsscore Neu'])


if __name__ == '__main__':
    
    saveDataToFile(getAverageScoresAndSetDataframe(loadData()))