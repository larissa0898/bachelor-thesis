from transformers import pipeline
#from transformers import BertTokenizer
#from transformers import AutoTokenizer, AutoModelForMaskedLM
import pandas as pd
import re
import json
from deep_translator import GoogleTranslator



# zero shot classification + writing results to json
#features = pd.read_csv("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Features_clean.csv", sep=';', usecols=[2,3,7], encoding="latin-1")
features = pd.read_csv("newData.csv", sep='\t', usecols=[4, 6], encoding="utf-8")   # HIER CONFIG EINFÜGEN
#definitions = pd.read_excel("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Rating_Definitionen.xlsx", usecols=[0,1,8])
defi = set()

assoziationen = []
#defini = []
for i in range(len(features)):

    #if str(features['features'][i]) != "nan" and str(features['features'][i]) != "Fail" and str(features['features'][i]) != ",":

    translated_feat = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', features['features'][i]))
    translated_definition = GoogleTranslator(source='auto', target='en').translate(features["definition"][i])

    assoziationen.append(translated_feat)
    defi.add(translated_definition)

defi = list(defi)
""" for i in range(len(definitions)):
    translated_emo = GoogleTranslator(source='auto', target='en').translate(definitions["Konzept "][i])
    translated_neu = GoogleTranslator(source='auto', target='en').translate(definitions["N_Konzept"][i])
    defini.append(translated_emo)
    defini.append(translated_neu) """

with open("translated_asso.txt", "w") as fout:    # HIER CONFIG EINFÜGEN
    json.dump(assoziationen, fout)

with open("translated_def.txt", "w") as f2out:     # HIER CONFIG EINFÜGEN
    json.dump(defi, f2out)


f = open("translated_def.txt")   # HIER CONFIG EINFÜGEN
f2 = open("translated_asso.txt")   # HIER CONFIG EINFÜGEN


data = json.load(f)
data2 = json.load(f2)


defini = []
assoziationen = []

for i in data:
    defini.append(i)

for j in data2:
    assoziationen.append(j)


classifier = pipeline("zero-shot-classification", model="facebook/bart-base", multi_label=True)  # model="bert-base-german-cased"
result = classifier(defini, candidate_labels=assoziationen)


with open("zero_shot_english_MultiLabel.txt", "w") as fout:    # HIER CONFIG EINFÜGEN
    json.dump(result, fout)
