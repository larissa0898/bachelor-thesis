import re
import json
import pandas as pd


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

def addToChainSublist(sublist, k, all_indices, overallLength, average_index, all_scores, average_score):
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
    sublist.append(average_index)
    sublist.append(overallLength)
    sublist.append(all_scores)
    sublist.append(average_score)

    return sublist



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


def createCSVFile(finallist, overallAvgScore):

    df = pd.DataFrame(finallist, columns=['Name', 'Emotionalität', 'Definition', 'Assoziationen', 'Anzahl Teilnehmer', 'Index der Scores', 'Durchschnittsindex', 'Insgesamte Anzahl der Indizes', 'Scores', 'Durchschnittsscore'])
    df['Gesamtdurchschnittsscore'] = [overallAvgScore]*len(finallist)

    df.to_csv("getIndexGenerated.csv", sep='\t', encoding='utf-8')   # HIER CONFIG EINFÜGEN



def getIndexinZeroShot(indices, scores, averageIndex, averageScore, association, zeroshotAssociation, zeroshotScores, k):

    k = 0
    overallAssociations = len(zeroshotAssociation)

    for el in association:

        try:
            index = zeroshotAssociation.index(el)
            indices.append(index)

            score = zeroshotScores[index]
            scores.append(score)

            averageIndex += index
            averageScore += score
            k += 1
        except ValueError:
            print(el)
            #pass
            #print("----------------------------------------------------------------------------------------------------------------------------")
            #print(zeroshotAssociation)
            #print("----------------------------------------------------------------------------------------------------------------------------")

    return indices, scores, averageIndex, averageScore, k, overallAssociations



def createListForCsvFile(featuresFile, name_emo, name_neu, generated_emo, generated_neu, splitted):

    finallist = []

    for i in range(len(name_emo)):

        name = name_emo[i]

        tmp_associations_emo = []

        generatedEmo = generated_emo[i]


        name_rows = featuresFile.loc[featuresFile['word'] == name]

        for j in name_rows.index:

            if str(name_rows["emotionality"][j]) == "emo":

                if splitted == False:

                    cleanAsso = re.sub(r'\s*\+\s*', ', ', str(name_rows['features'][j]))
                    tmp_associations_emo.append(cleanAsso)
                
                else: 
                    tmp_associations_emo.append(str(name_rows['features'][j]))

            
        if tmp_associations_emo != []:
            finallist.append(createSublistForFinallist(name, generatedEmo, tmp_associations_emo, emotionality='emo'))
        


    for i in range(len(name_neu)):

        name = name_neu[i]
        generatedNeu = generated_neu[i]
        
        tmp_associations_neu = []

        name_rows = featuresFile.loc[featuresFile['word'] == name]

        for j in name_rows.index:

            if str(name_rows["emotionality"][j]) == "neu":

                if splitted == False:

                    cleanAsso = re.sub(r'\s*\+\s*', ', ', str(name_rows['features'][j]))
                    tmp_associations_neu.append(cleanAsso)

                else: 
                    tmp_associations_neu.append(str(name_rows['features'][j]))

        if tmp_associations_neu != []:
            finallist.append(createSublistForFinallist(name, generatedNeu, tmp_associations_neu, emotionality='neu'))
    
    with open("finallist.json", "w") as fl:
        json.dump(finallist, fl)
    
    return finallist




def ZeroShotChainResultToFile(finallist):
    zeroShotResults = getJsonZeroshot("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\zero_shot_english_generatedtext_emo.json") 
    zeroShotResults2 = getJsonZeroshot("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\zero_shot_english_generatedtext_neu.json")
    finalzeroshot = []
    for i in range(len(zeroShotResults)):
        finalzeroshot.append(zeroShotResults[i])
        finalzeroshot.append(zeroShotResults2[i])
    with open("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\BERT model\\TEST.json", "w") as fout2:    # HIER CONFIG EINFÜGEN
        json.dump(finalzeroshot, fout2)
    
    #for m in range(len(zeroShotResults2)):
        #finalzeroshot.append(zeroShotResults2[m])
        

    overall_avg_score = 0

    for sublist in finallist:

        all_indices = []
        all_scores = []
        averageIndex = 0
        averageScore = 0
        anzahlProbanden = 0
        overallLength = 0

        #schoneinmal = False

        for i in range(len(finalzeroshot)):

            indices = []
            scores = []
            k = 0
            
        
            zeroshot = list(finalzeroshot[i].values())
        

            itemsWithSameGeneratedAssosiation = []

            for zeroshotsub in finalzeroshot:
                if list(zeroshotsub.values())[0] == sublist[2]:
                    itemsWithSameGeneratedAssosiation.append(list(zeroshotsub.values()))
            
            if len(itemsWithSameGeneratedAssosiation) > 1:
                index = -1
                for items in itemsWithSameGeneratedAssosiation:
                    #if items[1].containsListOfStrings(sublist[3]):
                    if all(x in items[1] for x in sublist[3]):
                        index = itemsWithSameGeneratedAssosiation.index(items)

                zeroshot = itemsWithSameGeneratedAssosiation[index]

            """ anzahlAnEinträgenmitGenerierterAssotioation = finalzeroshot.containsAmount(sublist[2])
            anzahlAnEinträgenmitGenerierterAssotioation > 1 {
                // mache stuff
            } """

            if zeroshot[0] == sublist[2]:# and schoneinmal == False:
                #print(zeroshot[0])
                #print(zeroshot[1])
                anzahlProbanden = len(sublist[3])
                indices, scores, averageIndex, averageScore, k, overallAssociations = getIndexinZeroShot(indices, scores, averageIndex, averageScore, sublist[3], zeroshot[1], zeroshot[2], k)

                all_indices.append(indices)
                all_scores.append(scores)
                averageIndex = int(averageIndex / k)
                averageScore = averageScore / k
                overallLength = overallAssociations
                #schoneinmal = True
                #if(schoneinmal):
                #    print("Hello")

        sublist = addToChainSublist(sublist, anzahlProbanden, all_indices, overallLength, averageIndex, all_scores, averageScore)

        overall_avg_score += averageScore

    overall_avg_score = overall_avg_score/(len(finallist))

    createCSVFile(finallist, overall_avg_score)





zero_shot_results = open("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\BERT model\\generated_en.json")
generated = json.load(zero_shot_results)

regex = r'^(.*?)I associate it with'

generated_emo = []
generated_neu = []
name_emo = []
name_neu = []

for dict in generated:

        if "emotional" in list(dict.keys())[0]:

            name_emo.append(list(dict.keys())[0].split(",")[0])

            generated_text = list(dict.get(list(dict.keys())[0])[0].values())[0]
            generated_association = re.sub(regex, '', generated_text)
            generated_emo.append(generated_association.split(".")[0])

        if "neutral" in list(dict.keys())[0]:

            name_neu.append(list(dict.keys())[0].split(",")[0])

            generated_text = list(dict.get(list(dict.keys())[0])[0].values())[0]
            generated_association = re.sub(regex, '', generated_text)
            generated_neu.append(generated_association.split(".")[0])


featuresFile = pd.read_csv("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\BERT model\\TranslatednewData.csv", sep='\t', usecols=[1, 2, 3, 6], encoding="utf-8")   # HIER CONFIG EINFÜGEN

ZeroShotChainResultToFile(createListForCsvFile(featuresFile, name_emo, name_neu, generated_emo, generated_neu, splitted=False))