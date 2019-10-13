import init_and_prepare as iap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# inicjalizacja danych
init_data = iap.InitAndPrepare()
df = init_data.prepare_data_flights()
airlines_names = init_data.prepare_data_airlines()
airports = init_data.prepare_data_airports()

# Zapisanie kodow linii lotniczych do slownika
airlines_abbrev = airlines_names.set_index('IATA_CODE')['AIRLINE'].to_dict()

# ################################ WYKRES - RYS 22 #####################################################################
airport_mean_delays = pd.DataFrame(pd.Series(df['ORIGIN_AIRPORT'].unique()))
airport_mean_delays.set_index(0, drop=True, inplace=True)
identify_airport = airports.set_index('IATA_CODE')['CITY'].to_dict()

for n_carrier in airlines_abbrev.keys():
    df1 = df[df['AIRLINE'] == n_carrier]
    test = df1['DEPARTURE_DELAY'].groupby(df['ORIGIN_AIRPORT']).apply(init_data.get_statistics).unstack()
    airport_mean_delays[n_carrier] = test.loc[:, 'srednia']

# przygotowanie wykresu mapy cieplnej
sns.set(context="paper")
fig = plt.figure(1, figsize=(12, 12))
# Lewa czesc
axs = fig.add_subplot(1, 2, 1)
subset = airport_mean_delays.iloc[:50, :].rename(columns=airlines_abbrev)
subset = subset.rename(index=identify_airport)
msk = subset.isnull()
sns.heatmap(subset, linewidths=0.01, cmap="Dark2", mask=msk, vmin=0, vmax=35)
plt.setp(axs.get_xticklabels(), fontsize=11, rotation=85)
axs.yaxis.label.set_visible(False)
# Prawa czesc
axs = fig.add_subplot(1, 2, 2)
subset = airport_mean_delays.iloc[50:100, :].rename(columns=airlines_abbrev)
subset = subset.rename(index=identify_airport)
msk = subset.isnull()
sns.heatmap(subset, linewidths=0.01, cmap="Dark2", mask=msk, vmin=0, vmax=35)
plt.setp(axs.get_xticklabels(), fontsize=11, rotation=85)
axs.yaxis.label.set_visible(False)
plt.tight_layout()

#zapis do pliku
plt.savefig("6new.png")