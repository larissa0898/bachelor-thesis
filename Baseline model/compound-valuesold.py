import csv
import statistics

situation_emo = open("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\stimuli_resultate_emotional.tsv")
situation_neu = open("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\stimuli_resultate_neutral.tsv")


read_tsv = csv.reader(situation_emo, delimiter="\t")
read_tsv2 = csv.reader(situation_neu, delimiter="\t")
comp_val = []

for row in read_tsv:

    if row == []:
        row = row
    else:
        comp_val.append(eval(row[2]).get("compound"))


for row in read_tsv2:

    if row == []:
        row = row
    else:
        comp_val.append(eval(row[2]).get("compound"))


comp_val.sort()
negativ = []
positiv = []


for el in comp_val:

    if el < 0:
        negativ.append(el)
    elif el > 0:
        positiv.append(el)


# METHODE 3

""" length = int(len(negativ)/2)
new = statistics.median(negativ)
print(new)
#print(negativ[length]) """

""" print(negativ)
print("-------------------------------------------------------")
print(positiv) """

""" length2 = int(len(positiv)/2)
new = statistics.median(positiv)
print(new)
#print(positiv[length]) """



#### METHODE 2
#comp_val.sort()
#print(comp_val)
length = int(len(comp_val)/2)
new = statistics.median(comp_val)
print(new)
print(comp_val[length])

print("---------------------------------------------------")
print(statistics.median(comp_val[:length]))
print(statistics.median(comp_val[length:]))