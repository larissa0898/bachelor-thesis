import json
import re
import pandas as pd
import statistics


def createSublistForFinallist(name, definition, associations, emotionality):
    """
    This function takes a pseudoword, the definition, the associations and the emotionality (emo or neu)
    and returns a list containing this data.

    Parameters:
    -----------
    name : str
       Contains the pseudoword.
    definition : str
        Contains definition of pseudoword.
    associations : list
        Contains list of associations of the pseudoword.
    emotionality : str
        Contains whether pseudoword is neutral or emotional.
   
    
    Returns:
    --------
    sublist : list
       Contains name, definition, associations and emotionality of the pseudoword. 
    """
    sublist = []

    sublist.append(name)
    sublist.append(emotionality)
    sublist.append(definition)
    sublist.append(associations)

    return sublist


def addToChainSublist(sublist, k, all_indices, overallLength, average_index, medianIndex, all_scores, average_score):
    """
    This function takes the number of participants, all indices for the associations of the pseudoword,
    the overall number of all indices, the average index, all scores for the associations of the pseudoword and the average score
    and adds this data to the sublist.

    Parameters:
    -----------
    sublist : list
       Contains the pseudoword.
    k : int
        Contains definition of pseudoword.
    all_indices : list
        Contains list of associations of the pseudoword.
    overallLength : str
        Contains whether pseudoword is neutral or emotional.
    average_index : int
        Contains 
    all_scores : list
        
    average_score : int
   
    
    Returns:
    --------
    sublist : list
       Contains name, definition, associations and emotionality of the pseudoword. 
    """
    sublist.append(k)   
    sublist.append(all_indices)
    sort = all_indices[0].copy()
    sort.sort()
    sublist.append(sort)
    sublist.append(average_index)
    sublist.append(medianIndex)
    sublist.append(getBestPercentage(sort, topindices=195))
    sublist.append(overallLength)
    sublist.append(all_scores)
    sublist.append(average_score)

    return sublist


def addToSplittedSublist(sublist, anzahlProbanden, indicesPerDefinition, all_indices, average_index, overallLength, all_scores, average_score):
    sublist.append(anzahlProbanden)   
    sublist.append(indicesPerDefinition)
    flat_list = [item for lst in indicesPerDefinition for sublst in lst for item in sublst]
    flat_list.sort()
    medianIndex = statistics.median(flat_list)
    sublist.append(flat_list)
    sublist.append(all_indices)
    sublist.append(average_index)
    sublist.append(medianIndex)
    sublist.append(getBestPercentage(flat_list, topindices=454))
    sublist.append(overallLength)
    sublist.append(all_scores)
    sublist.append(average_score)

    return sublist


def getBestPercentage(all_indices, topindices):
    bestIx = 0

    for ix in all_indices:

        if ix <= topindices:

            bestIx += 1
    
    return round(bestIx*100/len(all_indices), 0)
    



def getJsonZeroshot(filename):
    """
    This function takes a pseudoword, the definition, the associations and the emotionality (emo or neu)
    and returns a list containing this data.

    Parameters:
    -----------
    filename : str
        Contains the name of the file.
   
    
    Returns:
    --------
    Returns a json object containing the zero shot output of the model.
    """

    zero_shot_results = open(filename)

    return json.load(zero_shot_results)




def getIndexinZeroShot(indices, scores, averageIndex, medianIndex, averageScore, association, zeroshotAssociation, zeroshotScores, k):

    k = 0
    overallAssociations = len(zeroshotAssociation)
    for el in association:

        index = zeroshotAssociation.index(el)
        indices.append(index)
        medianIndex.append(index)

        score = zeroshotScores[index]
        scores.append(score)

        averageIndex += index
        averageScore += score
        k += 1

    return indices, scores, averageIndex, medianIndex, averageScore, k, overallAssociations



def createListForCsvFile(featuresFile, definitionsFile, splitted):

    finallist = []

    for i in range(len(definitionsFile)):

        name = str(definitionsFile["word"][i])

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
            
        if tmp_associations_emo != []:
            finallist.append(createSublistForFinallist(name, definitionEmo, tmp_associations_emo, emotionality='emo'))
        if tmp_associations_neu != []:
            finallist.append(createSublistForFinallist(name, definitionNeu, tmp_associations_neu, emotionality='neu'))

    
    return finallist



