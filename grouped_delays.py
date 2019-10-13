import init_and_prepare as iap
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# inicjalizacja danych
init_data = iap.InitAndPrepare()
df = init_data.prepare_data_flights()
airlines_names = init_data.prepare_data_airlines()

# Zapisanie kodow linii lotniczych do slownika
airlines_abbrev = airlines_names.set_index('IATA_CODE')['AIRLINE'].to_dict()

# ################################ WYKRES - RYS 18 #####################################################################
# Grupowanie opóźnień w odpowiednie zakresy
df['DELAY_LEVEL'] = df['DEPARTURE_DELAY'].apply(lambda x: ((0, 1)[x > 5], 2)[x > 45])

# Przygotowanie wykresu
fig = plt.figure(1, figsize=(10, 7))
ax = sns.countplot(y="AIRLINE", hue='DELAY_LEVEL', data=df)

# Zastapienie skrotow linii ich pelnymi nazwami, definiowanie etykiet osi
lbl = [airlines_abbrev[item.get_text()] for item in ax.get_yticklabels()]
ax.set_yticklabels(lbl)
plt.setp(ax.get_xticklabels(), fontsize=11, weight='normal', rotation=0)
plt.setp(ax.get_yticklabels(), fontsize=11, weight='bold', rotation=0)
ax.yaxis.label.set_visible(False)
plt.xlabel('Ilość lotów', fontsize=17, weight='bold', labelpad=10)

# Ustawianie legendy
leg = plt.legend()
leg.get_texts()[0].set_text('na czas (<5min)')
leg.get_texts()[1].set_text('małe opóźnienie (5 < t < 45min)')
leg.get_texts()[2].set_text('duże opóźnienie (>45min)')
plt.tight_layout()

# Zapis do pliku
plt.savefig("2new.png")