from ibmdbpy import IdaDataBase, IdaDataFrame
import datetime_format as dtf
import pandas as pd


class InitAndPrepare:
    def __init__(self):
        self.idadb = IdaDataBase(dsn="DASHDB",
                        uid="dash5264",
                        pwd="GSEvq__6f9wZ",
                        verbose=True)

    def print_table(self):
        print(self.idadb.show_tables())

    def close_connection(self):
        self.idadb.close()

    def init_dataframe(self, tablename):
        df = IdaDataFrame(self.idadb, tablename)
        return df

    def prepare_data_airlines(self):
        df = self.init_dataframe('AIRLINES').as_dataframe()
        return df

    def prepare_data_airports(self):
        df = self.init_dataframe('AIRLINES').as_dataframe()
        return df

    def prepare_data_flights(self):
        df = self.init_dataframe('FLIGHTS')

        # Wczytanie tabeli FLIGHTS do struktury dataframe, wraz z przefiltrowaniem po miesiącu
        # i interesujących nas kolumnach
        df = df[df['MONTH'] == 1]
        df = df[['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
                 'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'DEPARTURE_DELAY',
                 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME', 'ARRIVAL_DELAY',
                 'SCHEDULED_TIME', 'ELAPSED_TIME', 'YEAR', 'MONTH', 'DAY']].as_dataframe()

        # Konsolidacja kolumn YEAR, MONTH, DAY do DATE
        df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']])
        variables_to_remove = ['YEAR', 'MONTH', 'DAY']
        df.drop(variables_to_remove, axis=1, inplace=True)

        # Operacje konwersji kolumn do odpowiednich formatow czasowych
        df['SCHEDULED_DEPARTURE'] = dtf.merge_dfcol_to_flight_time(df, 'SCHEDULED_DEPARTURE')
        df['DEPARTURE_TIME'] = df['DEPARTURE_TIME'].apply(dtf.convert_to_time)
        df['SCHEDULED_ARRIVAL'] = df['SCHEDULED_ARRIVAL'].apply(dtf.convert_to_time)
        df['ARRIVAL_TIME'] = df['ARRIVAL_TIME'].apply(dtf.convert_to_time)
        print(df.loc[:5, ['SCHEDULED_DEPARTURE', 'SCHEDULED_ARRIVAL', 'DEPARTURE_TIME',
                          'ARRIVAL_TIME', 'DEPARTURE_DELAY', 'ARRIVAL_DELAY']])

        # Statystyka kompletności danych
        missing_data_df = df.isnull().sum(axis=0).reset_index()
        missing_data_df.columns = ['Kolumna', 'Brakujace wartosci']
        missing_data_df['Kompletnosc danych (%)'] = (df.shape[0] - missing_data_df['Brakujace wartosci']) / df.shape[
            0] * 100
        print(missing_data_df.sort_values('Kompletnosc danych (%)').reset_index(drop=True))

        # Usunięcie wierszy danych z niekompletnymi informacjami
        df.dropna(inplace=True)

        return df

    def print_flights_table_statistics(self, dataframe):
        print("ilość wierszy: {}, ilość kolumn: {}".format(*dataframe.shape))
        print(dataframe.sort(columns=['MONTH', 'DAY']).head(10))

    # Funkcja zwracająca statystyki (slownik) obiektu group by
    def get_statistics(self, group):
        return {'minimum': group.min(), 'maximum': group.max(), 'ilosc_wierszy': group.count(), 'srednia': group.mean()}


# Wypisanie statystyk tabeli lotów
if __name__ == "__main__":
    init_data = InitAndPrepare()
    dtf = init_data.init_dataframe('FLIGHTS')
    init_data.print_flights_table_statistics(dtf)
    init_data.close_connection()
