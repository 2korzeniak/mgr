import init_and_prepare as iap
import matplotlib as mpl
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

# ################################ WYKRES - RYS 21 #####################################################################
mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams['hatch.linewidth'] = 2.0
fig = plt.figure(1, figsize=(13, 6))
axs1 = sns.barplot(x="DEPARTURE_DELAY", y="AIRLINE", data=df, color="lightgreen", ci=None)
axs1 = sns.barplot(x="ARRIVAL_DELAY", y="AIRLINE", data=df, color="black", hatch='//', alpha=0.0, ci=None)
lbls = [airlines_abbrev[item.get_text()] for item in axs1.get_yticklabels()]
axs1.set_yticklabels(lbls)
axs1.yaxis.label.set_visible(False)
plt.xlabel('Średnie opóźnienie [min] (wylot: kolor zielony, przylot: czarne paski)', fontsize=14, weight='bold',
           labelpad=10)
plt.tight_layout()

# zapis do pliku
plt.savefig("5new.png")
