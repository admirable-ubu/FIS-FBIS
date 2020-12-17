#!/bin/bash

route=$1
file=$2
name=$3

mkdir tmp
cp $route/$file tmp
cd tmp

tar -xaf $file
r="./home/paciente/Descargas"
for i in $(ls -1 $r/*.webm)
do
    echo "file '"$i"'" >> mylist.txt
done
ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.webm 2>/dev/null >> /dev/null

audios=$(ls -1 $r/*.ogg)
if [ $? -eq 0 ]; then
    echo "" > mylist.txt
    for i in $audios
    do
        echo "file '"$i"'" >> mylist.txt
    done
    ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.ogg 

    ffmpeg -i output.webm -i output.ogg -c:v copy -c:a copy output2.webm
else
    mv output.webm ouput2.webm
fi

ffmpeg -i output2.webm -filter:v fps=10 $name 2>/dev/null >> /dev/null

cp $name $route/../static/videos/processed/

cd ..
rm -rf tmp
