import init_and_prepare as iap
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import ConnectionPatch
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np
import warnings
warnings.filterwarnings("ignore")


# ######################################### Funkcje pomocnicze #########################################################
# dopasowanie eksponencjalne
def func_exp(x, a, b):
    return a * np.exp(-x / b)
# ######################################################################################################################


# inicjalizacja danych
init_data = iap.InitAndPrepare()
df = init_data.prepare_data_flights()
airlines_names = init_data.prepare_data_airlines()

# Zapisanie kodow linii lotniczych do slownika
airlines_abbrev = airlines_names.set_index('IATA_CODE')['AIRLINE'].to_dict()

# Utworzenie dataframe ze podstawowymi statystykami dla kazdej z linii lotniczych
airlines_stats = df['DEPARTURE_DELAY'].groupby(df['AIRLINE']).apply(init_data.get_statistics).unstack()
airlines_stats = airlines_stats.sort_values('ilosc_wierszy')

# Wyciagniecie 2 kolumn airline i departure_delay do nowego dataframe; podmiana nazw linii na slownikowy
dtframe2 = df.loc[:, ['AIRLINE', 'DEPARTURE_DELAY']]
dtframe2['AIRLINE'] = dtframe2['AIRLINE'].replace(airlines_abbrev)

# ################################ WYKRES - RYS 19-20 ##################################################################
lbl_company = []
pts = []
fig = plt.figure(1, figsize=(12, 12))
i = 0
for n_carrier in [airlines_abbrev[x] for x in airlines_stats.index]:
    i += 1
    ax = fig.add_subplot(5, 3, i)
    # histogram z linią dopasowania
    n, bins, patches = plt.hist(x=dtframe2[dtframe2['AIRLINE'] == n_carrier]['DEPARTURE_DELAY'], range=(15, 180),
                                normed=True, bins=60)
    cbin = bins[:-1] + 0.5 * (bins[1:] - bins[:-1])
    popt, pcov = curve_fit(func_exp, cbin, n, p0=[1, 2])
    pts.append(popt)
    lbl_company.append(n_carrier)
    # rysowanie liniii dopasowania
    plt.plot(cbin, func_exp(cbin, *popt), 'r-', linewidth=3)
    # zdefiniowanie labelek
    if i < 10:
        ax.set_xticklabels(['' for x in ax.get_xticks()])
    else:
        ax.set_xticklabels(['{:2.0f}h{:2.0f}m'.format(*[int(y) for y in divmod(x, 60)]) for x in ax.get_xticks()])

    # ustawienie tytułu
    plt.title(n_carrier, fontsize=10, fontweight='bold', color='darkred')
    if i == 4:
        ax.text(-0.3, 0.9, 'Znormalizowana ilość lotów', fontsize=15, rotation=90, color='black',
                horizontalalignment='center', transform=ax.transAxes)
    if i == 14:
        ax.text(0.5, -0.5, 'Opóźnienie wylotu', fontsize=15, rotation=0, color='black', horizontalalignment='center',
                transform=ax.transAxes)

    # ustawienie legendy i wyświetlenie wartości parametrów a i b
    ax.text(0.68, 0.7, 'a = {}\nb = {}'.format(round(popt[0], 2), round(popt[1], 1)), style='italic',
            transform=ax.transAxes, fontsize=12, family='serif', bbox={'facecolor': 'lightgrey', 'alpha': 0.8, 'pad': 5})

# zapis do pliku i czyszczenie
plt.tight_layout()
plt.savefig("3new.png")
plt.clf()
plt.cla()
plt.close()

# wykres 20
mpl.rcParams.update(mpl.rcParamsDefault)
sns.set_context('paper')
fig = plt.figure(1, figsize=(12, 8))
x_val = [s[1] for s in pts]
y_val = [s[0] for s in pts]
y_shft = [0 for _ in range(14)]
y_shft[3] = 0.5 / 1000
y_shft[12] = 2.5 / 1000
y_shft[11] = -0.5 / 1000
y_shft[8] = -2.5 / 1000
y_shft[5] = 1 / 1000
gspace = GridSpec(2, 7)

