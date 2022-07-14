from transformers import pipeline
import pandas as pd
from configparser import ConfigParser
import json
import re


config = ConfigParser()
config.read('config.ini')


def loadData():
    return  pd.read_csv(config['PATHS']['TranslatedDefinitions'], sep='\t', usecols=[1,2,3], encoding='utf-8')


def saveData(generatedText, filename):
    with open(config['PATHS'][filename], "w") as fout:
        json.dump(generatedText, fout)


def generatingEnglishFeatures(definitions):

    generatedText = []
    generator = pipeline("text-generation")

    for i in range(len(definitions["word"])):

        textEmo = str(definitions["word"][i]) + " is " + str(definitions["Konzept "][i]).replace('.', '') + " and when I think of it, I associate it with"
        textNeu = str(definitions["word"][i]) + " is " + str(definitions["N_Konzept"][i]).replace('.', '') + " and when I think of it, I associate it with"

        generatedText.append({str(definitions['word'][i]) + ", emotional": generator(textEmo, max_length=120, num_return_sequences=2)})
        generatedText.append({str(definitions['word'][i]) + ", neutral": generator(textNeu, max_length=120, num_return_sequences=2)})

    return generatedText, 'Generated'



def generatingMaskedEnglishFeatures(definitions):

    maskedFeatures = []
    unmasker = pipeline("fill-mask")

    for i in range(len(definitions["word"])):

        textEmo = str(definitions["word"][i]) + " is " + str(definitions["Konzept "][i]).replace('.', '') + " and when I think of it, I associate it with <mask>."
        textNeu = str(definitions["word"][i]) + " is " + str(definitions["N_Konzept"][i]).replace('.', '') + " and when I think of it, I associate it with <mask>."

        resultEMO = unmasker(textEmo, top_k=6)
        assoEMO = [list(dictionary.values())[2] for dictionary in resultEMO]
        maskedFeatures.append({str(definitions['word'][i]) + ", emotional": assoEMO})

        resultNEU = unmasker(textNeu, top_k=6)
        assoNEU = [list(dictionary.values())[2] for dictionary in resultNEU]
        maskedFeatures.append({str(definitions['word'][i]) + ", neutral": assoNEU})

    return maskedFeatures, 'unmaskedEn'



if __name__ == "__main__":
    generatedText, filename = generatingMaskedEnglishFeatures(loadData())
    saveData(generatedText, filename)