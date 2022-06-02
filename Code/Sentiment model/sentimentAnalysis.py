import pandas as pd
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from configparser import ConfigParser
import json


config = ConfigParser()
config.read('config.ini')


def loadJSON(path):
    zero_shot_results = open(path)

    return json.load(zero_shot_results)


def saveDataToFile(finallist, columns, filename):
    df = pd.DataFrame(finallist, columns=columns)

    df.to_csv(config['PATHS'][filename], sep='\t', encoding='utf-8')


def getSentimentScore(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)

    return score


def getInterpretation(score):
    if score.get('compound') < 0.5 and score.get('compound') > -0.5:
        interpretation = 'neutral'

    else:
        interpretation = 'emotional'

    return interpretation


def listFeaturesToOneString(listOfMaskedFeatures):
    allFeatString = ''
    for feature in listOfMaskedFeatures:

        allFeatString = allFeatString + feature.strip() + ', '

    featureString = allFeatString[:-2]

    return featureString


def getEmotionality(text):
    if 'emotional' in text:
        return 'emo'
    elif 'neutral' in text:
        return 'neu'


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
    
    for i in range(len(df['features'])):

        feature = re.sub(r'\s*\+\s*', ', ', str(df['features'][i]))
        score = getSentimentScore(feature)

        finallist.append([df['VP_Code'][i], df['word'][i], df['emotionality'][i], df['features'][i], score.get('compound'), getInterpretation(score)])


    return finallist, ['VP_Code', 'Wort', 'Emotionalität', 'Features', 'Sentiment Score', 'Interpretation'], 'SentimentScoreFeatures'



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
    generatedFile = loadJSON(config['PATHS']['ZeroShotGenerated'])

    for dict in generatedFile:
        
        word = list(dict.keys())[0].split(',')[0]

        generatedRaw = list(dict.get(list(dict.keys())[0])[0].values())[0]
        generatedClean = re.sub(r'^(.*?)I associate it with', '', generatedRaw)
        generatedFeature = generatedClean.split('.')[0]

        score = getSentimentScore(generatedFeature)
        
        emotionality = getEmotionality(list(dict.keys())[0])

        finallist.append([word, emotionality, generatedFeature, score.get('compound'), getInterpretation(score)])

    return finallist, ['Wort', 'Emotionalität', 'Features', 'Sentiment Score', 'Interpretation'], 'SentimentScoreGenerated'



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
    maskedFile = loadJSON(config['PATHS']['unmasked_en'])

    for dict in maskedFile:

        word = list(dict.keys())[0].split(",")[0]
        featureString = listFeaturesToOneString(listOfMaskedFeatures=list(dict.values())[0])
        score = getSentimentScore(featureString)

        emotionality = getEmotionality(list(dict.keys())[0])

        finallist.append([word, emotionality, featureString, score.get('compound'), getInterpretation(score)])


    return finallist, ['Wort', 'Emotionalität', 'Features', 'Sentiment Score', 'Interpretation'], 'SentimentScoreMasked'



def situations_results(df):
    """
    This function takes German descriptions of a situation of a "Pseudowort" and creates a 
    finallist with sublists of the data that needs to be saved to a file.

    Parameters:
    -----------
    df : DataFrame
        Contains the data of a file.
    
    Returns:
    --------
        Returns a tsv-file with the predicted labels (neutral/emotional).
    """
    finallist = []
    

    for i in range(len(df['Wort'])):

        score = getSentimentScore(df['Situation'][i])

        finallist.append([str(df['Wort'][i]), str(df['Emotionalität'][i]), str(df['Situation'][i]), score.get('compound'), getInterpretation(score)])

    return finallist, ['Wort', 'Emotionalität', 'Situation', 'Sentiment Score', 'Interpretation'], 'SentimentScoreSituationen'



def definition_results(df):
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
    

    for i in range(len(df['Wort'])):

        scoreEmo = getSentimentScore(df['Konzept '][i])
        finallist.append([str(df['Wort'][i]), 'emo', str(df['Konzept '][i]), scoreEmo.get('compound'), getInterpretation(scoreEmo)])


        scoreNeu = getSentimentScore(df['N_Konzept'][i])
        finallist.append([str(df['Wort'][i]), 'neu', str(df['N_Konzept'][i]), scoreNeu.get('compound'), getInterpretation(scoreNeu)])
            

    return finallist, ['Wort', 'Emotionalität', 'Definition', 'Sentiment Score', 'Interpretation'], 'SentimentScoreDefinitionen'



#saveDataToFile(feature_results(pd.read_csv(config['PATHS']['TranslatednewData'], sep='\t', usecols=[1,2,3,4,5,6], encoding='utf-8')))

#saveDataToFile(definition_results(pd.read_csv(config['PATHS']['TranslatedDefinitions'], sep='\t', encoding='utf-8')))

#saveDataToFile(generated_results())
#saveDataToFile(masked_results())
finallist, columns, filename = situations_results(pd.read_csv(config['PATHS']['TranslatedSituations'], sep='\t', usecols=[0,1,2,3], encoding='utf-8'))
saveDataToFile(finallist, columns, filename)