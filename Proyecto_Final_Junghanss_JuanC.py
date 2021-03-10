import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import datetime as dt
import seaborn as sns

class GetData:
    """
    Para la obtención y manejo de datos se construye una clase que encapsulará la información a descargar, 
    disponiendo también de métodos para su posterior administración y visualización.
    """


    def __init__(self):     # constructor: dejaremos creados los dataframes y listas propios de la clase necesarios para usar en las funciones
        self.df = pd.DataFrame()
        self.fallas_datos = []
        self.rendimiento_df = None
        self.rendimiento_acumulado_df = None


    def historical_data(self, lista_activos, Period):
        """
        Función para la descarga y administración de los datos históricos de los activos target. 
        Parámetros: lista de activos/strings y período (string).
        Se define un loop que itera la lista de activos para la descarga de cada uno y ajuste dentro de un DataFrame.
        Se atrapa cualquier excepción en la ejecución del método para imprimirla en pantalla junto con el nombre de activo (mensaje personalizado).
        """
        for activos in lista_activos:
            try:
                data = yf.download(activos, start="2015-01-01", end=dt.date.today().strftime("%Y-%m-%d"))
                data.rename(columns={"Adj Close": activos}, inplace=True)                
                data.drop(["Open", "High", "Low", "Close", "Volume"], axis=1, inplace=True)             
                self.df = self.df.merge(data, right_index=True, left_index=True, how="outer").resample(Period).last()                
                print("\n Data historica (tail preview): \n",self.df.tail())
                # self.df.to_csv("precios.csv", decimal=',', sep=';')       # En caso que se desee exportar en archivo separado por comas los datos de las criptomonedas del dataframe 
            except Exception as e:
                print(e)
                self.fallas_datos.append(activos)
                print("NO SE PUEDEN DESCARGAR DATOS DE: {0}".format(self.fallas_datos))


    def returns(self):
        """
        Función que gestiona los rendimientos de los activos en DataFrames individuales.
        Se obtienen los rendimientos diarios al eliminar la tendencia en la evolución del precio porcentualizando el cambio con el método DataFrame.pct_change() 
        Se obtiene el rendimiento acumulado final al efectuar la suma acumulada de cada columna, simplemente con el método DataFrame.cumsum()
        Cada rendimiento es imprimido en consola, con vista previa corta (tail preview).
        """
        self.rendimiento_df = self.df.pct_change()      # Documentacion: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pct_change.html
        print("\n Rendimientos diarios (tail preview): \n",self.rendimiento_df.tail())
        self.rendimiento_acumulado_df = self.rendimiento_df.cumsum()
        print("\n Rendimiento acumulado: \n",self.rendimiento_acumulado_df.tail(1))


    def ploting_returns(self):
        """
        Función que ejecuta los gráficos y posterior visualización de estos para:
        - Evolución 2015-2021 en gráfico de lineas
        - Rendimiento diario 2015-2021 en gráfico de lineas
        - Matriz de correlaciones (método Pearson)
        """
        self.df.plot()
        plt.ylabel(ylabel='Precio (Expresado en USD)')
        plt.xlabel(xlabel='Tiempo')
        plt.title(label='Evolución 2015-2021')
        plt.show()

        self.rendimiento_df.plot()
        plt.ylabel(ylabel='Rendimiento')
        plt.xlabel(xlabel='Tiempo')
        plt.title(label='Rendimiento Diario (Periodo 2015-2021)')
        plt.show()

        sns.heatmap(self.df.corr())
        plt.title(label='Matriz de correlaciones')
        plt.show()


data = GetData()
data.historical_data(lista_activos=['BTC-USD', 'ETH-USD', 'USDT-USD'], Period="W")
data.returns()
data.ploting_returns()