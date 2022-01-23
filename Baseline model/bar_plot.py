import numpy as np
import matplotlib.pyplot as plt

""" # Make a random dataset:
height = [334, 653, 643, 323]
bars = ('Neutral Richtig', 'Emotional Richtig', 'Neutral Falsch', 'Emotional Falsch')
y_pos = np.arange(len(bars))

# Create bars
plt.bar(y_pos, height, color=['green', 'green', 'red', 'red'])

# Create names on the x-axis
plt.xticks(y_pos, bars)

# Show graphic
plt.show() """



""" #import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = ('Emotional Richtig', 'Emotional Falsch')
sizes = [653, 323]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show() """



# Make a random dataset:
height = [127, 23]
bars = ('Richtig', 'Falsch')
y_pos = np.arange(len(bars))

# Create bars
plt.bar(y_pos, height, color=['black', 'grey'])

# Create names on the x-axis
plt.xticks(y_pos, bars)

# Show graphic
plt.show() 