import pandas as pd
import numpy as np
from os import listdir
import datetime 
from datetime import datetime as dt


relative_path_precipitacion = "./PrecipitacionMedia"
relative_path_max_temp = "./TemperaturaMaxima"
relative_path_min_temp = "./TemperaturaMinima"
stationCodeIndex = 0
stationNameIndex = 1
heightIndex = 2
dateIndex = 3
valueIndex = 4

start_date = datetime.date(1976,1,1)



def readFiles():
    precipitationFiles = listdir(relative_path_precipitacion)
    stationCode = ''
    stationName = ''
    latitude = ''
    longitude = ''
    height = ''
    lines = [["CodigoEstacion", "NombreEstacion", "Altura", "Promedio", "Desviacion Estandar", "Coeficiente de variacion"]]
    print("Primera linea",len(lines[0]))
    for pf in precipitationFiles:
        print(f'start {pf}')
        data = pd.read_csv(f'{relative_path_precipitacion}/{pf}')
        to_drop = list(filter(lambda x: x not in ["CodigoEstacion", "NombreEstacion", "Valor", "Fecha", "Altitud"], data.columns))        
        data = data.drop(to_drop, axis=1)
        data = data.values.tolist()

        current_date = start_date
        end_date = datetime.date(2006, 1, 1)
        days_between = (end_date - current_date).days
        days_for_percentage = days_between
        days_to_count = 0
        new_line_csv = []
        firstTime = True
        data_to_calculate = []
        for d in data:
            if firstTime:
                firstTime = False
                new_line_csv.append(f'{d[stationCodeIndex]}')
                new_line_csv.append(f'{d[stationNameIndex]}')
                new_line_csv.append(f'{d[heightIndex]}')
            date = dt.strptime (f'{d[dateIndex].split(" ")[0]}', "%Y-%m-%d")
            date = datetime.date(date.year, date.month, date.day)
            
            for single_date in (current_date + datetime.timedelta(n) for n in range(days_between)):
                if date < single_date:
                    break
                if(date == single_date):
                    current_date = single_date + datetime.timedelta(1)
                    data_to_calculate.append(d[valueIndex])
                    break
                else:
                    days_to_count +=1
                    
            days_between = (end_date - current_date).days 
        
        average = np.average(data_to_calculate)
        standar_dev = np.std(data_to_calculate)
        coeficiente_variacion = average/standar_dev
        new_line_csv.append(f'{average}')
        new_line_csv.append(f'{standar_dev}')
        new_line_csv.append(f'{coeficiente_variacion}')
        
        lines.append(new_line_csv)
        print(f'end {pf}', len(new_line_csv))
    newLines = []
    for l in lines:
        s = ", "
        print(l[1])
        nl = s.join(l)  
        newLines.append(nl)

    separator = "\n"

    newText = separator.join(newLines)
    
    

    f = open("coeficienteVariacionPrecipitacion.csv", "a")
    f.write(newText)
    f.close()


        

        

readFiles()
