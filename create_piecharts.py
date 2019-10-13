import init_and_prepare as iap
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# inicjalizacja danych
init_data = iap.InitAndPrepare()
df = init_data.prepare_data_flights()
airlines_names = init_data.prepare_data_airlines()

# Utworzenie dataframe ze podstawowymi statystykami dla kazdej z linii lotniczych
airlines_stats = df['DEPARTURE_DELAY'].groupby(df['AIRLINE']).apply(init_data.get_statistics).unstack()
airlines_stats = airlines_stats.sort_values('ilosc_wierszy')
print(airlines_stats)

# Zapisanie kodow linii lotniczych do slownika
airlines_abbrev = airlines_names.set_index('IATA_CODE')['AIRLINE'].to_dict()

# ################################# WYKRES - RYS 17 ####################################################################
# Wykres statystyk
font = {'family': 'serif',
        'weight': 'bold',
        'size': 16}
mpl.rc('font', **font)

# Wyciagniecie 2 kolumn airline i departure_delay do nowego dataframe; podmiana nazw linii na slownikowy
dtframe2 = df.loc[:, ['AIRLINE', 'DEPARTURE_DELAY']]
dtframe2['AIRLINE'] = dtframe2['AIRLINE'].replace(airlines_abbrev)

# Zdefiniowanie kolorow do wykresu
colors = ['lavender', 'darkgrey', 'orange', 'cyan', 'red', 'green', 'lightblue',
          'lightgrey', 'lightgreen', 'gold', 'brown', 'violet', 'indigo', 'pink']

# Budowanie obrazu
fig = plt.figure(1, figsize=(22, 16))
grdspec = GridSpec(2, 2)
axis1 = fig.add_subplot(grdspec[0, 0])
axis2 = fig.add_subplot(grdspec[0, 1])
axis3 = fig.add_subplot(grdspec[1, :])

# Diagram kołowy 1 - ilosc lotow per linia lotnicza
lbls = [i for i in airlines_stats.index]
siz = airlines_stats['ilosc_wierszy'].values
explode = [0.3 if siz[i] < 20000 else 0.0 for i in range(len(airlines_abbrev))]
patches, txt, autotxt = axis1.pie(siz,
                                  explode=explode, labels=lbls,
                                  colors=colors, autopct='%1.0f%%',
                                  shadow=False, startangle=0)
for i in range(len(airlines_abbrev)):
    txt[i].set_fontsize(15)
axis1.axis('equal')
axis1.set_title('% lotów per linia lotnicza', bbox={'facecolor': 'black', 'pad': 5}, color='white', fontsize=17)

# Ustawienie legendy w postaci "skrot : pelna nazwa linii
hnd = []
for i in range(len(airlines_abbrev)):
    hnd.append(mpatches.Patch(color=colors[i],
                              label=airlines_stats.index[i] + ': ' + airlines_abbrev[airlines_stats.index[i]]))
axis1.legend(handles=hnd, bbox_to_anchor=(0.2, 0.9), fontsize=14, bbox_transform=plt.gcf().transFigure)

# Diagram kołowy 2 - średnie opóźnienie przy wylocie
siz = airlines_stats['srednia'].values
siz = [max(i, 0) for i in siz]
explode = [0.0 if siz[i] < 20000 else 0.01 for i in range(len(airlines_abbrev))]
patches, txt, autotxt = axis2.pie(siz, explode=explode, labels=lbls,
                                  colors=colors, shadow=False,
                                  startangle=0, autopct=lambda x:  '{:.0f}'.format(x*sum(siz)/100))
for i in range(len(airlines_abbrev)):
    txt[i].set_fontsize(14)
axis2.axis('equal')
axis2.set_title('średnie opóźnienie przy wylocie [min]', bbox={'facecolor': 'black', 'pad': 5},
                color='white', fontsize=17)

# Wykres striplot ze wszystkimi opóźnieniami skategoryzowanymi wg linii lotniczej
axis3 = sns.stripplot(y="AIRLINE", x="DEPARTURE_DELAY", size=4, palette=colors, data=dtframe2, linewidth=0.5,
                      jitter=True)
plt.setp(axis3.get_xticklabels(), fontsize=15)
plt.setp(axis3.get_yticklabels(), fontsize=15)
# formatowanie wartości osi x do postaci HHhMMm
axis3.set_xticklabels(['{:2.0f}h{:2.0f}m'.format(*[int(y) for y in divmod(x, 60)]) for x in axis3.get_xticks()])
plt.xlabel('Opóźnienie wylotu', fontsize=17, bbox={'facecolor': 'black', 'pad': 5}, color='white', labelpad=20)
axis3.yaxis.label.set_visible(False)
plt.tight_layout(w_pad=3)

# Zapis wykresu do pliku
plt.savefig("1new.png")

# Zamknięcie połącznia
init_data.close_connection()
