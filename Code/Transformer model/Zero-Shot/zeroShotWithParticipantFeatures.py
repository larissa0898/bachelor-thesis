from transformers import pipeline
import pandas as pd
import re
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def getWords(featuresFile):
    words = set()
    for i in range(len(featuresFile['word'])):
        words.add(featuresFile['word'][i])
    return words


def getFeatureChains(featuresFile):

    featureChains = []

    for i in range(len(featuresFile)):

        cleanFeatureChain = re.sub(r'\s*\+\s*', ', ', featuresFile['features'][i])
        featureChains.append(cleanFeatureChain)

    return featureChains, 'ZeroShotFeaturesChain'


def getAllFeatureChainsOfOneWord(featuresFile):

    pseudowords = getWords(featuresFile)

    allFeatureChains = []

    for word in pseudowords:

        nameRows = featuresFile.loc[featuresFile['word'] == word]

        featureChainsOneWordEmo, featureChainsOneWordNeu = '', ''

        for k in nameRows.index:

            cleanFeatureChain = re.sub(r'\s*\+\s*', ', ', featuresFile['features'][k])

            if str(nameRows["emotionality"][k]) == "emo":

                featureChainsOneWordEmo = featureChainsOneWordEmo + ", " + cleanFeatureChain

            if str(nameRows["emotionality"][k]) == "neu":

                featureChainsOneWordNeu = featureChainsOneWordNeu + ", " + cleanFeatureChain

        allFeatureChains.append(featureChainsOneWordEmo.replace(', ', '', 1))
        allFeatureChains.append(featureChainsOneWordNeu.replace(', ', '', 1))

    return allFeatureChains, 'ZeroShotAllProbandsOneWord'



def getFeaturesSplitted(featuresFile):

    allFeaturesSplitted = set()

    for i in range(len(featuresFile)):

        featureChain = featuresFile['features'][i].split("+")

        for feature in featureChain:

            allFeaturesSplitted.add(feature.strip())

    return list(allFeaturesSplitted), 'ZeroShotFeaturesSplitted'



def getDefinitions(definitionsFile):

    defini = []

    for m in range(len(definitionsFile)):

        defini.append(definitionsFile["Konzept "][m])
        defini.append(definitionsFile["N_Konzept"][m])
    
    return defini



def zeroShotClassification(sequence, labels):

    classifier = pipeline("zero-shot-classification", model="facebook/bart-base", multi_label=True)

    return classifier(sequence, candidate_labels=labels)


def  writeToFile(result, filename):

    with open(config['PATHS'][filename], "w") as fout:
        json.dump(result, fout)




if __name__ == "__main__":

    featuresFile = pd.read_csv(config['PATHS']['TranslatedFeatures'], sep='\t', encoding="utf-8")
    definitionsFile = pd.read_csv(config['PATHS']['TranslatedDefinitions'], sep='\t', encoding='utf-8')

    #features, filename = getFeatureChains(featuresFile)
    features, filename = getAllFeatureChainsOfOneWord(featuresFile)
    #features, filename = getFeaturesSplitted(featuresFile)
    definitions = getDefinitions(definitionsFile)

    writeToFile(zeroShotClassification(definitions, features), filename)