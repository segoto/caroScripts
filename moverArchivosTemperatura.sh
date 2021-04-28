#!/bin/bash

cd Temperaturamedia

for d in */ ; do
    echo "$d"
    cd $d
    for z in *.zip; do
      echo "unzip $z"
      unzip $z
      if [[ $z == *"max"* ]]; then
        mv excel.csv.csv ~/tesisCaro/TemperaturaMaxima/"${d//\/}".csv
      else
        mv excel.csv.csv ~/tesisCaro/TemperaturaMinima/"${d//\/}".csv
      fi
    done
    cd ..
done