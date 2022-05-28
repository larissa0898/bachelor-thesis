import pandas as pd
import csv
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from configparser import ConfigParser
import json



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

    finallist = []
    scores = []
    
    for i in range(len(df["features"])):

        replaced = re.sub(r'\s*\+\s*', ', ', str(df['features'][i]))

        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(str(replaced))
        scores.append(score)


        if score.get("compound") < 0.5 and score.get("compound") > -0.5:    # 0.7845  und    -0.5388999999999999

            finallist.append([df['VP_Code'][i], df['word'][i], df['emotionality'][i], df['features'][i], score.get('compound'), 'neutral'])

        else:

            finallist.append([df['VP_Code'][i], df['word'][i], df['emotionality'][i], df['features'][i], score.get('compound'), 'emotional'])



    df = pd.DataFrame(finallist, columns=['VP_Code', 'Wort', 'Emotionalität', 'Features', "Sentiment Score", "Interpretation"])

    df.to_csv(config['PATHS']['SentimentScoreFeatures'], sep='\t', encoding='utf-8')



def generated_results():
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

    finallist = []
    scores = []
    zero_shot_results = open(config['PATHS']['ZeroShotGenerated'])
    generated = json.load(zero_shot_results)

    regex = r'^(.*?)I associate it with'

    generated_emo = []
    generated_neu = []
    name_emo = []
    name_neu = []
    finallist = []
    sia = SentimentIntensityAnalyzer()
    for dict in generated:

        if "emotional" in list(dict.keys())[0]:

            name_emo = list(dict.keys())[0].split(",")[0]

            generated_text = list(dict.get(list(dict.keys())[0])[0].values())[0]
            generated_association = re.sub(regex, '', generated_text)
            generated_emo = generated_association.split(".")[0]
            
            score = sia.polarity_scores(generated_emo)
            scores.append(score)

            if score.get("compound") < 0.5 and score.get("compound") > -0.5:    # 0.7845  und    -0.5388999999999999

                finallist.append([name_emo, 'emo', generated_emo, score.get('compound'), 'neutral'])
            else:
                finallist.append([name_emo, 'emo', generated_emo, score.get('compound'), 'emotional'])

        if "neutral" in list(dict.keys())[0]:

            name_neu=list(dict.keys())[0].split(",")[0]

            generated_text = list(dict.get(list(dict.keys())[0])[0].values())[0]
            generated_association = re.sub(regex, '', generated_text)
            generated_neu = generated_association.split(".")[0]
        
            score = sia.polarity_scores(generated_neu)
            scores.append(score)

            if score.get("compound") < 0.5 and score.get("compound") > -0.5:    # 0.7845  und    -0.5388999999999999

                finallist.append([name_neu, 'neu', generated_neu, score.get('compound'), 'neutral'])
            else:
                finallist.append([name_emo, 'neu', generated_neu, score.get('compound'), 'emotional'])


    df = pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Features', "Sentiment Score", "Interpretation"])

    df.to_csv(config['PATHS']['SentimentScoreGenerated'], sep='\t', encoding='utf-8')



def masked_results():
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

    finallist = []
    scores = []
    zero_shot_results = open(config['PATHS']['unmasked_en']) 
    masked = json.load(zero_shot_results)

    regex = r'^(.*?)I associate it with'

    generated_emo = []
    generated_neu = []
    name_emo = []
    name_neu = []
    finallist = []
    sia = SentimentIntensityAnalyzer()
    for dict in masked:

        if "emotional" in list(dict.keys())[0]:

            generated_text = list(dict.values())[0]

            name_emo = list(dict.keys())[0].split(",")[0]
            string = ""
            for asso in generated_text:
                string = string + asso.strip() + ", "

            generated_emo = string[:-2]
            
            score = sia.polarity_scores(generated_emo)
            scores.append(score)

            if score.get("compound") < 0.5 and score.get("compound") > -0.5:    # 0.7845  und    -0.5388999999999999

                finallist.append([name_emo, 'emo', generated_emo, score.get('compound'), 'neutral'])
            else:
                finallist.append([name_emo, 'emo', generated_emo, score.get('compound'), 'emotional'])

        if "neutral" in list(dict.keys())[0]:

            generated_text = list(dict.values())[0]
            name_neu = list(dict.keys())[0].split(",")[0]
            string2 = ""
            for asso2 in generated_text:
                string2 = string2 + asso2.strip() + ", "
            generated_neu = string2[:-2]
        
            score = sia.polarity_scores(generated_neu)
            scores.append(score)

            if score.get("compound") < 0.5 and score.get("compound") > -0.5:    # 0.7845  und    -0.5388999999999999

                finallist.append([name_neu, 'neu', generated_neu, score.get('compound'), 'neutral'])
            else:
                finallist.append([name_emo, 'neu', generated_neu, score.get('compound'), 'emotional'])


    df = pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Features', "Sentiment Score", "Interpretation"])

    df.to_csv(config['PATHS']['SentimentScoreMasked'], sep='\t', encoding='utf-8')

##########################################################################################
# Stimuli_clean_emotional Datei extrahieren und dem Modell übergeben
##########################################################################################


def stimuli_resultate(df):
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
    finallist = []
    all_scores = []
    

    for i in range(len(df["Wort"])):

        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(df["Situation"][i])
        all_scores.append(score)

        if score.get("compound") < 0.5423 and score.get("compound") > -0.528:   # 0.5844  und    -0.24555

            siaResult = score.get("compound")
            finallist.append([str(df["Wort"][i]), str(df["Emotionalität"][i]), str(df["Situation"][i]), siaResult, "neutral"])

        else:

            siaResult = score.get("compound")
            finallist.append([str(df["Wort"][i]), str(df["Emotionalität"][i]), str(df["Situation"][i]), siaResult, "emotional"])

    df = pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Situation', "Sentiment Score", "Interpretation"])

    df.to_csv(config['PATHS']['SentimentScoreSituationen'], sep='\t', encoding='utf-8')



features = pd.read_csv(config['PATHS']['TranslatednewData'], sep='\t', usecols=[1,2,3,4,5,6], encoding="utf-8")
feature_results(features)
#generated_results()
#masked_results()
#stimuli = pd.read_csv(config['PATHS']['TranslatedSituations'], sep="\t", usecols=[0,1,2,3], encoding="utf-8")
#stimuli_resultate(stimuli)
