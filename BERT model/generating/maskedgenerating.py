from transformers import pipeline
import pandas as pd
import re
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')



def generating_english_features(definitions):
    """
    This function takes the definition of a "Pseudowort", translates it into English, 
    generates English features with the text-generation pipeline from transformers and 
    returns a json file containing the a list of dictionaries with each "Pseudowort", 
    the related emotionality and the generated features.

    Parameters:
    -----------
    definitions : DataFrame
        Contains the relevant columns of the Rating_Definitionen.xlsx file with the definitions.
    
    Returns:
    --------
        Returns a json-file with each "Pseudowort", the related emotionality and the generated features.
    """

    generated_text = []
    unmasker = pipeline("fill-mask")

    for i in range(len(definitions["word"])):

        text_emo = str(definitions["word"][i]) + " is " + str(definitions["Konzept "][i]).replace('.', '') + " and when I think of it, I associate it with <mask>."
        text_neu = str(definitions["word"][i]) + " is " + str(definitions["N_Konzept"][i]).replace('.', '') + " and when I think of it, I associate it with <mask>."

        resultEMO = unmasker(text_emo, top_k=6)
        assoEMO = [list(dictionary.values())[2] for dictionary in resultEMO]
        generated_text.append({str(definitions['word'][i]) + ", emotional": assoEMO})

        resultNEU = unmasker(text_neu, top_k=6)
        assoNEU = [list(dictionary.values())[2] for dictionary in resultNEU]
        generated_text.append({str(definitions['word'][i]) + ", neutral": assoNEU})


    with open("unmasked_en.json", "w") as fout:  # HIER CONFIG EINSETZEN
        json.dump(generated_text, fout)



definitions =  pd.read_csv(config['load_paths']['filepath_feat'], sep='\t', usecols=[1,2,3], encoding='utf-8')

generating_english_features(definitions)
