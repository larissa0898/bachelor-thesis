from nltk.sentiment.vader import SentimentIntensityAnalyzer
from configparser import ConfigParser
import pandas as pd
import re
import json


config = ConfigParser()
config.read('config.ini')


def loadJSON(path):
    zero_shot_results = open(path)

    return json.load(zero_shot_results)


def saveDataToFile(df, filename):
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


def setFeatureOutputDataframe(df):

    finallist = []
    
    for i in range(len(df['features'])):

        feature = re.sub(r'\s*\+\s*', ', ', str(df['features'][i]))
        score = getSentimentScore(feature)

        finallist.append([df['VP_Code'][i], df['word'][i], df['emotionality'][i], df['features'][i], score.get('compound'), getInterpretation(score)])


    return pd.DataFrame(finallist, columns=['VP_Code', 'Wort', 'Emotionalität', 'Features', 'Sentiment Score', 'Interpretation']), 'SentimentScoreFeatures'



def setGeneratedOutputDataframe():

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

    return pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Features', 'Sentiment Score', 'Interpretation']), 'SentimentScoreGenerated'



def setMaskedOutputDataframe():

    finallist = []
    maskedFile = loadJSON(config['PATHS']['unmaskedEn'])

    for dict in maskedFile:

        word = list(dict.keys())[0].split(",")[0]
        featureString = listFeaturesToOneString(listOfMaskedFeatures=list(dict.values())[0])
        score = getSentimentScore(featureString)

        emotionality = getEmotionality(list(dict.keys())[0])

        finallist.append([word, emotionality, featureString, score.get('compound'), getInterpretation(score)])


    return pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Features', 'Sentiment Score', 'Interpretation']), 'SentimentScoreMasked'



def setSituationOutputDataframe(df):

    finallist = []
    

    for i in range(len(df['Wort'])):

        score = getSentimentScore(df['Situation'][i])

        finallist.append([str(df['Wort'][i]), str(df['Emotionalität'][i]), str(df['Situation'][i]), score.get('compound'), getInterpretation(score)])

    return pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Situation', 'Sentiment Score', 'Interpretation']), 'SentimentScoreSituationen'



def setDefinitionOutputDataframe(df):

    finallist = []

    for i in range(len(df['Wort'])):

        scoreEmo = getSentimentScore(df['Konzept '][i])
        finallist.append([str(df['Wort'][i]), 'emo', str(df['Konzept '][i]), scoreEmo.get('compound'), getInterpretation(scoreEmo)])


        scoreNeu = getSentimentScore(df['N_Konzept'][i])
        finallist.append([str(df['Wort'][i]), 'neu', str(df['N_Konzept'][i]), scoreNeu.get('compound'), getInterpretation(scoreNeu)])
            

    return pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Definition', 'Sentiment Score', 'Interpretation']), 'SentimentScoreDefinitionen'


# Sentimentanalyse mit Teilnehmer-Features
#data, filename = setFeatureOutputDataframe(pd.read_csv(config['PATHS']['TranslatedFeatures'], sep='\t', usecols=[1,2,3,4,5,6], encoding='utf-8'))
#saveDataToFile(data, filename)

# Sentimentanalyse mit Definitionen
data, filename = setDefinitionOutputDataframe(pd.read_csv(config['PATHS']['TranslatedDefinitions'], sep='\t', encoding='utf-8'))
saveDataToFile(data, filename)

# Sentimentanalyse mit generierten Features
#data, filename = setGeneratedOutputDataframe()
#saveDataToFile(data, filename)

# Sentimentanalyse mit masked Features
#data, filename =  setMaskedOutputDataframe()
#saveDataToFile(data, filename)

# Sentimentanalyse mit Situationen
#df, filename = setSituationOutputDataframe(pd.read_csv(config['PATHS']['TranslatedSituations'], sep='\t', usecols=[0,1,2,3], encoding='utf-8'))
#saveDataToFile(df, filename)