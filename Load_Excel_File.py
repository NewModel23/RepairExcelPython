"""
Created on Fri Apr 12 11:58:29 2019

@author: Raúl Guerrero

Why im doin this?:
    
Since the file provided has formated as CSV but the extension is XLSX
I made this class for clean and prepare the data before work on it
It Return a Dataframe!

"""

import pandas as pd
import re
import os

def procesa_Excel(directorio, nombre):
    # Leer el archivo de Excel proporcionado
    os.chdir(directorio)
    archivo = pd.read_excel(nombre)  
    # Obtener el nombre de la columna y guardarlo temporalmente en un arreglo
    columna = pd.Series(archivo.columns.values, name='x').head(1)
    
    # El arreglo lo convertimos a un string
    columna = columna[0]
    
    # La variable archivo recibirá el split de columna
    archivo = archivo.join(archivo[columna].str.split(',', expand=True).add_prefix('x'))
    
    # Eliminar la primer columna
    archivo.drop(archivo.columns[[0]], axis = 1, inplace=True)
    
    result = []
    [result.append(re.sub(r'[^a-zA-Z0-9_\s]+', '', x)) for x in archivo['x1']]
    
    dataA = pd.DataFrame({'Devices1': result})
    
    archivo = pd.concat([archivo, dataA], 1, ignore_index=False)
    
    # Eliminar la primer columna x1 (Device) por que ya la tenemos libre de comillas
    archivo.drop(archivo.columns[[1]], axis = 1, inplace=True)
    
    columnas = [0, 11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    archivo = archivo[archivo.columns[columnas]]
    
    archivo.columns = ['date', 'device', 'failure','attribute1','attribute2','attribute3','attribute4','attribute5','attribute6','attribute7','attribute8','attribute9']
    
    archivo[['failure','attribute1','attribute2','attribute3','attribute4','attribute5','attribute6','attribute7','attribute8','attribute9']] = archivo[['failure','attribute1','attribute2','attribute3','attribute4','attribute5','attribute6','attribute7','attribute8','attribute9']].apply(pd.to_numeric)
    
    archivo['month'] = pd.DatetimeIndex(archivo['date']).month
    
    return archivo

