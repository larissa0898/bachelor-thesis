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
    it to a tsv-file.

    Parameters:
    -----------
    df : DataFrame
        Contains the relevant columns of the Features_clean.csv file.
    
    Returns:
    --------
        Returns a tsv-file with the predicted labels (neutral/emotional).
    """
    compound = []
    result = []
    texte = []
    scores = []
    
    for i in range(len(df["features"])):

        if str(df['features'][i]) != "nan" and str(df['features'][i]) != "Fail" and str(df['features'][i]) != ",":
            replaced = re.sub(r'\+', ' + ', str(df['features'][i]))
            translated = GoogleTranslator(source='auto', target='en').translate(replaced)
            texte.append(translated)

            sia = SentimentIntensityAnalyzer()
            score = sia.polarity_scores(str(translated))
            scores.append(score)

            if score.get("compound") < 0.5 and score.get("compound") > -0.5:    # 0.7845  und    -0.5388999999999999
                result.append("neutral")
                compound.append(score.get("compound"))
            else:
                result.append("emotional")
                compound.append(score.get("compound"))



    j = 0
    with open("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\compound_TEST1var.tsv", 'wt', encoding='utf-8') as out_file:   #config['save_paths']['save_feat']

        for i in range(len(df["features"])):

            if str(df['features'][i]) != "nan" and str(df['features'][i]) != "Fail" and str(df['features'][i]) != ",":
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([df['word'][i], df['emotionality'][i], str(df['features'][i]), scores[j], result[j]])    #texte[j],
                j += 1



##########################################################################################
# Stimuli_clean_emotional Datei extrahieren und dem Modell übergeben
##########################################################################################


def stimuli_resultate_emotional(stimuli):
    """
    This function takes German descriptions of a situation of a "Pseudowort", translates it to English and 
    returns for the situations of every word, if they are neutral or emotional, and saves 
    it to a tsv-file.

    Parameters:
    -----------
    stimuli : DataFrame
        Contains the relevant columns of the Stimuli_clean.xlsx-file.
    
    Returns:
    --------
        Returns a tsv-file with the predicted labels (neutral/emotional).
    """
    compound_values = []
    results =[]
    translated_situations = []
    all_scores = []
    
    for j in range(1,6):

        for i in range(len(stimuli["Pseudowort"])):

            text = GoogleTranslator(source='auto', target='en').translate(str(stimuli[f'Situation emotional {j}'][i]))
            translated_situations.append(text)
            sia = SentimentIntensityAnalyzer()
            score = sia.polarity_scores(str(text))
            all_scores.append(score)

            if score.get("compound") < 0.5423 and score.get("compound") > -0.528:   # 0.5844  und    -0.24555
                results.append("neutral")
                compound_values.append(score.get("compound"))
            else:
                results.append("emotional")
                compound_values.append(score.get("compound"))


    m = 0
    with open("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\compound_emo1var.tsv", 'wt', encoding='utf-8') as out_file:   #config['save_paths']['save_stimuli_emo']

        for k in range(1,6):

            for i in range(len(stimuli["Pseudowort"])):

                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([stimuli['Pseudowort'][i], str(stimuli[f'Situation emotional {k}'][i]), all_scores[m], results[m]]) #translated_situations[m],
                m += 1



##########################################################################################
# Stimuli_clean_neutral Datei extrahieren und dem Modell übergeben
##########################################################################################


def stimuli_resultate_neutral(stimuli):
    """
    This function takes German descriptions of a situation of a "Pseudowort", translates it to English and 
    returns for the situations of every word, if they are neutral or emotional, and saves 
    it to a tsv-file.

    Parameters:
    -----------
    stimuli : DataFrame
        Contains the relevant columns of the Stimuli_clean.xlsx-file.
    
    Returns:
    --------
        Returns a tsv-file with the predicted labels (neutral/emotional).
    """
    compound_values = []
    results = []
    translated_situations = []
    all_scores = []

    for j in range(1,6):    

        for i in range(len(stimuli["Pseudwort"])):

            text = GoogleTranslator(source='auto', target='en').translate(str(stimuli[f'Situation neutral {j}'][i]))
            translated_situations.append(text)
            sia = SentimentIntensityAnalyzer()
            score = sia.polarity_scores(str(text))
            all_scores.append(score)

            if score.get("compound") < 0.5423 and score.get("compound") > -0.528:
                results.append("neutral")
                compound_values.append(score.get("compound"))
            else:
                results.append("emotional")
                compound_values.append(score.get("compound"))


    m = 0
    with open(config['save_paths']['save_stimuli_neu'], 'wt', encoding='utf-8') as out_file:

        for k in range(1,6):

            for i in range(len(stimuli["Pseudwort"])):

                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([stimuli['Pseudwort'][i], str(stimuli[f'Situation neutral {k}'][i]), all_scores[m], results[m]])  # append "translated_situations[m], ", if english version should be in output file
                m += 1






#features = pd.read_csv(config['load_paths']['filepath_feat'], sep=';', usecols=[2,3,7], encoding="latin-1")
#feature_results(features)

stimuli = pd.read_excel(config['load_paths']['filepath_stimuli_emo'], usecols=[0,2,3,4,5,6])
stimuli_resultate_emotional(stimuli)

#stimuli_2 = pd.read_excel(config['load_paths']['filepath_stimuli_neu'], usecols=[0,2,3,4,5,6])
#stimuli_resultate_neutral(stimuli_2)