import pandas as pd
import re
import csv
from textblob import TextBlob

text="Hallo Welt, was für ein Spaß hier zu leben!"

analysis = TextBlob(text)
eng=analysis.translate(to='en')
print(eng)

##########################################################################################
# Features_clean Datei extrahieren und dem Modell übergeben
##########################################################################################

df = pd.read_csv("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\Features_clean.csv", sep=';', usecols=[2,3,7], encoding="latin-1")

print(df)



with open('C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\dev.tsv', 'wt', encoding='utf-8') as out_file:
    for i in range(len(df["features"])):
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow([df['emotionality'][i], TextBlob(str(df['features'][i])).translate(to='en')])    #re.sub( regex, ' ', str(df['features'][i])))])






##########################################################################################
# Stimuli_clean Datei extrahieren und dem Modell übergeben
##########################################################################################


""" df = pd.read_excel("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\emotional.xlsx", usecols=[0,2])

print(df)
#print(df["features"][0])


regex = r'\*.[^.\s]*'


with open('C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\dev3.tsv', 'wt') as out_file:
    for i in range(len(df["Pseudowort"])):
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow([df['Pseudowort'][i], re.sub( regex, '', str(df['Situation emotional 1'][i]))]) """