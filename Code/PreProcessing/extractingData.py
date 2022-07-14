import re
import pandas as pd
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def loadDataframe():
    features = pd.read_csv(config['PATHS']['FeaturesClean'], sep=';', usecols=[0,2,3,5,7], encoding="latin-1")
    definitions = pd.read_excel(config['PATHS']['RatingDefinitionen'], usecols=[0,1,8])
    return features, definitions



def getDefinitions(emotionality, definitionsFile, featuresWord, definition):
    if emotionality == 'emo':

        nameRowsEmo = definitionsFile.loc[definitionsFile['Name'] == featuresWord]
        definition.append(definitionsFile['Konzept '][nameRowsEmo.index[0]])

    else: 

        nameRowsNeu = definitionsFile.loc[definitionsFile['Name'] == featuresWord]
        definition.append(definitionsFile['N_Konzept'][nameRowsNeu.index[0]])
        
    return definition



def cleanFeatures(featuresFile, definitionsFile):
    vpCode = []
    word = []
    emotionality = []
    group = []
    features = []
    definitions = []

    for i in range(len(featuresFile)):

        if str(featuresFile['features'][i]) != "nan" and str(featuresFile['features'][i]) != "Fail" and str(featuresFile['features'][i]) != ",":

            clean_association = re.sub(r'\s*\+\s*', ' + ', featuresFile['features'][i])

            vpCode.append(featuresFile['VP_Code'][i])
            word.append(featuresFile['word'][i])
            emotionality.append(featuresFile['emotionality'][i])
            group.append(featuresFile['group'][i])
            features.append(clean_association)
            
            definitions = getDefinitions(featuresFile['emotionality'][i], definitionsFile, featuresFile['word'][i], definition=definitions)

    return vpCode, word, emotionality, definitions, group, features


def createFinallist(vpCode, word, emotionality, definitions, group, features):
    finallist = []

    for i in range(len(vpCode)):

        finallist.append([vpCode[i], word[i], emotionality[i], definitions[i], group[i], features[i]])
    
    return finallist, ['VP_Code', 'word', 'emotionality', 'definition', 'group', 'features'], 'newData'


def saveData(finallist,columns,filename):
    df = pd.DataFrame(finallist, columns=columns)

    df.to_csv(config['PATHS'][filename], sep='\t', encoding='utf-8')
