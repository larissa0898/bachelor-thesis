from transformers import pipeline
from configparser import ConfigParser
import json
import re
import pandas as pd

config = ConfigParser()
config.read('config.ini')


def loadDataFrame(filename):
    return pd.read_csv(config['PATHS'][filename], sep='\t', encoding="utf-8")


def loadJSON(filename):
    data = open(config['PATHS'][filename], 'r')
    return json.load(data)


def saveDataAsJSON(data, filename):
    with open(config['PATHS'][filename], "w") as fout:
        json.dump(data, fout)


def cleanParticipantFeatures():
    featuresDf = loadDataFrame('TranslatedFeatures')

    associations_neu = []
    associations_emo = []

    for i in range(len(featuresDf)):

        clean_association = re.sub(r'\s*\+\s*', ', ', featuresDf['features'][i])

        #if featuresDf["emotionality"][i] == "neu":
        #    associations_neu.append(clean_association)

        #if featuresDf["emotionality"][i] == "emo":
        #    associations_emo.append(clean_association)
        associations_emo.append(clean_association)


    #allFeatures = [associations_emo, associations_neu]

    return associations_emo


def getDefinitions():
    definitionsDf = loadDataFrame('TranslatedDefinitions')

    definiNeu = []
    definiEmo = []

    for m in range(len(definitionsDf)):

        definiEmo.append(definitionsDf["Konzept "][m])
        definiNeu.append(definitionsDf["N_Konzept"][m])
    
    return definiNeu, definiEmo


def getMaskedFeatures(maskedFile, allFeatures=True):

    maskedNeu, maskedEmo = [], []
    
    for dict in maskedFile:
        maskedText = list(dict.values())[0]

        if "emotional" in list(dict.keys())[0]:

            string = ""
            for featEmo in maskedText:
                string = string + featEmo.strip() + ", "

            maskedEmo.append(string[:-2])

        if "neutral" in list(dict.keys())[0]:

            string2 = ""
            for featNeu in maskedText:
                string2 = string2 + featNeu.strip() + ", "
            maskedNeu.append(string2[:-2])
            
    if allFeatures == True:
        masked = []
        for i in range(len(maskedNeu)):
            masked.append(maskedNeu[i])
            masked.append(maskedEmo[i])
        return masked

    return maskedNeu, maskedEmo


def getGeneratedFeatures(generatedFile):
    generated_neu, generated_emo = [], []

    regex = r'^(.*?)I associate it with'

    for dict in generatedFile:

        if "emotional" in list(dict.keys())[0]:

            generated_text = list(dict.get(list(dict.keys())[0])[0].values())[0]
            print(generated_text)
            generated_association = re.sub(regex, '', generated_text)
            generated_emo.append(generated_association.split(".")[0])

        if "neutral" in list(dict.keys())[0]:

            generated_text = list(dict.get(list(dict.keys())[0])[0].values())[0]
            generated_association = re.sub(regex, '', generated_text)
            generated_neu.append(generated_association.split(".")[0])
            
    return generated_neu, generated_emo



def zeroShotClassification(sequenceNeu, sequenceEmo, labelsNeu, labelsEmo):
     
    classifierNeu = pipeline("zero-shot-classification", model="facebook/bart-base", multi_label=True)  # model="bert-base-german-cased"
    classifierEmo = pipeline("zero-shot-classification", model="facebook/bart-base", multi_label=True)
    
    saveDataAsJSON(classifierNeu(sequenceNeu, candidate_labels=labelsNeu), 'ZeroShotMaskedNeu')
    saveDataAsJSON(classifierEmo(sequenceEmo, candidate_labels=labelsEmo), 'ZeroShotMaskedEmo')


def zeroShotClassificationAllFeatures(sequence,labels):
     
    classifierNeu = pipeline("zero-shot-classification", model="facebook/bart-base", multi_label=True)
    
    saveDataAsJSON(classifierNeu(sequence, candidate_labels=labels), 'ZeroShotMaskedWithAllFeatures')




#data = loadJSON('unmaskedEn')

# Zero-Shot-Classification für masked Features
#maskedFeat = getMaskedFeatures(data)
#participantFeat = cleanParticipantFeatures()
#zeroShotClassificationAllFeatures(maskedFeat, participantFeat)


# Zero-Shot-Classification für gesplittete masked Features mit Teilnehmer-Features als Label
#maskedFeatNeu, maskedFeatEmo = getMaskedFeatures(loadJSON('unmaskedEn'))
#participantFeat = cleanParticipantFeatures()
#zeroShotClassification(maskedFeatNeu, maskedFeatEmo, labelsNeu=participantFeat[1], labelsEmo=participantFeat[0])


# Zero-Shot-Classification für masked Features mit Definitionen als Label
#maskedFeatNeu, maskedFeatEmo = getMaskedFeatures(loadJSON('unmaskedEn'))
#definiNeu, definiEmo = getDefinitions()
#zeroShotClassification(maskedFeatNeu, maskedFeatEmo, labelsNeu=definiNeu, labelsEmo=definiEmo)


# Zero-Shot-Classification für generated Features
#generatedFeatNeu, generatedFeatEmo = getGeneratedFeatures(loadJSON('generatedEn'))
#zeroShotClassification(generatedFeatNeu, generatedFeatEmo, labelsNeu=participantFeat[1], labelsEmo=participantFeat[0])
#zeroShotClassification(generatedFeatNeu, generatedFeatEmo, labelsNeu=definiNeu, labelsEmo=definiEmo)