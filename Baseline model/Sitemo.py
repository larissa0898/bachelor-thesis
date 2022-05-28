from scipy.stats.stats import pearsonr
import pandas as pd
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


sia = pd.read_csv(config['PATHS']['SentimentScoreSituationen'], sep='\t', encoding="utf-8")

names = ['Wunicher', 'Neif', 'Zimerhubst', 'Zwelde', 'Herklögen', 'Preier', 'Muschürdur', 'Ismiprämpf', 'Glühm', 'Rugliebast',
'Wumeizauch', 'Häugnung', 'Wupforau', 'Bismirbiel', 'Enkmitas', 'Mege', 'Faube', 'Odef', 'Skibt', 'Mölauzegt', 'Troff', 
'Bingsemöl', 'Ferandsor', 'Struk', 'Vul', 'Namistell', 'Weforshank', 'Plüpp', 'Bisknirgo', 'Iberletsch']

finallist = []

for name in names:
    name_rows = sia.loc[sia['Wort'] == name]

    emo_avrg = 0
    emo_sent_lst = []
    neu_avrg = 0
    neu_sent_lst = []

    for i in name_rows.index:

        if sia['Emotionalität'][i] == 'emo':

            emo_sent_lst.append(sia['Sentiment Score'][i])  
            emo_avrg += sia['Sentiment Score'][i]
        
        if sia['Emotionalität'][i] == 'neu':

            neu_sent_lst.append(sia['Sentiment Score'][i])  
            neu_avrg += sia['Sentiment Score'][i]
    
    finallist.append([name, list(zip(emo_sent_lst, neu_sent_lst)), emo_avrg/len(emo_sent_lst), neu_avrg/len(neu_sent_lst)])


df = pd.DataFrame(finallist, columns=['Wort', 'Sent Score (emo,neu)', 'Durchschnitt Score Emo', 'Durchschnitt Score Emo'])
df.to_csv('SituationEmoalsNeu.csv', sep='\t', encoding='utf-8')