#!/bin/sh

for j in $(seq 1 1251)
do

cat combineImages.py | sed 's/asdf/'`head -1 r1.txt`'/g' | sed 's/qwer/'`head -1 r2.txt`'/g' | sed 's/zxcv/'`head -1 r4.txt`'/g' | sed 's/hjkl/'`head -1 r5.txt`'/g' > cim.py

~/Downloads/lr2024/asdf/bin/python cim.py

mv Combined.png combos/c_$j.png
echo "Created c_$j.png"

tail -n +2 r1.txt > tmp.txt
	mv tmp.txt r1.txt
tail -n +2 r2.txt > tmp.txt
        mv tmp.txt r2.txt
tail -n +2 r4.txt > tmp.txt
        mv tmp.txt r4.txt
tail -n +2 r5.txt > tmp.txt
        mv tmp.txt r5.txt

done
