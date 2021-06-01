import pandas as pd
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


def generateFirstLine():
    
    line = ["CodigoEstacion", "NombreEstacion", "Altura", "Latitud", "Longitud"]
    end_date = datetime.date(2006, 1, 1)
    # days_between = (end_date - start_date).days
    
    start_year = 1976
    end_year = 2006
    # for single_date in (start_date + datetime.timedelta(n) for n in range(days_between)):
    #     line.append(f'{single_date}')
    
    for i in range(11):
        line.append(f'{start_year + i} - {end_year}')    

    return line

def readFiles():
    precipitationFiles = listdir(relative_path_precipitacion)
    # stationCode = ''
    # stationName = ''
    # latitude = ''
    # longitude = ''
    # height = ''
    lines = [generateFirstLine()]
    print("Primera linea",len(lines[0]))
    count_fatals = 0
    fatals = []
    for pf in precipitationFiles:
        print(f'start {pf}')
        data = pd.read_csv(f'{relative_path_precipitacion}/{pf}')
        to_drop = list(filter(lambda x: x not in ["CodigoEstacion", "NombreEstacion", "Valor", "Fecha", "Altitud", "Longitud", "Latitud"], data.columns))        
        data = data.drop(to_drop, axis=1)
        data = data.values.tolist()
        firstTime = True
        start_year = 1976
        new_line_csv = []
        continue_bool = False
        for i in range(11):
            start_date = datetime.date(start_year+i,1,1)
            current_date = start_date
            end_date = datetime.date(2006, 1, 1)
            days_between = (end_date - current_date).days
            days_for_percentage = days_between
            days_to_count = 0
            if continue_bool:
                break
            for d in data:
                try:
                    if firstTime:
                        firstTime = False
                        new_line_csv.append(f'{d[stationCodeIndex]}')
                        new_line_csv.append(f'{d[stationNameIndex]}')
                        new_line_csv.append(f'{d[latitudeIndex]}')
                        new_line_csv.append(f'{d[longitudeIndex]}')
                        new_line_csv.append(f'{d[heightIndex]}')
                    date = dt.strptime (f'{d[dateIndex].split(" ")[0]}', "%Y-%m-%d")
                except:
                    print("FATAAAAAAL", pf)
                    fatals.append(pf)
                    continue_bool = True
                    count_fatals+= 1
                    break
                    

                date = datetime.date(date.year, date.month, date.day)
                
                for single_date in (current_date + datetime.timedelta(n) for n in range(days_between)):
                    if date < single_date:
                        break
                    if(date == single_date):
                        current_date = single_date + datetime.timedelta(1)
                        # new_line_csv.append(f'{1}')
                        break
                    else:
                        days_to_count +=1
                        # new_line_csv.append(f'{0}')
                days_between = (end_date - current_date).days 
            if(days_between>0):
                for single_date in (current_date + datetime.timedelta(n) for n in range(days_between)):
                    days_to_count +=1
                    # new_line_csv.append(f'{0}')
            percentage = days_to_count/days_for_percentage
            
            new_line_csv.append(f'{percentage}')
        if(len(new_line_csv) == 16):
            lines.append(new_line_csv)
        print(f'end {pf}', len(new_line_csv))
    newLines = []
    print("count fatals", count_fatals, fatals)
    for l in lines:
        s = ", "
        print(l)
        print(l[1])
        nl = s.join(l)  
        newLines.append(nl)

    separator = "\n"

    newText = separator.join(newLines)
    
    

    f = open("porcentajeIntento.csv", "a")
    f.write(newText)
    f.close()


        

        

readFiles()