# ranking: lewa część
axs1 = fig.add_subplot(gspace[1, 0:2])
plt.scatter(x=x_val, y=y_val, marker='D', edgecolor='red', linewidth='1')
# Linia Hawaiian Airlines
i = 1
axs1.annotate(lbl_company[i], xy=(x_val[i] + 1.5, y_val[i] + y_shft[i]), xycoords='data', fontsize=10)
plt.xlabel("parametr $b$", fontsize=16,labelpad=20)
plt.ylabel("parametr $a$", fontsize=16, labelpad=20)

# Linia Delta Airlines
i = 12
axs1.annotate(lbl_company[i], xy=(x_val[i] + 1.5, y_val[i] + y_shft[i]), xycoords='data', fontsize=10)
plt.xlabel("parametr $b$", fontsize=16, labelpad=20)
plt.ylabel("parametr $a$", fontsize=16, labelpad=20)

# Ustawienie tytułu
axs1.text(.5, 1.5, 'Ranking opóźnień\n wg linii lotniczych', fontsize=16,
          bbox={'facecolor': 'lightgray', 'pad': 5}, color='black',
          horizontalalignment='center',
          transform=axs1.transAxes)
# obramowanie
for k in ['top', 'bottom', 'right', 'left']:
    axs1.spines[k].set_visible(True)
    axs1.spines[k].set_linewidth(0.5)
    axs1.spines[k].set_color('black')

# prostokąt z przerywaną linią
rectangle = mpatches.Rectangle((21, 0.025), 19, 0.07, linewidth=2, edgecolor='darkblue', linestyle='-.',
                               facecolor='none')
axs1.add_patch(rectangle)

# ranking: prawa część (przybliżenie)
axs2 = fig.add_subplot(gspace[0:2, 2:])
plt.scatter(x=x_val, y=y_val, marker='D', edgecolor='red', linewidth='1')
plt.setp(axs1.get_xticklabels(), fontsize=12)
plt.setp(axs1.get_yticklabels(), fontsize=12)
axs2.set_xlim(21, 45)
axs2.set_ylim(0.025, 0.095)

# Nazwy linii lotniczych
for i in range(len(airlines_abbrev)):
    axs2.annotate(lbl_company[i], xy=(x_val[i] + 0.5, y_val[i] + y_shft[i]), xycoords='data', fontsize=10)

# strzałka z kierunkiem wzrostu opóźnień
axs2.arrow(30, 0.09, 8, -0.03, head_width=0.005, shape='full', head_length=2, fc='darkgrey', ec='darkgrey')
axs2.annotate('wzrost \n  opóźnienia', fontsize=20, color='darkgrey', xy=(35, 0.075), xycoords='data')
plt.tick_params(labelleft=False, labelright=True)
plt.setp(axs2.get_xticklabels(), fontsize=14)
plt.setp(axs2.get_yticklabels(), fontsize=14)
for k in ['top', 'bottom', 'right', 'left']:
    axs2.spines[k].set_visible(True)
    axs2.spines[k].set_linewidth(0.5)
    axs2.spines[k].set_color('black')

# Połączenie pomiędzy dwoma wykresami
xy2 = (40, 0.09)
xy1 = (21, 0.095)
con = ConnectionPatch(xyA=xy1, xyB=xy2, coordsA="data", coordsB="data", axesA=axs2, axesB=axs1, linestyle='-.',
                      linewidth=2, color="darkblue")
axs2.add_artist(con)
xy2 = (40, 0.025)
xy1 = (21, 0.025)
con = ConnectionPatch(xyA=xy1, xyB=xy2, coordsA="data", coordsB="data", axesA=axs2, axesB=axs1, linestyle='-.',
                      linewidth=2, color="darkblue")
axs2.add_artist(con)
plt.xlabel("parametr $b$", fontsize=16, labelpad=20)

#zapis do pliku
plt.savefig("4new.png")
