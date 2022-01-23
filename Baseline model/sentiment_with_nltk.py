import pandas as pd
import csv
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')


##########################################################################################
# Features_clean Datei extrahieren und dem Modell übergeben
##########################################################################################

def feature_results(df):
    """
    This function takes German features of a "Pseudowort", translates it to English and 
    returns for the features of every word, if they are neutral or emotional, and saves 
    it to a tsv file.

    Parameters:
    -----------
    df : str
        Contains the relevant columns of the Features_clean.csv file.
    
    Returns:
    --------
        Returns a tsv file with the predicted labels (neutral/emotional).
    """

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
            print("empty column")
    

    j = 0
    with open(config['paths']['save_feat'], 'wt', encoding='utf-8') as out_file:
        for i in range(len(df["features"])):
            if str(df['features'][i]) != "nan" and str(df['features'][i]) != "Fail" and str(df['features'][i]) != ",":
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([df['emotionality'][i], str(df['features'][i]), scores[j], result[j]])    #texte[j],
                j += 1
            else:
                print("empty column")


##########################################################################################
# Stimuli_clean_emotional Datei extrahieren und dem Modell übergeben
##########################################################################################


def stimuli_resultate_emotional(stimuli):
    """
    This function takes German features of a "Pseudowort", translates it to English and 
    returns for the features of every word, if they are neutral or emotional, and saves 
    it to a tsv file.

    Parameters:
    -----------
    stimuli : str
        Contains the relevant columns of the Features_clean.csv file.
    
    Returns:
    --------
        Returns a tsv file with the predicted labels (neutral/emotional).
    """

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
    with open(config['paths']['save_stimuli_emo'], 'wt', encoding='utf-8') as out_file:
        for k in range(1,6):
            for i in range(len(stimuli["Pseudowort"])):
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([stimuli['Pseudowort'][i], str(stimuli[f'Situation emotional {k}'][i]), situationen[m], punktzahl[m], resultate[m]])
                m += 1



##########################################################################################
# Stimuli_clean_neutral Datei extrahieren und dem Modell übergeben
##########################################################################################


def stimuli_resultate_neutral(stimuli):
    """
    This function takes German features of a "Pseudowort", translates it to English and 
    returns for the features of every word, if they are neutral or emotional, and saves 
    it to a tsv file.

    Parameters:
    -----------
    stimuli : str
        Contains the relevant columns of the Features_clean.csv file.
    
    Returns:
    --------
        Returns a tsv file with the predicted labels (neutral/emotional).
    """

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
    with open(config['paths']['save_stimuli_neu'], 'wt', encoding='utf-8') as out_file:
        for k in range(1,6):
            for i in range(len(stimuli["Pseudwort"])):
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([stimuli['Pseudwort'][i], str(stimuli[f'Situation neutral {k}'][i]), situationen[m], punktzahl[m], resultate[m]])
                m += 1






#features = pd.read_csv(config['paths']['filepath_feat'], sep=';', usecols=[2,3,7], encoding="latin-1")
#feature_results(features)

#stimuli = pd.read_excel(config['paths']['filepath_stimuli_emo'], usecols=[0,2,3,4,5,6])
#stimuli_resultate_emotional(stimuli)

#stimuli_2 = pd.read_excel(config['paths']['filepath_stimuli_neu'], usecols=[0,2,3,4,5,6])
#stimuli_resultate_neutral(stimuli_2)