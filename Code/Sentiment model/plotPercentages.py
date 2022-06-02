import numpy as np
import matplotlib.pyplot as plt

""" # Make a random dataset:
height = [68.75, 33.27]
bars = ('emotional', 'neutral')
x_pos = [0,0.5]
width = [0.3, 0.3]
# Create bars
bar = plt.bar(x_pos, height,color=['darkgrey', 'lightblue'], width=width)
plt.ylabel('Anzahl korrekt erkannter emotionaler/neutraler Features in %')
plt.ylim([0,100])

# Create names on the x-axis
plt.xticks(x_pos, bars)

# Add counts above the two bar graphs
i = 0
te = ['68.75', '33.27']
for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{te[i]}%', ha='center', va='bottom')
    i+=1


# Show graphic
plt.show() """


import matplotlib.pyplot as plt


""" labels = ['emotional', 'neutral']
#men_means = [671, 325]
#women_means = [305, 652]
men_means = [107, 130]
women_means = [43, 20]

width = 0.45       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots()

ax.bar(labels, men_means, width, label='korrekt erkannt', color='darkgrey')
ax.bar(labels, women_means, width, bottom=men_means,
       label='falsch erkannt', color='lightblue')

ax.set_ylabel('Anzahl emotionaler/neutraler Situationsbeschreibungen')
#ax.set_ylabel('Anzahl emotionaler/neutraler Feature')
plt.ylim([0,300])
#plt.ylim([0,2000])
ax.legend()

plt.show() """



labels = ['gesamt']
men_means = [127]
women_means = [173]
#men_means = [1323]
#women_means = [630]
#men_std = [1, 0.5, 1.3]
#women_std = [2, 2, 4]
width = 0.01       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots()

ax.bar(labels, men_means, width=0.1, label='emotional erkannt', color='darkgrey')
ax.bar(labels, women_means, width=0.1, bottom=men_means,
       label='neutral erkannt', color='palegreen')

ax.set_ylabel('Anzahl emotionaler/neutraler Situationsbeschreibungen')
plt.ylim([0,350])
#ax.set_ylabel('Anzahl emotionaler/neutraler Feature')
#plt.ylim([0,2500])
ax.legend()

plt.show()