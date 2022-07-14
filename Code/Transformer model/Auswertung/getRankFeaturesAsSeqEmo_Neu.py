import json
import re
import pandas as pd
import statistics
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def createSublistForFinallist(name, definition, associations, emotionality):

    sublist = []

    sublist.append(name)
    sublist.append(emotionality)
    sublist.append(definition)
    sublist.append(associations)

    return sublist


def addToChainSublist(sublist, k, all_indices, overallLength, average_index, medianIndex, all_scores, average_score):

    sublist.append(k)   
    sublist.append(all_indices)
    sort = [el for sublst in all_indices for el in sublst]
    sort.sort()
    sublist.append(sort)
    sublist.append(int(average_index/len(sort)))
    sublist.append(medianIndex)
    sublist.append(getBestPercentage(sort, topindices=6))
    sublist.append(overallLength)
    sublist.append(all_scores)
    sublist.append(average_score/len(all_scores))

    return sublist


def getBestPercentage(all_indices, topindices):
    bestIx = 0

    for ix in all_indices:

        if ix <= topindices:

            bestIx += 1
    
    return round(bestIx*100/len(all_indices), 0)



def getJsonZeroshot(filename):

    zero_shot_results = open(filename)

    return json.load(zero_shot_results)




def getIndexinZeroShot(all_indices, all_scores, averageIndex, medianIndex, averageScore, definition, zeroshotAssociation, zeroshotScores):

    overallAssociations = len(zeroshotAssociation)

    index = zeroshotAssociation.index(definition[0])
    index2 = zeroshotAssociation.index(definition[1])
    all_indices.append([index, index2])
    medianIndex.append(index)
    medianIndex.append(index2)


    score = zeroshotScores[index]
    score2 = zeroshotScores[index2]
    all_scores.append([score,score2])

    averageIndex += index + index2
    averageScore += score + score2

    return all_indices, all_scores, averageIndex, medianIndex, averageScore, overallAssociations



def createListForCsvFile(featuresFile, definitionsFile, splitted):

    finallist = []

    for i in range(len(definitionsFile)):

        name = str(definitionsFile["Wort"][i])

        definitionEmo = str(definitionsFile["Konzept "][i])
        definitionNeu = str(definitionsFile["N_Konzept"][i])

        tmp_associations_emo = []
        tmp_associations_neu = []


        name_rows = featuresFile.loc[featuresFile['word'] == name]

        for j in name_rows.index:

            if str(name_rows["emotionality"][j]) == "emo":

                if splitted == False:

                    cleanAsso = re.sub(r'\s*\+\s*', ', ', str(name_rows['features'][j]))
                    tmp_associations_emo.append(cleanAsso)

                else: 
                    tmp_associations_emo.append(str(name_rows['features'][j]))

            else:
                if splitted == False:

                    cleanAsso = re.sub(r'\s*\+\s*', ', ', str(name_rows['features'][j]))
                    tmp_associations_neu.append(cleanAsso)

                else: 
                    tmp_associations_neu.append(str(name_rows['features'][j]))
            

        finallist.append(createSublistForFinallist(name, [definitionEmo, definitionNeu], tmp_associations_emo, emotionality='emo'))
        finallist.append(createSublistForFinallist(name, [definitionNeu,definitionEmo], tmp_associations_neu, emotionality='neu'))

    
    return finallist



def createCSVFile(finallist, overallAvgScore):

    df = pd.DataFrame(finallist, columns=['Name', 'Emotionalität', 'Definition', 'Features', 'Anzahl Teilnehmer', 'Index der Scores', 'geordnete Indizes', 'Durchschnittsindex', 'Median Index', 'unter Top 10 Prozent', 'Insgesamte Anzahl der Assoziationen', 'Scores', 'Durchschnittsscore'])
    df['Gesamtdurchschnittsscore'] = [overallAvgScore]*len(finallist)

    df.to_csv(config['PATHS']['GetIndexFeaturesAsSeqEmo_Neu'], sep='\t', encoding='utf-8')   # HIER CONFIG EINFÜGEN




def ZeroShotChainResultToFile(finallist):
    zeroShotResults = getJsonZeroshot(config['PATHS']['ZeroShotFeaturesAsSeq']) 
    overall_avg_score = 0

    for sublist in finallist:

        all_indices = []
        all_scores = []
        averageIndex = 0
        averageScore = 0
        anzahlProbanden = 0
        overallLength = 0
        medianIndex = []

        for i in range(len(zeroShotResults)):


            zeroshot = list(zeroShotResults[i].values())

            for associationchain in sublist[3]:

                if zeroshot[0] == associationchain:

                    anzahlProbanden = len(sublist[3])
                    all_indices, all_scores, averageIndex, medianIndex, averageScore, overallAssociations = getIndexinZeroShot(all_indices, all_scores, averageIndex, medianIndex, averageScore, sublist[2], zeroshot[1], zeroshot[2])

                    overallLength = overallAssociations
        
        
        sublist = addToChainSublist(sublist, anzahlProbanden, all_indices, overallLength, averageIndex, statistics.median(medianIndex), all_scores, averageScore)

        overall_avg_score += averageScore

    overall_avg_score = overall_avg_score/(len(finallist))

    createCSVFile(finallist, overall_avg_score)




featuresFile = pd.read_csv(config['PATHS']['TranslatedFeatures'], sep='\t', usecols=[1, 2, 3, 6], encoding="utf-8")
definitionsFile = pd.read_csv(config['PATHS']['TranslatedDefinitions'], sep='\t', usecols=[1,2,3], encoding='utf-8')

ZeroShotChainResultToFile(createListForCsvFile(featuresFile, definitionsFile, splitted=False))