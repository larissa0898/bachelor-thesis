import pandas as pd
from deep_translator import GoogleTranslator
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')


stimuli = pd.read_excel(config['PATHS']['stimuli_emo'], usecols=[0,2,3,4,5,6])
stimuli_2 = pd.read_excel(config['PATHS']['stimuli_neu'], usecols=[0,2,3,4,5,6])

translated_situations = []
finallist = []

for j in range(1,6):    

    for i in range(len(stimuli_2["Pseudwort"])):

        text = GoogleTranslator(source='auto', target='en').translate(str(stimuli_2[f'Situation neutral {j}'][i]))
        translated_situations.append(text)

        finallist.append([stimuli_2['Pseudwort'][i], 'neu', text])  # append "translated_situations[m], ", if english version should be in output file


for k in range(1,6):

        for m in range(len(stimuli["Pseudowort"])):

            text = GoogleTranslator(source='auto', target='en').translate(str(stimuli[f'Situation emotional {k}'][m]))
            translated_situations.append(text)

            finallist.append([stimuli['Pseudowort'][m], 'emo', text]) #translated_situations[m],

df = pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Situation'])

df.to_csv(config['PATHS']['TranslatedSituations'], sep='\t', encoding='utf-8')