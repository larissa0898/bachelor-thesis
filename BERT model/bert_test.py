from transformers import pipeline
from transformers import BertTokenizer
from transformers import AutoTokenizer, AutoModelForMaskedLM
import pandas as pd
import re
import json
from deep_translator import GoogleTranslator


# getting text of result
""" tokenizer = BertTokenizer.from_pretrained('bert-base-german-cased')
MASK_TOKEN = tokenizer.mask_token

bert_mask = pipeline("fill-mask", model="bert-base-german-cased")
results = bert_mask("Er arbeitet dort seit langer {}.".format(MASK_TOKEN), top_k=2)
print(results) """


# getting tensor of result
""" tokenizer = AutoTokenizer.from_pretrained('bert-base-german-cased')
model = AutoModelForMaskedLM.from_pretrained("bert-base-german-cased")
MASK_TOKEN = tokenizer.mask_token

sent = "Er arbeitet dort seit langer {}.".format(MASK_TOKEN)
tok = tokenizer(sent, return_tensors='pt')

results = model(**tok)
print(results) """



# zero shot classification + writing results to json
""" features = pd.read_csv("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Features_clean.csv", sep=';', usecols=[2,3,7], encoding="latin-1")
definitions = pd.read_excel("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Rating_Definitionen.xlsx", usecols=[0,1,8])


assoziationen = []
defini = []
for i in range(len(features)):
    if str(features['features'][i]) != "nan" and str(features['features'][i]) != "Fail" and str(features['features'][i]) != ",":
        func
        translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))
        assoziationen.append(translated_asso)

print("DONE")

for i in range(len(definitions)):
    translated_emo = GoogleTranslator(source='auto', target='en').translate(definitions["Konzept "][i])
    translated_neu = GoogleTranslator(source='auto', target='en').translate(definitions["N_Konzept"][i])
    defini.append(translated_emo)
    defini.append(translated_neu)

with open("translated_asso.txt", "w") as fout:
    json.dump(assoziationen, fout)

with open("translated_def.txt", "w") as f2out:
    json.dump(defini, f2out) """


f = open("translated_def.txt")
f2 = open("translated_asso.txt")


data = json.load(f)
data2 = json.load(f2)


defini = []
assoziationen = []

for i in data:
    defini.append(i)

for j in data2:
    assoziationen.append(j)

print("PHASE 1: DONE")

classifier = pipeline("zero-shot-classification", function_to_apply="none")  # model="bert-base-german-cased"
result = classifier(defini, candidate_labels=assoziationen)

print("PHASE 2: DONE")

with open("zero_shot_english_withoutSoftmax.txt", "w") as fout:
    json.dump(result, fout)

print("PHASE 3: DONE")

""" classifier = pipeline("zero-shot-classification")# , model="distilbert-base-german-cased"
result = classifier("The president travels to France.", candidate_labels=["tourism","politics","abroad","computer","education"])
print(result) """
