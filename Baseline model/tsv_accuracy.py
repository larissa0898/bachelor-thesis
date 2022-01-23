import csv

""" tsv_file = open("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\features_results.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")

neutral_richtig = 0
neutral_falsch = 0
emo_richtig = 0
emo_falsch = 0
gesamt = 1952

for row in read_tsv:
    if row == []:
        print("hi")
    else:
        if row[0] == "neu":
            if row[3] == "neutral":
                neutral_richtig +=1
            else:
                neutral_falsch += 1
        if row[0] == "emo":
            if row[3] == "emotional":
                emo_richtig += 1
            else:
                emo_falsch += 1
        

print("neutral_richtig: ", neutral_richtig)
print("neutral_falsch: ", neutral_falsch)
print("emo_richtig: ", emo_richtig)
print("emo_falsch: ", emo_falsch)

acc = 987 / gesamt * 100

print("Accuracy: ", acc) """


tsv_file = open("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\stimuli_resultate_emotional.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")

emo_richtig = 0
gesamt = 0

for row in read_tsv:
    if row == []:
        print("hi")
    else:
        if row[4] == "emotional":
            emo_richtig += 1
        gesamt += 1
        

print("emo_richtig: ", emo_richtig)
print("gesamt: ", gesamt)
acc = emo_richtig / gesamt * 100

print("Accuracy: ", acc)



""" tsv_file = open("C:\\Users\\laris\\Desktop\\Bachelorarbeit\\Daten\\stimuli_resultate_neutral.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")

neutral_richtig = 0
gesamt = 0

for row in read_tsv:
    if row == []:
        print("hi")
    else:
        if row[4] == "neutral":
            neutral_richtig += 1
        gesamt += 1
        

print("emo_richtig: ", neutral_richtig)
print("gesamt: ", gesamt)
acc = neutral_richtig / gesamt * 100

print("Accuracy: ", acc) """