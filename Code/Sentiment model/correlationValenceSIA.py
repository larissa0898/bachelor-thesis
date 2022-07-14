from scipy.stats.stats import spearmanr
import pandas as pd
from configparser import ConfigParser
import matplotlib.pyplot as plt
import numpy as np

config = ConfigParser()
config.read('config.ini')


def loadData():
    sia = pd.read_csv(config['PATHS']['SentimentScoreFeatures'], sep='\t', usecols=[1,2,3,4,5,6], encoding="utf-8")
    valence = pd.read_csv(config['PATHS']['Valence'], sep=',', encoding="latin-1")
    return sia, valence


def getWords(df):
    words = set()

    for i in range(len(df["Wort"])):

        words.add(df["Wort"][i])
    
    return words

def getInterpretation(df):
    interpretation = []

    for i in range(len(df)):

        if df['Korrelation'][i][0] > 0.5 or df['Korrelation'][i][0] < -0.5:
           interpretation.append('strong')
        if df['Korrelation'][i][0] < 0.5 and df['Korrelation'][i][0] > 0.3:
           interpretation.append('moderate')
        if df['Korrelation'][i][0] > -0.5 and df['Korrelation'][i][0] < -0.3:
           interpretation.append('moderate')
        if df['Korrelation'][i][0] > -0.3 and df['Korrelation'][i][0] < -0.1:
           interpretation.append('weak')
        if df['Korrelation'][i][0] < 0.3 and df['Korrelation'][i][0] > 0.1:
           interpretation.append('weak')
        if df['Korrelation'][i][0] > -0.1 and df['Korrelation'][i][0] < 0.1:
            interpretation.append('no correlation')


    df['Interpretation'] = interpretation

    return df


def saveDataToFile(df):
    df.to_csv(config['PATHS']['KorrelationSiaValence'], sep='\t', encoding='utf-8')


def setOutputDataframe(sia, valence):
    words = getWords(sia)
    finallist = []

    for word in words:

        siaWordRows = sia.loc[sia['Wort'] == word]
        valenceWordRows = valence.loc[valence['word'] == word]
        
        siaValueEmo, valenceValueEmo, siaValueNeu, valenceValueNeu = [],[],[],[]

        for j in siaWordRows.index:
        
            for k in valenceWordRows.index:

                if sia['Emotionalität'][j] == 'emo' and valence['code'][k] == 'emo' and sia['VP_Code'][j] == valence['VP_Code'][k] and valence['time'][k] == 'post':

                    siaValueEmo.append(sia['Sentiment Score'][j])
                    valenceValueEmo.append(valence['valence_rating'][k])
            
                if sia['Emotionalität'][j] == 'neu' and valence['code'][k] == 'neu' and sia['VP_Code'][j] == valence['VP_Code'][k] and valence['time'][k] == 'post':

                    siaValueNeu.append(sia['Sentiment Score'][j])
                    valenceValueNeu.append(valence['valence_rating'][k])
        sumEmo = 0
        sum_neu = 0
        sumVlncEmo = 0
        sumVlncNeu = 0
        
        for i in range(len(siaValueEmo)):
            sumEmo += abs(siaValueEmo[i])
            sumVlncEmo += abs(valenceValueEmo[i])

        for j in range(len(siaValueNeu)):
            sum_neu += abs(siaValueNeu[j])
            sumVlncNeu += abs(valenceValueNeu[j])
        finallist.append([word, 'emo', siaValueEmo, round(sumEmo/len(siaValueEmo), 4), valenceValueEmo, round(sumVlncEmo/len(valenceValueEmo),2), spearmanr(siaValueEmo, valenceValueEmo)])
        finallist.append([word, 'neu', siaValueNeu, round(sum_neu/len(siaValueNeu), 4), valenceValueNeu, round(sumVlncNeu/len(valenceValueNeu),2), spearmanr(siaValueNeu, valenceValueNeu)])
    
    return pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Sentiment Score', 'Durchschnittsscore', 'Valence Rating', 'Durchschnittsrating', 'Korrelation'])


if __name__ == '__main__':

    sia, valence = loadData()
    df = getInterpretation(setOutputDataframe(sia,valence))
    saveDataToFile(df)
