'''
import sys
sys.path.append('../scripts')
import pdmunging as pdm
'''

import pandas as pd
import numpy as np


def null_values(dataframe):
    nulls = 1-(dataframe.count()/len(dataframe))
    return nulls[nulls!=0]

def negative_values(dataframe):
    arrnegativos = []
    for coluna in dataframe.columns:
        considerar = ['int64', 'float64']
        if dataframe[coluna].dtypes in considerar:
            numnegativos = len(dataframe[dataframe[coluna]<0])
            percentual = numnegativos/len(dataframe[coluna]) 
            if percentual > 0:
                arrnegativos.append([coluna, len(dataframe[coluna]), numnegativos, percentual ])
    return arrnegativos

def fill_na_median(dataframe, grupo, valor, tipo='median'):
    return dataframe[valor].fillna\
        (dataframe.groupby(grupo)[valor]\
         .transform(tipo))

def set_onehotencoding(dataframe, coluna, prefixo):
    cols = pd.get_dummies(dataframe[coluna], prefix=prefixo)
    dataframe.drop(coluna, axis=1, inplace=True)
    return pd.concat([dataframe,cols],axis=1)

def coluna_agg(dataframe, grupo, valor, tipo='count'):
    return dataframe.groupby(grupo)[valor].transform(tipo)

def trendserie(serie, freq=6):
    """
    returns the percentual variation between min and max of trend.
    
    require :
        from numpy import isnan
        from statsmodels.tsa.seasonal import seasonal_decompose

    Example : 
    trendserie([10,11,15,11,13,4,11,12,16,12,14,11,10,11,15,11,13,4,11,12,16,12,14,11])
    0.14569536423841078
    
    
    """
    t = seasonal_decompose(serie, freq=freq).trend
    notna = t[~np.isnan(t)]
    return 1-(notna.min()/notna.max())
