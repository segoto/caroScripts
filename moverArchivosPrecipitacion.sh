#!/bin/bash

cd Precipitacionmedia

for d in */ ; do
    echo "$d"
    cd $d
    for z in *.zip; do
      echo "unzip $z"
      unzip $z
      mv excel.csv.csv ~/tesisCaro/PrecipitacionMedia/"${d//\/}".csv
    done
    cd ..
done