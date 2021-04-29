import pandas as pd
import numpy as np
import copy
from os import listdir
import datetime 
from datetime import datetime as dt


relative_path_precipitacion = "./PrecipitacionMedia"
relative_path_max_temp = "./TemperaturaMaxima"
relative_path_min_temp = "./TemperaturaMinima"
stationCodeIndex = 0
stationNameIndex = 1
latitudeIndex = 2
longitudeIndex = 3
heightIndex = 4
dateIndex = 5
valueIndex = 6


def generateFirstLine(initial_date):
    line = ["CodigoEstacion", "Altura"]
    end_date = datetime.date(2006, 1, 1)
    days_between = (end_date - initial_date).days
    
    for single_date in (initial_date + datetime.timedelta(n) for n in range(days_between)):
        line.append(f'{single_date}')

    return line

def readFiles(relative_path, initial_date, file_name):
    precipitationFiles = listdir(relative_path)
    stationCode = ''
    stationName = ''
    latitude = ''
    longitude = ''
    height = ''
    lines = [generateFirstLine(initial_date)]
    names = []
    print("Primera linea",len(lines[0]))
    for pf in precipitationFiles:
        print(f'start {pf}')
        data = pd.read_csv(f'{relative_path}/{pf}')
        to_drop = list(filter(lambda x: x not in ["CodigoEstacion", "NombreEstacion", "Valor", "Fecha", "Altitud", "Longitud", "Latitud"], data.columns))        
        data = data.drop(to_drop, axis=1)
        names.append(data['NombreEstacion'].tolist()[0])
        data = data.values.tolist()
        current_date = initial_date
        end_date = datetime.date(2006, 1, 1)
        days_between = (end_date - current_date).days
        days_for_percentage = days_between
        days_to_count = 0
        new_line_csv = []
        firstTime = True
        
        name = ''
        for d in data:
            if firstTime:
                firstTime = False
                new_line_csv.append(d[stationNameIndex])
                new_line_csv.append(f'{d[heightIndex]}')
            date = dt.strptime (f'{d[dateIndex].split(" ")[0]}', "%Y-%m-%d")
            date = datetime.date(date.year, date.month, date.day)
            
            for single_date in (current_date + datetime.timedelta(n) for n in range(days_between)):
                if date < single_date:
                    break
                if(date == single_date):
                    current_date = single_date + datetime.timedelta(1)
                    new_line_csv.append(d[valueIndex])
                    break
                else:
                    days_to_count +=1
                    new_line_csv.append(None)
            days_between = (end_date - current_date).days 
        if(days_between>0):
            for single_date in (current_date + datetime.timedelta(n) for n in range(days_between)):
                days_to_count +=1
                new_line_csv.append(None)
        
        
        
        lines.append(new_line_csv)
        print(f'end {pf}', len(new_line_csv))

    new_lines = np.array(lines)
    new_lines = new_lines.transpose()
    
    new_data = pd.DataFrame(data=new_lines[1:,1:], index=new_lines[1:, 0], columns=new_lines[0, 1:]).astype(float)
    print(new_data.head())
    corr = new_data.corr()
    corr.to_csv(file_name)    

# precipitacion 1 vez
# temp min 2 veces 81, 86
#temp max 2 veces 81, 86


def createFiles():
    dates = [datetime.date(1976, 1, 1), datetime.date(1981, 1, 1), datetime.date(1986, 1, 1), datetime.date(1981, 1, 1), datetime.date(1986, 1, 1)]
    sub_dir = "./correlacion"
    file_names = [f'{sub_dir}/correlacionPrecipitacion.csv', f'{sub_dir}/correlacionTemperaturaMax81.csv', f'{sub_dir}/correlacionTemperaturaMax86.csv', f'{sub_dir}/correlacionTemperaturaMin81.csv', f'{sub_dir}/correlacionTemperaturaMin86.csv']
    relative_paths = [relative_path_precipitacion, relative_path_max_temp, relative_path_max_temp, relative_path_min_temp, relative_path_min_temp]
    for i in range(len(dates)):
        print("generate ",file_names[i])
        readFiles(relative_paths[i], dates[i], file_names[i])
        print("generated", file_names[i])
        

        

createFiles()
