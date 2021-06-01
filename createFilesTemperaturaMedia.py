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
dateIndex = 16
valueIndex = 17


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

def calculateNewData(min_temp, max_temp, data_min, data_max, min_temp_index, max_temp_index):
    for d in range(len(min_temp)):
        for dt in range(len(max_temp)):
            if min_temp[d] == max_temp[dt]:
                average = (data_max[max_temp_index[dt]][valueIndex] + data_min[min_temp_index[d]][valueIndex])/2
                
                # print(average)
                data_max[max_temp_index[dt]][valueIndex] = average
                break
    return data_max

def readFiles():
    maxTempFiles = listdir(relative_path_max_temp)
    # stationCode = ''
    # stationName = ''
    # latitude = ''
    # longitude = ''
    # height = ''
    for pf in maxTempFiles:
        print(f'start {pf}')
        data = pd.read_csv(f'{relative_path_max_temp}/{pf}')
        data2 = pd.read_csv(f'{relative_path_min_temp}/{pf}')
        # to_drop = list(filter(lambda x: x not in ["CodigoEstacion", "NombreEstacion", "Valor", "Fecha", "Altitud", "Longitud", "Latitud"], data.columns))        
        # data = data.drop(to_drop, axis=1)
        # data2 = data2.drop(to_drop, axis=1)
        lines = [list(data.columns)]
        print(lines[0][valueIndex])
        data = data.values.tolist()
        data2 = data2.values.tolist()
        # firstTime = True
        start_year = 1976
        # new_line_csv = []
        for i in range(1):
            print("año",start_year+i)
            start_date = datetime.date(start_year+i,1,1)
            current_date = start_date
            current_date_copy = start_date
            end_date = datetime.date(2006, 1, 1)
            days_between = (end_date - current_date).days
            days_between_copy = (end_date - current_date).days
            days_for_percentage = days_between
            
            max_temp_dates = []
            max_temp_index = []
            min_temp_dates = []
            min_temp_index = []
            max_index = -1
            min_index = -1
            for d in data:
                max_index += 1
                # if firstTime:
                #     firstTime = False
                #     new_line_csv.append(f'{d[stationCodeIndex]}')
                #     new_line_csv.append(f'{d[stationNameIndex]}')
                #     new_line_csv.append(f'{d[latitudeIndex]}')
                #     new_line_csv.append(f'{d[longitudeIndex]}')
                #     new_line_csv.append(f'{d[heightIndex]}')
                # print(d[dateIndex])
                date = dt.strptime (f'{d[dateIndex].split(" ")[0]}', "%Y-%m-%d")
                date = datetime.date(date.year, date.month, date.day)
                
                for single_date in (current_date + datetime.timedelta(n) for n in range(days_between)):
                    if date < single_date:
                        break
                    if(date == single_date):
                        max_temp_dates.append(single_date)
                        max_temp_index.append(max_index)
                        current_date = single_date + datetime.timedelta(1)
                        # new_line_csv.append(f'{1}')
                        break
                days_between = (end_date - current_date).days 
            
            for d in data2:
                min_index += 1
                date = dt.strptime (f'{d[dateIndex].split(" ")[0]}', "%Y-%m-%d")
                date = datetime.date(date.year, date.month, date.day)
                
                for single_date in (current_date_copy + datetime.timedelta(n) for n in range(days_between_copy)):
                    
                    if date < single_date:
                        break
                    if(date == single_date):
                        min_temp_dates.append(single_date)
                        min_temp_index.append(min_index)
                        current_date_copy = single_date + datetime.timedelta(1)
                        # new_line_csv.append(f'{1}')
                        break
                days_between_copy = (end_date - current_date_copy).days 

            new_data = calculateNewData(min_temp_dates, max_temp_dates, data2, data, min_temp_index, max_temp_index)
            for nd in new_data:
                lines.append(nd)
            
        
            newLines = []
            for l in lines:
                s = ","
                for x in range(len(l)):
                    l[x] = str(l[x])
                    l[x] = l[x].replace(",", "")
                nl = s.join(l)  
                newLines.append(nl)

            separator = "\n"

            newText = separator.join(newLines)
            
            
            print("Write", pf)
            f = open(f'TemperaturaMedia/{pf}', "a")
            f.write(newText)
            f.close()
            print("End write", pf)


        

        

readFiles()
