from transformers import pipeline
import json
from deep_translator import GoogleTranslator
import re
import pandas as pd


""" features = pd.read_csv("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\Features_clean.csv", sep=';', usecols=[2,3,7], encoding="latin-1")


assoziationen_neu = []
assoziationen_emo = []

for i in range(len(features)):
    if str(features['features'][i]) != "nan" and str(features['features'][i]) != "Fail" and str(features['features'][i]) != ",":
        clean = re.sub(r',', '', features['features'][i])
        translated_asso = GoogleTranslator(source='auto', target='en').translate(re.sub(r'\s*\+\s*', ', ', clean))
        if features["emotionality"][i] == "neu":
            assoziationen_neu.append(translated_asso)
        if features["emotionality"][i] == "neu":
            assoziationen_emo.append(translated_asso)
    print(i)

newlist= [assoziationen_emo, assoziationen_neu]
with open("translated_asso_split.txt", "w") as f2out:
    json.dump(newlist, f2out) """

assoziationen = open("translated_asso_split.txt")
assoziationen = json.load(assoziationen)

assoziationen_emo = assoziationen[0]
assoziationen_neu = assoziationen[1]

generated_neu = []
generated_emo = []


genAssofile = open("generated.txt")
genAsso = json.load(genAssofile)

regex = r'^(.*?)I associate it with'

for el in genAsso:

    if "emotional" in list(el.keys())[0]:
        value = el.get(list(el.keys())[0])
        genasso = re.sub(regex, '', value)
        generated_emo.append(genasso.split(".")[0])

    if "neutral" in list(el.keys())[0]:
        value = el.get(list(el.keys())[0])
        genasso = re.sub(regex, '', value)
        generated_neu.append(genasso.split(".")[0])

uni_chr_re = re.compile(r'\\u([a-fA-F0-9]{4})')

generated_neu_clean = []
generated_emo_clean = []

for ele in generated_emo:
    generated_emo_clean.append(uni_chr_re.sub(lambda m: chr(int(m.group(1), 16)), ele))

for ele2 in generated_neu:
    generated_neu_clean.append(uni_chr_re.sub(lambda m: chr(int(m.group(1), 16)), ele2))
    print(ele2)




print("PHASE 1: DONE")

classifier = pipeline("zero-shot-classification")  # model="bert-base-german-cased"
result = classifier(generated_neu_clean, candidate_labels=assoziationen_neu)

print("PHASE 2: DONE")

with open("zero_shot_english_generatedtext_neu.txt", "w") as fout:
    json.dump(result, fout)

print("PHASE 3: DONE")


print("JETZT EMOTIONAL")


print("PHASE 1: DONE")

classifier = pipeline("zero-shot-classification")  # model="bert-base-german-cased"
result = classifier(generated_emo_clean, candidate_labels=assoziationen_emo)

print("PHASE 2: DONE")

with open("zero_shot_english_generatedtext_emo.txt", "w") as fout:
    json.dump(result, fout)

print("PHASE 3: DONE")