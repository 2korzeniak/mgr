import init_and_prepare as iap
import custom_delay_plots as cdp
import datetime
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore")


# ######################################### Funkcje pomocnicze #########################################################
# dopasowanie kwadratowe
def func_sq(x, a, b, c):
    return a*x*x + b*x + c


def fct(x):
    return x.hour*3600+x.minute*60+x.second
# ######################################################################################################################


# inicjalizacja danych
init_data = iap.InitAndPrepare()
df = init_data.prepare_data_flights()
airlines_names = init_data.prepare_data_airlines()
airports = init_data.prepare_data_airports()

# ################################ WYKRES - RYS 23-24 ##################################################################
# WN = Southwest Airlines
n_carrier = 'WN'
# PHX = 5
# LAX = 8
airport_id = 5
origin_airport_lst = df[df['AIRLINE'] == n_carrier]['ORIGIN_AIRPORT'].unique()
# print(origin_airport_lst[airport_id])
dframe2 = df[(df['AIRLINE'] == n_carrier) & (df['ARRIVAL_DELAY'] > 0)
             & (df['ORIGIN_AIRPORT'] == origin_airport_lst[airport_id])]
dframe2.sort_values('SCHEDULED_DEPARTURE', inplace=True)
# print(df2.head(5))
fig = cdp.CustomDelayPlots(11, 5, 1, 1)
fig.update_position(0, 0)
fig.draw_custom_plot(dframe2['SCHEDULED_DEPARTURE'], dframe2['DEPARTURE_DELAY'], color='darkgreen', line_style='-')
# ustawienie osi i legendy
fig.def_style()
fig.set_xlabel('Data wylotu', fontsize=14)
fig.set_ylabel('Opóźnienie [min]', fontsize=14)
date_start = datetime.datetime(2015, 1, 1)
date_end = datetime.datetime(2015, 1, 15)
fig.set_xlim(date_start, date_end)
fig.set_ylim(-15, 260)
# zapis do pliku
fig.save_file("7phx.jpg")
# fig1.save_file("8lax.jpg")

# Wykres 24
dframe2['departure_hours'] = dframe2['SCHEDULED_DEPARTURE'].apply(lambda x: x.time())
tst = dframe2['DEPARTURE_DELAY'].groupby(dframe2['departure_hours']).apply(init_data.get_statistics).unstack()
xval = np.array([fct(s) for s in tst.index])
yval = tst['srednia']
popt, pcov = curve_fit(func_sq, xval, yval)
tst['fit'] = pd.Series(func_sq(xval, *popt), index=tst.index)
fig = cdp.CustomDelayPlots(8, 4, 1, 1)
fig.update_position(0, 0)
fig.draw_custom_plot_date(dframe2['departure_hours'], dframe2['DEPARTURE_DELAY'], markeredge=False, label='opóźnienia')
fig.draw_custom_plot(tst.index, tst['srednia'], color='darkgreen', line_style='--', line_width=2,
                     label='średnie opóźnienie')
fig.draw_custom_plot(tst.index, tst['fit'], color='r', line_style='-', line_width=3, label='fit')
# ustawienie osi i legendy
fig.def_style()
fig.draw_legend('upper left')
fig.set_xlabel('Czas wylotu', fontsize=14)
fig.set_ylabel('Opóźnienie [min]', fontsize=14)
fig.set_ylim(-15, 210)
# zapis do pliku
fig.save_file("9phx.jpg")
# fig1.save_file("10lax.jpg")
