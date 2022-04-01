from transformers import pipeline
import pandas as pd
from deep_translator import GoogleTranslator
from configparser import ConfigParser
import json
import re


config = ConfigParser()
config.read('config.ini')

definitions = pd.read_excel(config['load_paths']['filepath_definitions'], usecols=[0,1,8])


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
    generator = pipeline("text-generation")

    #for j in range(1,2):

    for i in range(len(definitions["Name"])):

        text_emo = GoogleTranslator(source='auto', target='en').translate(str(definitions["Name"][i]) + " is " + str(definitions["Konzept "][i]) + " and when I think of it, I associate it with")
        text_neu = GoogleTranslator(source='auto', target='en').translate(str(definitions["Name"][i]) + " is " + str(definitions["N_Konzept"][i]) + " and when I think of it, I associate it with")

        generated_text.append({str(definitions['Name'][i]) + ", emotional": generator(text_emo)})
        generated_text.append({str(definitions['Name'][i]) + ", neutral": generator(text_neu)})


    with open("generated_en.txt", "w") as fout:  # HIER CONFIG EINSETZEN
        json.dump(generated_text, fout)




def generating_german_features(definitions):
    """
    This function takes the definition of a "Pseudowort", 
    generates German features with the text-generation pipeline from transformers and 
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
    generator = pipeline("text-generation", model="dbmdz/german-gpt2")

    #for j in range(1,2):

    for i in range(len(definitions["Name"])):

        #text_emo = str(definitions["Name"][i]) + " ist " + str(definitions["Konzept "][i]) + " und wenn ich daran denke, assoziiere ich es mit"
        text_emo = re.sub("\.", "", str(definitions["Konzept "][i]))
        lower_emo = text_emo[0].lower() + text_emo[1:]
        #text_neu = str(definitions["Name"][i]) + " ist " + str(definitions["N_Konzept"][i]) + " und wenn ich daran denke, assoziiere ich es mit"
        text_neu = re.sub("\.", "", str(definitions["N_Konzept"][i]))
        lower_neu = text_neu[0].lower() + text_neu[1:]

        generated_text.append({str(definitions['Name'][i]) + ", emotional": generator(str(definitions["Name"][i]) + " ist " + lower_emo + " und wenn ich daran denke, assoziiere ich es mit",
                                                                                            max_length=120,
                                                                                            num_return_sequences=2,)[0]})
        generated_text.append({str(definitions['Name'][i]) + ", neutral": generator(str(definitions["Name"][i]) + " ist " + lower_neu + " und wenn ich daran denke, assoziiere ich es mit", 
                                                                                            max_length=120,
                                                                                            num_return_sequences=2,)[0]})


    with open("generated_de.txt", "w") as fout:   # HIER CONFIG EINFÜGEN
        json.dump(generated_text, fout)



generating_english_features(definitions)
generating_german_features(definitions)