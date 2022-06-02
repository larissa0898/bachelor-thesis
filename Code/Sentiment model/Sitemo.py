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



def saveDataToFile(finallist):
    df = pd.DataFrame(finallist, columns=['Wort', 'Sentimentscores der Beschreibungen (emo,neu)', 'Durchschnittsscore Emo', 'Durchschnittsscore Neu'])
    df.to_csv(config['PATHS']['VergleichSituationEmo+Neu'], sep='\t', encoding='utf-8')



def extractAndGetAverageScore(df):
    words = getWords(df)
    finallist = []

    for word in words:
        
        wordRows = df.loc[df['Wort'] == word]

        emo_sent_lst = []
        neu_sent_lst = []

        for i in wordRows.index:

            if df['Emotionalität'][i] == 'emo':

                emo_sent_lst.append(df['Sentiment Score'][i])  
        
            if df['Emotionalität'][i] == 'neu':

                neu_sent_lst.append(df['Sentiment Score'][i])  
    
        finallist.append([word, list(zip(emo_sent_lst, neu_sent_lst)), round(sum(emo_sent_lst)/len(emo_sent_lst), 4), round(sum(neu_sent_lst)/len(neu_sent_lst), 4)]) 

    return finallist


if __name__ == '__main__':
    
    saveDataToFile(extractAndGetAverageScore(loadData()))