import matplotlib.pyplot as plt

vals = [29.4905686378479, 0.01217, 0.040996074]
lbs = ['Input', 'Lógica do jogo', 'Output']

fig1, ax1 = plt.subplots(figsize=(20,10))
w,t,a = ax1.pie(vals, autopct='', startangle=0, rotatelabels=True)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.suptitle('Porcentagem de tempo gasto em processamento no cenário 2', fontsize=16)

ax1.legend(w, lbs,
title="Ingredients",
loc="center left",
bbox_to_anchor=(1, 0, 0.5, 1))


plt.show()
