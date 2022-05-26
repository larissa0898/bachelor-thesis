""" import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
langs = ['Methode 1', 'Methode 2', 'Methode 3']
students = [51.20327700972862, 51.45929339477726, 51.1520737327189]
ax.bar(langs,students, color="red")
plt.show()
 """

""" import numpy as np
import matplotlib.pyplot as plt
 
# create a dataset
height = [51.20327700972862, 51.45929339477726, 51.1520737327189]
bars = ('Methode 1', 'Methode 2', 'Methode 3')
x_pos = np.arange(len(bars))

# Create bars with different colors
plt.bar(x_pos, height, color='red')

# Create names on the x-axis
plt.xticks(x_pos, bars)

# Show graph
plt.show() """


""" import matplotlib.pyplot as plt
x = ['Methode 1', 'Methode 2', 'Methode 3']
y = [51.20327700972862, 51.45929339477726, 51.1520737327189]
plt.barh(x, y, color="black")
 
for index, value in enumerate(y):
    plt.text(value, index,
             str(value))
 
plt.show() """




""" import matplotlib.pyplot as plt
import math
x = ['Methode 1', 'Methode 2', 'Methode 3']
y = [51.20327700972862, 51.45929339477726, 51.1520737327189]
low = min(y)
high = max(y)
plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
plt.bar(x,y, width=0.9, color="black") 

for index, value in enumerate(y):
    plt.text(value, index,
             str(value))

plt.show() """



from turtle import color
import pandas as pd 
import matplotlib.pyplot as plt 

data=[["Methode 1", 76.0, 84.6666667],
      ["Methode 2", 79.3333333, 79.333333],
      ["Methode 3", 71.33333334, 86.666667],
     ]

df = pd.DataFrame(data, columns=["Methode","Emotional","Neutral"])
df.plot(x="Methode", y=["Emotional","Neutral"], kind="bar",figsize=(9,8), color=["brown", "grey"])
plt.show()