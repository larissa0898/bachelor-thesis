import pandas as pd
from deep_translator import GoogleTranslator
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')


def loadData():
    stimuliEmo = pd.read_excel(config['PATHS']['stimuli_emo'], usecols=[0,2,3,4,5,6])
    stimuliNeu = pd.read_excel(config['PATHS']['stimuli_neu'], usecols=[0,2,3,4,5,6])

    return stimuliEmo, stimuliNeu


def saveDataToFile(finallist, columns, filename):
    df = pd.DataFrame(finallist, columns=columns)

    df.to_csv(config['PATHS'][filename], sep='\t', encoding='utf-8')


def translateStimuli(stimuliEmo, stimuliNeu):
    finallist = []

    for i in range(len(stimuliNeu["Pseudwort"])):

        for j in range(1,6): 

            text = GoogleTranslator(source='auto', target='en').translate(str(stimuliNeu[f'Situation neutral {j}'][i]))
            finallist.append([stimuliNeu['Pseudwort'][i], 'neu', text]) 


            text = GoogleTranslator(source='auto', target='en').translate(str(stimuliEmo[f'Situation emotional {j}'][i]))
            finallist.append([stimuliEmo['Pseudowort'][i], 'emo', text])

    return finallist, ['Wort', 'Emotionalität', 'Situation'], 'TranslatedSituations'



if __name__ == '__main__':
    
    stimuliEmo, stimuliNeu = loadData()
    finallist, columns, filename = translateStimuli(stimuliEmo, stimuliNeu)
    saveDataToFile(finallist, columns, filename)