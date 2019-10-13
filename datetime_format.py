import pandas as pd
import datetime
import numpy as np


# Funkcja konwertujaca string w postaci 'HHMM' do formatu datetime.time
def convert_to_time(strn):
    if pd.isnull(strn):
        return np.nan
    else:
        if strn == 2400:
            strn = 0
        strn = "{0:04d}".format(int(strn))
        vtime = datetime.time(int(strn[0:2]), int(strn[2:4]))
        return vtime


# Funkcja przeksztalcajaca date i czas do formatu datetime.datetime
def convert_to_date_time(x):
    if pd.isnull(x[0]) or pd.isnull(x[1]):
        return np.nan
    else:
        return datetime.datetime.combine(x[0], x[1])


# Funkcja laczaca dwie kolumny z dataframe i przekstalcajaca do formatu datetime
def merge_dfcol_to_flight_time(dframe, coll):
    lst = []
    for index, colls in dframe[['DATE', coll]].iterrows():
        if pd.isnull(colls[1]):
            lst.append(np.nan)
        elif float(colls[1]) == 2400:
            colls[0] += datetime.timedelta(days=1)
            colls[1] = datetime.time(0, 0)
            lst.append(convert_to_date_time(colls))
        else:
            colls[1] = convert_to_time(colls[1])
            lst.append(convert_to_date_time(colls))
    return pd.Series(lst)