def createCSVFile(finallist, overallAvgScore):

    df = pd.DataFrame(finallist, columns=['Name', 'Emotionalität', 'Definition', 'Assoziationen', 'Anzahl Teilnehmer', 'Index der Scores', 'geordnete Indizes', 'Durchschnittsindex', 'Median Index', 'unter Top 10 Prozent', 'Insgesamte Anzahl der Assoziationen', 'Scores', 'Durchschnittsscore'])
    df['Gesamtdurchschnittsscore'] = [overallAvgScore]*len(finallist)

    df.to_csv("getIndexMultiLable_chainTEEEEEEESSSSSTTTT.csv", sep='\t', encoding='utf-8')   # HIER CONFIG EINFÜGEN




def ZeroShotChainResultToFile(finallist):
    zeroShotResults = getJsonZeroshot("zero_shot_english_MultiLabel_chain.json") 

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

            indices = []
            scores = []
            k = 0

            zeroshot = list(zeroShotResults[i].values())
        
            if zeroshot[0] == sublist[2]:
                anzahlProbanden = len(sublist[3])
                indices, scores, averageIndex, medianIndex, averageScore, k, overallAssociations = getIndexinZeroShot(indices, scores, averageIndex, medianIndex, averageScore, sublist[3], zeroshot[1], zeroshot[2], k)

                all_indices.append(indices)
                all_scores.append(scores)
                averageIndex = int(averageIndex / k)
                
                averageScore = averageScore / k
                overallLength = overallAssociations
        
        
        sublist = addToChainSublist(sublist, anzahlProbanden, all_indices, overallLength, averageIndex, statistics.median(medianIndex), all_scores, averageScore)

        overall_avg_score += averageScore

    overall_avg_score = overall_avg_score/(len(finallist))

    createCSVFile(finallist, overall_avg_score)



def ZeroShotSplittedResultToFile(finallist):
    zeroShotResults = getJsonZeroshot("zero_shot_english_MultiLabel_splitted.json")

    anzahl = 0

    for sublist in finallist:

        all_indices = []
        all_scores = []
        average_index = 0
        average_score = 0
        indicesPerDefinition = []
        anzahl = 0
        overallLength = 0
        

        for i in range(len(zeroShotResults)):

            indices = []
            scores = []
            einzelnIndexDurchschnitt = []
            einzelnScoreDurchschnitt = []

            zeroshot = list(zeroShotResults[i].values())
        
            if zeroshot[0] == sublist[2]:

                associations = sublist[3]
                anzahlProbanden = len(associations)
                zeroshotAssociation = zeroshot[1]
                overallAssociations = len(zeroshotAssociation)
                zeroshotScores = zeroshot[2]
                
                for proband in associations:

                    proband = proband.split('+')
                    einzelnIndex = []
                    einzelnScore = []

                    for el in proband:

                        index = zeroshotAssociation.index(el.strip())
                        einzelnIndex.append(index)


                        score = zeroshotScores[index]
                        einzelnScore.append(score)
                        anzahl += 1

                    indices.append(einzelnIndex)
                    scores.append(einzelnScore)

                    einzelnIndexDurchschnitt.append(int(sum(einzelnIndex)/len(einzelnIndex)))
                    einzelnScoreDurchschnitt.append(sum(einzelnScore)/len(einzelnScore))
                    average_index += sum(einzelnIndex)
                    average_score += sum(einzelnScore)


                indicesPerDefinition.append(indices)
                all_indices.append(einzelnIndexDurchschnitt)
                all_scores.append(einzelnScoreDurchschnitt)
                overallLength = overallAssociations

        #int(all_indices/anzahl)
        sublist = addToSplittedSublist(sublist, anzahlProbanden, indicesPerDefinition, all_indices, int(average_index/anzahl), overallLength, all_scores, average_score/anzahl)

    
    df = pd.DataFrame(finallist, columns=['Name', 'Emotionalität', 'Definition', 'Assoziationen', 'Anzahl Teilnehmer', 'Alle Indizes pro Definition', 'sortierte Indizes', 'Index der Scores', 'Durchschnittsindex', 'Median', 'unter Top 10 Prozent', 'Insgesamte Anzahl der Indizes', 'Scores', 'Durchschnittsscore'])



    df.to_csv("getIndexMultiLable_splittedTEEEEEEEEEEEEST.csv", sep='\t', encoding='utf-8')   # HIER CONFIG EINFÜGEN




featuresFile = pd.read_csv("TranslatednewData.csv", sep='\t', usecols=[1, 2, 3, 6], encoding="utf-8")   # HIER CONFIG EINFÜGEN
definitionsFile = pd.read_csv("TranslatedDefinitions.csv", sep='\t', usecols=[1,2,3], encoding='utf-8')   # HIER CONFIG EINFÜGEN

ZeroShotChainResultToFile(createListForCsvFile(featuresFile, definitionsFile, splitted=False))
#abc = createListForCsvFile(featuresFile, definitionsFile, splitted=True)
#ZeroShotSplittedResultToFile(abc)
