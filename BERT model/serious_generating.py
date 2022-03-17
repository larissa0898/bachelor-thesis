from transformers import pipeline
import pandas as pd
from deep_translator import GoogleTranslator
from configparser import ConfigParser
import re


config = ConfigParser()
config.read('config.ini')


definitions = pd.read_excel(config['load_paths']['filepath_definitions'], usecols=[0,1,8])

generated_text = []
generator = pipeline("text-generation")

for j in range(1,2):

    for i in range(len(definitions["Name"])):

        text_emo = GoogleTranslator(source='auto', target='en').translate(str(definitions["Name"][i]) + " is " + str(definitions["Konzept "][i]) + " and when I think of it, I associate it with")
        text_neu = GoogleTranslator(source='auto', target='en').translate(str(definitions["Name"][i]) + " is " + str(definitions["N_Konzept"][i]) + " and when I think of it, I associate it with")

        generated_text.append({str(definitions['Name'][i]) + ", emotional": generator(text_emo)})
        generated_text.append({str(definitions['Name'][i]) + ", neutral": generator(text_neu)})

print(generated_text[0])