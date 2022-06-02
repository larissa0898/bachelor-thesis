from transformers import pipeline
import pandas as pd
import re
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def getAssociationChain(featuresFile):
    """
    This function takes the FeaturesFile with all the data
    and returns the association chains from this file together with the filename.

    Parameters:
    -----------
    featuresFile : pd.DataFrame
       Contains the data with the associations.
   
    
    Returns:
    --------
    assoziationen : list
        Contains all association chains.
    filename : str
        Contains filename.
    """
    assoziationen = []

    for i in range(len(featuresFile)):

        translated_feat = re.sub(r'\s*\+\s*', ', ', featuresFile['features'][i])
        assoziationen.append(translated_feat)
    #filename = "zero_shot_english_MultiLabel_chain.json"
    filename = config['PATHS']['ZeroShotAndersrum']

    return assoziationen, filename


def getAssociationChainOfOneWord(featuresFile):
    """
    This function takes the FeaturesFile with all the data
    and returns the association chains from this file together with the filename.

    Parameters:
    -----------
    featuresFile : pd.DataFrame
       Contains the data with the associations.
   
    
    Returns:
    --------
    assoziationen : list
        Contains all association chains.
    filename : str
        Contains filename.
    """
    assoziationen = []
    pseudowords = ['Wunicher', 'Neif', 'Zimerhubst', 'Zwelde', 'Herklögen', 'Preier', 'Muschürdur', 'Ismiprämpf', 'Glühm', 'Rugliebast', 'Wumeizauch', 'Häugnung', 'Wupforau', 'Bismirbiel', 'Enkmitas',
                    'Mege', 'Faube', 'Odef', 'Skibt', 'Mölauzegt', 'Troff', 'Bingsemöl', 'Ferandsor', 'Struk', 'Vul', 'Namistell', 'Weforshank', 'Plüpp', 'Bisknirgo', 'Iberletsch']
    for word in pseudowords:

        name_rows = featuresFile.loc[featuresFile['word'] == word]
        tmp_str_emo = ""
        tmp_str_neu = ""

        for k in name_rows.index:

            translated_feat = re.sub(r'\s*\+\s*', ', ', featuresFile['features'][k])

            if str(name_rows["emotionality"][k]) == "emo":

                tmp_str_emo = tmp_str_emo + ", " + translated_feat

            if str(name_rows["emotionality"][k]) == "neu":

                tmp_str_neu = tmp_str_neu + ", " + translated_feat

        assoziationen.append(tmp_str_emo.replace(', ', '', 1))
        assoziationen.append(tmp_str_neu.replace(', ', '', 1))
    #filename = config['load_paths']['ZeroShotMultiLabelChain']
    filename = "zero_shot_AllProbandsOneWord.json"

    return assoziationen, filename



def getAssociationsSplitted(featuresFile):
    """
    This function takes the FeaturesFile with all the data
    and returns the splitted association chains from this file together with the filename.

    Parameters:
    -----------
    featuresFile : pd.DataFrame
       Contains the data with the associations.
   
    
    Returns:
    --------
    assoziationen : list
        Contains all splitted association chains.
    filename : str
        Contains filename.
    """
    assoziationen = set()
    #avglen = 0

    for i in range(len(featuresFile)):

        tmp = featuresFile['features'][i].split("+")
        #avglen += len(tmp)

        for j in tmp:

            assoziationen.add(j.strip())
    #print(avglen/len(featuresFile))

    assoziationen = list(assoziationen)
    filename = config['PATHS']['ZeroShotMultiLabelSplitted']

    return assoziationen, filename



def getDefinitions(definitionsFile):
    """
    This function takes the DefinitionsFile with the definitions 
    of the Pseudowörter and returns the definitions.

    Parameters:
    -----------
    definitionsFile : pd.DataFrame
       Contains the definitions of the Pseudowörter.
   
    
    Returns:
    --------
    defini : list
        Contains all definitions.
    """
    defini = []

    for m in range(len(definitionsFile)):

        defini.append(definitionsFile["Konzept "][m])
        defini.append(definitionsFile["N_Konzept"][m])
    
    return defini



def zeroShotClassification(defini, assoziationen):
    """
    This function takes the definitions and associations
    and passes them to the classifier.
    Parameters:
    -----------
    defini : list
       Contains the definitions.
    assoziationen : list
       Contins the associations.
   
    
    Returns:
    --------
    Returns the zeroshot output of the model.
    """
    classifier = pipeline("zero-shot-classification", model="facebook/bart-base", multi_label=True)  # model="bert-base-german-cased"

    #return classifier(defini, candidate_labels=assoziationen)
    return classifier(assoziationen, candidate_labels=defini)




def  writeToFile(result, filename):
    """
    This function takes the output of the zeroshot model and 
    writes it into a json- file.

    Parameters:
    -----------
    result : 
       Contains the output of the classifier.
   
    
    Returns:
    --------
    -
    """
    with open(filename, "w") as fout:
        json.dump(result, fout)





if __name__ == "__main__":

    featuresFile = pd.read_csv(config['PATHS']['TranslatednewData'], sep='\t', usecols=[1, 2, 3, 4, 5, 6], encoding="utf-8")   # HIER CONFIG EINFÜGEN
    definitionsFile = pd.read_csv(config['PATHS']['TranslatedDefinitions'], sep='\t', usecols=[1,2,3], encoding='utf-8')

    #associations, filename = getAssociationChain(featuresFile)
    associations, filename = getAssociationChainOfOneWord(featuresFile)
    #associations, filename = getAssociationsSplitted(featuresFile)
    definitions = getDefinitions(definitionsFile)

    writeToFile(zeroShotClassification(definitions, associations), filename)